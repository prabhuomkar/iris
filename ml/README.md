# ML

## Getting Started

### Prerequisites
Following are the softwares requried to get everything up and running.
- [Docker](https://docs.docker.com/engine/install/) for Infrastructure Components
- [Python](https://www.python.org/downloads/) for ML

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

**For ML**
- Install python dependencies
```
pip install -r requirements.txt
```
- Start the ML
```
python worker.py
```
- Linting the code
```
pylint worker.py pipeline/...
```

### Configuration
TBD
