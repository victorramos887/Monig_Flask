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
    SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432/monig
    TEST_DATABASE_URI=sqlite:///test.db \
    FLASK_DEBUG=1 \ 
    PORT=8080

# Expõe a porta em que sua aplicação estará ouvindo
CMD ["sh", "-c", "echo PORT=$PORT && python -m flask run --host=0.0.0.0 --port=$PORT"]