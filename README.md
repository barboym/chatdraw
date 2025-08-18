
# ChatDraw 

## Description
ChatDraw is a chatbot application that teaches users to draw simple sketches step-by-step. It generates drawing tutorials, guides users through each stroke, and provides feedback on submitted sketches. The backend is built with FastAPI and integrates with PostgreSQL for storing tutorials and user sketches. The frontend was built using vue.js and Typescript in a separate repo. The project features modular chat flows, AI-powered sketch generation, and drawing feedback.

## Serving 
For the time being the fronted is served by the backend. The bakend can be hosted any machine with a docker. 

## DataBase 
Yet to be written

## Features:
- AI-generated sketch tutorials
- Step-by-step drawing guidance
- Drawing feedback and scoring
- FastAPI REST API
- PostgreSQL database integration
- Extensible chat flow system

## Project Structure: 
chatdraw/ - core package with chat flows and sketch logic  
app.py - FastAPI server entry point  
tests/ - unit tests  
Dockerfile and docker-compose.yml - containerization

## Author: 
Moshe Barboy
