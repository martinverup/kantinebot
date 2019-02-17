FROM alpine:latest

COPY . /home

WORKDIR /home

RUN apk add --no-cache python3 python3-dev tzdata \
    && pip3 install -r requirements.txt \
    && cp /usr/share/zoneinfo/Europe/Copenhagen /etc/localtime \
    && apk del --no-cache python3-dev tzdata \
    && rm requirements.txt Dockerfile

CMD ["python3", "kantine.py"]
