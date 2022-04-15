FROM golang:1.17-alpine AS builder
WORKDIR /app
COPY go.mod .
COPY go.sum .
RUN go mod download
COPY . .
RUN go build -o iris-api ./cmd/iris/api

FROM alpine
LABEL author="Omkar Prabhu"
WORKDIR /app
COPY --from=builder /app/iris-api .
EXPOSE 5001
CMD ["/app/iris-api"]