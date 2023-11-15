# pull official base image
FROM python:3.10.6
#FROM ubuntu
#FROM alpine:3.17

# set work directory
RUN mkdir -p /src
#RUN apt update
#RUN apt install python3-pip -y
#RUN pip3 install Flask
#RUN apt-get update && apt-get install -y libpq-dev
WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DOCKER_BUILDKIT_TIMEOUT 10m
ENV SECRET_KEY dev
ENV FLASK_ENV development
ENV FLASK_APP src
ENV SQLALCHEMY_DATABASE_URI postgresql://postgres:postgres@monig.cvrntyeol4tz.us-east-2.rds.amazonaws.com/monig
ENV SQLALCHEMY_DATABASE_URI_ASNC postgresql+asyncpg://postgres:postgres@monig.cvrntyeol4tz.us-east-2.rds.amazonaws.com/monig
ENV JWT_SECRET_KEY JWT_SECRET_KEY
ENV TZ 'America/Sao_Paulo'
ENV DB_TEST sqlite:///test.db
ENV SESSION_TYPE 'redis'
ENV PORT 5000
ENV APP_PORT 5000
ENV POSTGRES_PASSWORD adminmonig
ENV POSTGRES_USER postgres
ENV POSTGRES_DATABASE postgres
ENV POSTGRES_ENDPOINT monig.chq1qedxshqi.sa-east-1.rds.amazonaws.com
ENV FLASK_DEBUG 1


# ENV POSTGRES_PASSWORD adminmonig
# ENV POSTGRES_USER postgres
# ENV POSTGRES_DATABASE monig
# ENV POSTGRES_ENDPOINT monig.cvrntyeol4tz.us-east-2.rds.amazonaws.com
# ENV FLASK_DEBUG 1

# Instale as dependências do Python
#RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

# Copie o arquivo entrypoint.sh para o diretório /usr/
COPY entrypoint.sh /
RUN chmod u+x /entrypoint.sh

# Copie o restante do projeto
COPY . /src

# Exiba o conteúdo do diretório para depuração
RUN ls -l /src

# Execute o entrypoint.sh
CMD ["/bin/bash", "/entrypoint.sh"]
#CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]