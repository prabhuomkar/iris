# api

## Getting Started

### Prerequisites
Following are the softwares requried to get everything up and running.
- [Docker](https://docs.docker.com/engine/install/) for Infrastructure Components
- [Go](https://golang.org/dl/) for API

### Installing
**For Local Setup**
- Add the below line in your `/etc/hosts`
```
127.0.0.1 storage-master storage-volume database api queue frontend worker ml
```
- Build and start the containers
```
docker-compose up -d
```

**For API**
- Install go modules 
```
go mod download
```
- Start the API
```
make run
```
- Linting the code
```
make lint
```

### Configuration
TBD
