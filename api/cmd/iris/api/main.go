package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"iris/api/internal/config"
	"iris/api/internal/graph/generated"
	"iris/api/internal/graph/resolvers"
	"iris/api/pkg/mongo"
	"iris/api/pkg/rabbitmq"

	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/handler/extension"
	"github.com/99designs/gqlgen/graphql/handler/transport"
	"github.com/99designs/gqlgen/graphql/playground"
	"github.com/go-chi/chi"
	"github.com/linxGnu/goseaweedfs"
	"github.com/rs/cors"
)

const shutdownTime = 10

func main() {
	// handle graceful shutdown
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt, syscall.SIGINT, syscall.SIGTERM)

	// initialize config
	cfg, err := config.Init()
	if err != nil {
		panic(err)
	}

	db, err := mongo.Init(cfg.Database.URI, cfg.Database.Name)
	if err != nil {
		panic(err)
	}

	queue, err := rabbitmq.Init(cfg.Queue.URI, cfg.Queue.Name)
	if err != nil {
		panic(err)
	}

	seaweed, err := goseaweedfs.NewSeaweed(
		cfg.CDN.URL, nil, cfg.CDN.ChunkSize,
		&http.Client{Timeout: time.Duration(cfg.CDN.Timeout) * time.Minute})
	if err != nil {
		panic(err)
	}

	router := chi.NewRouter()
	router.Use(cors.New(cors.Options{
		AllowCredentials: true,
		AllowedMethods:   []string{http.MethodPost, http.MethodGet, http.MethodOptions, http.MethodOptions},
		AllowedHeaders:   []string{"*"},
	}).Handler)

	c := generated.Config{
		Resolvers: &resolvers.Resolver{
			Config: &cfg,
			DB:     db,
			Queue:  queue,
			CDN:    seaweed,
		},
	}

	gqlHandler := handler.New(generated.NewExecutableSchema(c))
	gqlHandler.AddTransport(transport.Options{})
	gqlHandler.AddTransport(transport.POST{})
	gqlHandler.AddTransport(transport.GET{})
	gqlHandler.AddTransport(transport.MultipartForm{})
	gqlHandler.Use(extension.Introspection{})

	router.Handle("/", playground.Handler("graphql playground", "/graphql"))
	router.Handle("/graphql", gqlHandler)

	srv := &http.Server{
		Addr:    fmt.Sprintf(":%d", cfg.Port),
		Handler: router,
	}

	go func() {
		err = srv.ListenAndServe()
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			log.Fatalf("error starting iris api: %+v", err)
		}
	}()
	log.Printf("started iris api on port: %d", cfg.Port)

	<-interrupt
	log.Print("stopping iris api")

	ctx, cancel := context.WithTimeout(context.Background(), shutdownTime*time.Second)
	defer func() {
		_ = db.Client.Disconnect(ctx)

		_ = queue.Disconnect()

		cancel()
	}()

	if err := srv.Shutdown(ctx); err != nil {
		log.Printf("error shutting down iris api: %+v", err)
	}

	log.Print("stopped iris api")
}
