FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.9
USER root

# Install Rust and other dependencies
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN yum -y install vim-enhanced git

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy your application code
COPY vectordb-based_gpt .

# Set NLTK download directory to /tmp which is writable in Lambda environment
ENV NLTK_DATA /tmp
RUN python -m nltk.downloader stopwords

WORKDIR .
CMD [ "http_request_handler.lambda_handler" ]
