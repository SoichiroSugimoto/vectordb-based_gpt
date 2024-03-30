# VectorDB-Based_GPT
This application is RAG Chatbot, Retrieval-Augmented Generation, used on Slack.
You can use Notion as reference data store.
<img width="50%" src="https://github.com/SoichiroSugimoto/vectordb-based_gpt/assets/52186679/6ffe7367-e05c-4818-8c38-cfc4eb2acf8e">

## Prerequirements
- Docker Desktop
- OpenAI API Key
- Pinecone API Key
- Notion Integration Secret
- Slack Bot TOken


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
```
make deploy
```


## System Architecture / Tech Stack
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
