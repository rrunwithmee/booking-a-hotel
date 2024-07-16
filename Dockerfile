FROM python:3.12-alpine

WORKDIR ./app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements-docker.txt

RUN pip install jinja2

CMD ["python", "main.py"]
