# Execution Command: docker run -it -v $(pwd)/vectordb-based_gpt:/vectordb-based_gpt vectordb-based_gpt:dev

FROM public.ecr.aws/sam/build-python3.9:1.100.0-20231031003451
USER root

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN yum -y install vim-enhanced git

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

VOLUME ["/vectordb-based_gpt"]

WORKDIR /vectordb-based_gpt
CMD [ "python", "main.py" ]
