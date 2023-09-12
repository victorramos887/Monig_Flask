# pull official base image
FROM python:3.10.6

# set work directory
RUN mkdir -p /usr/src
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY dev
ENV FLASK_ENV development
ENV FLASK_APP src
ENV  SQLALCHEMY_DATABASE_URI postgresql://postgres:postgres@192.168.15.9:5432/monig
ENV SQLALCHEMY_DATABASE_URI_ASNC postgresql+asyncpg://postgres:postgres@192.168.15.9:5432/monig
ENV JWT_SECRET_KEY JWT_SECRET_KEY
ENV TZ 'America/Sao_Paulo'
ENV DB_TEST sqlite:///test.db
ENV SESSION_TYPE 'redis'
ENV PORT 5000
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_USER postgres
ENV POSTGRES_DATABASE monig
ENV POSTGRES_ENDPOINT xxxx:5432

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY entrypoint.sh /usr/src/
RUN chmod u+x /usr/entrypoint.sh

COPY . /usr/src/

RUN ls


# run entrypoint.sh
CMD ["/bin/bash", "/usr/src/entrypoint.sh"]