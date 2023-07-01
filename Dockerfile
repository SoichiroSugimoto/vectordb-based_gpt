FROM public.ecr.aws/sam/build-python3.9:1.79.0-20230407185812
USER root

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install python-dotenv
RUN pip install llama-index
RUN pip install pinecone-client
RUN pip install transformers

WORKDIR /src
