# iris

## About
WIP

### Architecture
TODO: Add diagram

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [Deployment](#deployment) section for on how to deploy the project on a live system.

### Development & Testing

#### Prerequisites
Following are the softwares requried to get everything up and running.
- [Docker](https://docs.docker.com/engine/install/) for Infrastructure Components
- [Go](https://golang.org/dl/) for API
- [Node.js](https://nodejs.org/en/) for UI

#### Installing
**For API**
- Install go modules using 
```
go mod download
```
- Start the API server  
```
make run
```

**For Frontend**:
- Install the packages mentioned in package.json file for getting all dependencies of the project.
```
npm install
```
- TODO: Configuration
- Start the application
```
npm start
```

**For Local Setup**
- Add the below line in your `/etc/hosts`
```
127.0.0.1 storage-master storage-volume database api frontend
```
- Build and start the containers
```
docker-compose up -d
```

### Deployment
TODO: Add Docker related notes

## Issues
Issues are managed via GitHub Issues [here](https://github.com/prabhuomkar/iris/issues).

## Maintainers
- [Omkar Prabhu](https://github.com/prabhuomkar)
- [Akshay Pithadiya](https://github.com/akshaypithadiya)

## License
TODO: Add license
