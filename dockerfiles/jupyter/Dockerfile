FROM python:3.13

ARG DIR_WORK
WORKDIR ${DIR_WORK}

ARG REQ_TXT
COPY ${REQ_TXT} .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r ${REQ_TXT}
