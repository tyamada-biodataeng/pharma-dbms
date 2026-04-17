FROM condaforge/miniforge3:latest

ARG DIR_WORK
WORKDIR ${DIR_WORK}/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ARG ENV_YAML
COPY ${ENV_YAML} ${DIR_WORK}/
RUN mamba update -y -c conda-forge mamba && \
    mamba env create -f ${ENV_YAML} && \
    mamba clean -a -y

USER ubuntu

ARG VENV
CMD ["mamba", "run", "-n", "${VENV}", "/bin/bash"]
