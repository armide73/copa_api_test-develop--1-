FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin
RUN mkdir /copa
WORKDIR /copa
ADD requirements.txt /copa/
RUN pip install -r requirements.txt
ADD . /copa/
