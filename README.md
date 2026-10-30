# Paris Travel Assistant - RAG Project

## Topic
The selected topic is travel in Paris.  
The application helps users ask questions about attractions, food, transportation, safety tips, and general travel information in Paris.

## Documents Used
The knowledge base was built using a small set of text documents about Paris:
- Paris overview
- Top attractions
- Transportation
- Food and cafes
- Best time to visit
- Travel tips and safety

The documents were uploaded to Amazon S3 and connected to Amazon Bedrock Knowledge Base.

## Project Flow
Documents → Amazon S3 → Amazon Bedrock Knowledge Base → Flask App → Docker → EC2 → Public Web App

## How the App Works
The user enters a question in the Flask web page.  
The Flask backend sends the question to Amazon Bedrock using boto3.  
Bedrock retrieves relevant information from the knowledge base and returns an answer to the user.

## Technologies Used
- Python
- Flask
- boto3
- Amazon S3
- Amazon Bedrock Knowledge Base
- Docker
- Amazon EC2
- HTML
- CSS

## Main Files
- app.py: Flask backend application
- templates/index.html: Web page structure
- static/style.css: Page design
- requirements.txt: Python dependencies
- Dockerfile: Docker container configuration

## Docker Commands Used

Build the Docker image:

```bash
docker build -t paris-rag-app .
```

Run the container:

```bash
docker run -p 5000:5000 paris-rag-app
```

Open the app in the browser:

```text
http://localhost:5000
```
## EC2 Deployment

The Dockerized application was deployed on an AWS EC2 instance.  
Docker was installed on the instance, the project files were copied to EC2, and the container was run using port 5000.


The application was tested using the public IP address:

```text
http://54.84.11.0:5000
```