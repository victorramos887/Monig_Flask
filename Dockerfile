FROM python:3.10.4



# Instala o PostgreSQL
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src

#Variáveis de ambiente.
ENV SECRET_KEY=dev \
    FLASK_ENV=development \
    FLASK_APP=src \
    SQLALCHEMY_DATABASE_URI=postgres://gicjewxbwgkabe:fa2facf2f623cb745b7f820404ce734853d13397f00c23e530f1f2d3b8d7a208@ec2-52-0-187-246.compute-1.amazonaws.com:5432/dbme6akn3pumit \
    SQLALCHEMY_DATABASE_URI_ASNC=postgres+asyncpg://gicjewxbwgkabe:fa2facf2f623cb745b7f820404ce734853d13397f00c23e530f1f2d3b8d7a208@ec2-52-0-187-246.compute-1.amazonaws.com:5432/dbme6akn3pumit \
    TEST_DATABASE_URI=sqlite:///test.db \
    FLASK_DEBUG=1 \ 
    PORT=8080

# Expõe a porta em que sua aplicação estará ouvindo
CMD ["sh", "-c", "echo PORT=$PORT && python -m flask run --host=0.0.0.0 --port=$PORT"]