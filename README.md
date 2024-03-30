# VectorDB-Based_GPT
This application is RAG Chatbot, Retrieval-Augmented Generation, used on Slack.
You can use Notion as reference data store.

## Prerequirements
- Docker Desktop
- OpenAI API Key
- Pinecone API Key
- Notion Integration Secret


## Preprocessing
Execute NotionReader(NotionReader.ipynb) on Google Colaboratory. NotionReader is a tool that fetches reference data from Notion, converts them into vector data, and stores them in a vector database.

## Usage
You can use it on 2 ways.
### CLI
deployed on local environment.
```
$ docker compose up -d --build
```
```
$ docker compose exec vectordb-based_gpt-local bash
```

### Slack
deployed on AWS environment.


## 🏗 System Architecture / Tech Stack
This application relies on several key technologies for its operation:<br>

### ■ AWS Lambda
AWS Lambda handles the backend logic of the application. It's responsible for executing functions in response to events like HTTP requests.

**Environment Variables:**
- AWS_ACCESS_KEY_ID: AWS Access Key
- AWS_SECRET_KEY: AWS Secret Key

### ■ Amazon ECR
ECR is used as a Docker container registry to store the Docker images used in this application via AWS Lambda.

### ■ Amazon DynamoDB
DynamoDB is used for accessibility control. It chooses accessible data from a vector database based on the user.


### ■ Pinecone
Pinecone is used for vector databases to store vector data made from text data.

**Environment Variables:**

- PINECONE_API_KEY: Pinecone API Key
- PINECONE_ENVIRONMENT: The environment for your Pinecone project
- PINECONE_INDEX_NAME: The name of your Pinecone project
  
<br>

## Third-Party Integrations
This application integrates with various third-party services for enhanced functionalities:

### ■ Slack API
The Slack API is used for Chatbot that creates completion based on vector data.

**Environment Variables:**

- SLACK_BOT_TOKEN: Slack Bot User OAuth Token

### ■ OpenAI API
The OpenAI API is used for natural language understanding and other AI-powered features. You'll need an OpenAI API key for these features.

**Environment Variables:**

- OPENAI_API_KEY: OpenAI API Key
