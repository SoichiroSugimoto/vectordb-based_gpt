FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.9
USER root

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN yum -y install vim-enhanced git

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
COPY vectordb-based_gpt/* .

WORKDIR .
CMD [ "http_request_handler.lambda_handler" ]
