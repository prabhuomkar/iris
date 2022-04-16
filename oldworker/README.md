# Worker

## Getting Started

### Prerequisites
Following are the softwares requried to get everything up and running.
- [Docker](https://docs.docker.com/engine/install/) for Infrastructure Components
- [Python](https://www.python.org/downloads/) for Worker

### Installing
**For Local Setup**
- Add the below line in your `/etc/hosts`
```
127.0.0.1 cdn-master cdn-volume database api queue frontend worker ml
```
- Build and start the containers
```
docker-compose up -d
```

**For Worker**
- Install python dependencies
```
pip install -r requirements.txt
```
- Start the Worker
```
python worker.py
```
- Linting the code
```
pylint ./*.py pipeline/...
```

### Configuration
TBD
