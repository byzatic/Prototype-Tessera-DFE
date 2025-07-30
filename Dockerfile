FROM python:3.9-slim-buster as python-base

# install tools
RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  && rm -rf /var/lib/apt/lists/*


##
FROM python-base as python-app

#
COPY . /app
WORKDIR /app

#
RUN mkdir -p /app/logs \
  && cd /app \
  && pip install -r requirements.txt

# prometheus service port
EXPOSE 8080

#
CMD chmod a+x ./run_in_docker.sh && /bin/bash ./run_in_docker.sh
