FROM alpine

ENV PYTHONUNBUFFERED=1

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

RUN apk add git

RUN python3 -m ensurepip

RUN pip3 install --no-cache --upgrade pip setuptools flask pillow json2

RUN git clone https://github.com/niklasw/bilder.git app

EXPOSE 5500

WORKDIR /app

CMD python ./app.py
