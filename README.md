
ChatDraw - You AI guide for drawing simple sketches
===================================================
### simple sketch drawing tutorials for whatever is on your mind
ChatDraw is a chatbot application that teaches users to draw simple sketches step-by-step. 
It generates drawing tutorials based on the concept the user provides, 
guides users through each stroke, and provides feedback for each step. 

Features
=============
![features](assets/chatdraw.gif)

- AI-generated sketch tutorials
- Step-by-step drawing guidance
- Drawing feedback and scoring
- FastAPI 
- PostgreSQL database integration


Quick Start
============
For quickly running the drawing chat service on your machine: 
1. Install [docker compose](https://docs.docker.com/compose/install/)
2. Get an [Anthropic](console.anthropic.com) API key and add it to your 
 environment variables using:
 ```bash
 export ANTHROPIC_API_KEY=<your key>
 ``` 
 Add this line to ~/.profile for persistance 

3. Download the [docker compose yaml](https://raw.githubusercontent.com/barboym/chatdraw/main/docker-compose.yml) from the repo and run it:
```bash
wget https://raw.githubusercontent.com/barboym/chatdraw/main/docker-compose.yml 
docker compose up -d
```
The site should be available on localhost:8010. 

Quick Start - K8s
==================
You can run the site using k8s. If you have a running pod and kubectr available: 
```bash
kubectl create secret generic anthropic-secret --from-literal ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f draw-service/postgres-deployment.yaml
```
The app then can be viewed on node-ip:30010 (find it out with `minikube ip`). Each service can be accessed with port-forward: 
```bash
kubectl port-forward service/postgres-dep 5433:5432 # to access the DB on localhost:5433
kubectl port-forward service/server-dep 8011:8010 # to access the app on localhost:8011
```



Project Structure
==================
draw_service/ - core package with chat flows and sketch logic  
frontend/ - vite project
k8s/ - example kubernetes configuration

Author 
===========
Moshe Barboy
