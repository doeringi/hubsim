FROM nvcr.io/nvidia/pytorch:23.10-py3
RUN apt-get update && apt-get install -y python3 python3-pip git nano
COPY docker-latest-requirements.txt .
RUN pip3 install -r docker-latest-requirements.txt