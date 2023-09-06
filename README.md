# 🐿VectorDB-Based_GPT
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
```
$ docker compose exec app bash
```

3. Now you can execute Python files within the Docker container.

**File loading**
```
$ python file_loader.py
```
**Chatbot creation**
```
$ python main.py
```
