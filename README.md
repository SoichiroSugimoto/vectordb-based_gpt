# VectorDB-Based_GPT
This application offers a set of valuable tools that enable you to perform the following tasks with ease:
- File loading: Convert text data into vector data and insert it into a vector database.
- Chatbot creation: Create a query engine using the data stored in the vector database.

It also allows you to set this accessibility of data for each user by mapping it to the data in DynamoDB. <br><br>


## 💻 Usage
To set up and run the project, execute the following Docker commands:
1. Build and start the Docker containers:
```bash
$ docker compose up -d --build
```

2. Access the application's container:
```bash
$ docker compose exec app bash
```

3. Now you can execute Python files within the Docker container.

- **File loading 🗂**:<br>
  First, make sure you have a `data` directory under the `root` directory of the project. Then run the following command to load files:
  ```bash
  $ python file_loader.py
  ```
- **Chatbot creation 🤖**:<br>
  Run the following command to start the chatbot:
  ```bash
  $ python main.py
  ```

<br>

**You can use Slack as an Interface of Chatbot as well.**

<br>

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

## 🌐 Third-Party Integrations
This application integrates with various third-party services for enhanced functionalities:

### ■ Slack API
The Slack API is used for Chatbot that creates completion based on vector data.

**Environment Variables:**

- SLACK_BOT_TOKEN: Slack Bot User OAuth Token

### ■ OpenAI API
The OpenAI API is used for natural language understanding and other AI-powered features. You'll need an OpenAI API key for these features.

**Environment Variables:**

- OPENAI_API_KEY: OpenAI API Key
