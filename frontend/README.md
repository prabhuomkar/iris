# frontend

## Getting Started

### Prerequisites
Following are the softwares requried to get everything up and running.
- [Docker](https://docs.docker.com/engine/install/) for Infrastructure Components
- [Node.js](https://nodejs.org/en/) for UI

### Installing
**For Local Setup**
- Add the below line in your `/etc/hosts`
```
127.0.0.1 storage-master storage-volume database api queue frontend ml
```
- Build and start the containers
```
docker-compose up -d
```

**For Frontend**
- Install the npm dependencies
```
npm install
```
- Start the frontend
```
npm start
```
- Lint the code
```
npm run lint
```

### Configuration
TBD
