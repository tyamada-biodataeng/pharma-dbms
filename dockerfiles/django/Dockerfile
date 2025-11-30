FROM python:3.13

ARG DIR_WORK
WORKDIR ${DIR_WORK}

ARG REQ_DIR
COPY ${REQ_DIR}/ ${REQ_DIR}/

ARG REQ_TXT
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r ${REQ_DIR}/${REQ_TXT}
