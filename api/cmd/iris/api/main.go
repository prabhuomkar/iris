package main

import (
	"errors"
	"fmt"
	"log"
	"net/http"

	"iris/api/internal/config"
	"iris/api/internal/graph/generated"
	"iris/api/internal/graph/resolvers"
	"iris/api/pkg/mongo"

	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/handler/extension"
	"github.com/99designs/gqlgen/graphql/handler/transport"
	"github.com/99designs/gqlgen/graphql/playground"
	"github.com/go-chi/chi"
	"github.com/rs/cors"
)

func main() {
	// later(omkar): Initialize gRPC clients
	// later(omkar): Handle graceful shutdowns
	cfg, err := config.Init()
	if err != nil {
		panic(err)
	}

	db, err := mongo.Init(cfg.Database.URI, cfg.Database.Name)
	if err != nil {
		panic(err)
	}

	router := chi.NewRouter()
	router.Use(cors.Default().Handler)

	c := generated.Config{
		Resolvers: &resolvers.Resolver{
			Config: &cfg,
			DB:     db,
		},
	}

	srv := handler.New(generated.NewExecutableSchema(c))
	srv.AddTransport(transport.Options{})
	srv.AddTransport(transport.POST{})
	srv.AddTransport(transport.GET{})
	srv.Use(extension.Introspection{})

	router.Handle("/", playground.Handler("graphql playground", "/graphql"))
	router.Handle("/graphql", srv)

	log.Printf("starting graphql server on port:%d", cfg.Port)

	err = http.ListenAndServe(fmt.Sprintf(":%d", cfg.Port), router)
	if err != nil && errors.Is(err, http.ErrServerClosed) {
		log.Fatal(err)
	}
}
