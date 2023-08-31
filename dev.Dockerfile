# Build: docker build -t vectordb_base_gpt:dev -f dev.Dockerfile .
FROM public.ecr.aws/sam/build-python3.9:1.96.0-20230829212321
USER root

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN yum -y install vim-enhanced git

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

WORKDIR .
