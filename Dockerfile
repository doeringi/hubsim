FROM nvidia/cuda:12.3.1-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y python3 python3-pip git nano
COPY docker-latest-requirements.txt .
RUN pip3 install -r docker-latest-requirements.txt
RUN pip3 install "fschat[model_worker,webui]"