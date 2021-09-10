all: code-quality

lint:
	golangci-lint run ./...

generate:
	go run github.com/99designs/gqlgen generate

build:
	go build -o cmd/iris/api/api cmd/iris/api/main.go

run: build
	./cmd/iris/api/api
