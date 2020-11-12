FROM ubuntu:20.04

LABEL author="arpitnarechania@gatech.edu"
LABEL maintainer="arpitnarechania@gatech.edu"

# Setup python and java and base system
ENV DEBIAN_FRONTEND noninteractive
ENV LANG=en_US.UTF-8

# Install JDK (for CoreNLP) and Python3
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -q -y openjdk-8-jdk python3-pip libsnappy-dev language-pack-en wget unzip

# Install packages
RUN pip3 install --upgrade --no-cache-dir pip requests nl4dv

# Download artefacts for Spacy and NLTK
RUN python3 -m spacy download en_core_web_sm \
    && python3 -m nltk.downloader popular

# Copy start script
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

# Copy Gunicorn config file
COPY ./gunicorn_conf.py /gunicorn_conf.py

# Copy NL4DV-specific files, namely the API end points, data assets, etc.
COPY ./app /app

# Install Requirements
RUN pip3 install -r /app/requirements.txt

# Download the English model of Stanford CoreNLP
RUN wget "https://nlp.stanford.edu/software/stanford-english-corenlp-2018-10-05-models.jar" -P /app/assets/jars/

# Download and Extract the Stanford Parser to the jars directory
RUN wget "https://nlp.stanford.edu/software/stanford-parser-full-2018-10-17.zip" -P /opt \
    && unzip /opt/stanford-parser-full-2018-10-17.zip -d /opt \
    && cp /opt/stanford-parser-full-2018-10-17/stanford-parser.jar /app/assets/jars/

# Set Working Directory. For relative paths inside the container main.py
WORKDIR /app

# Set PythonPath
ENV PYTHONPATH=/app

# Expose container port 80
EXPOSE 80

# Run the start script; it will start Gunicorn with Uvicorn
CMD ["/start.sh"]
