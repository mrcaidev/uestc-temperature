# syntax=docker/dockerfile:1

FROM python:3-slim

WORKDIR /app

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install --upgrade pip
RUN pip3 install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install

COPY . .

CMD [ "pipenv", "run", "python", "-u", "src/main.py" ]
