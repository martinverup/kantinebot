FROM alpine:latest

WORKDIR /home

COPY requirements.txt .
COPY today.py .

RUN apk add --no-cache python3 py3-pip \
    && pip install -r requirements.txt \
    && apk del --no-cache py3-pip \
    && rm requirements.txt

ARG LINK="https://issmenuplan.dk/Kundelink?GUID=fec3896c-cc3f-47f8-ac77-74826a4ae4e9"
ENV LINK=$LINK

CMD ["python3", "today.py"]
