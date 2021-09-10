FROM golang:1.15-alpine
WORKDIR /build
COPY go.mod .
COPY go.sum .
RUN go mod download
COPY . .
RUN go build -o iris-api ./cmd/iris/api
WORKDIR /dist
RUN cp /build/iris-api .
EXPOSE 5001
CMD /dist/iris-api
