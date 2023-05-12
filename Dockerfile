FROM python:3.10.4

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src

#Variáveis de ambiente.
ENV SECRET_KEY=dev \
    FLASK_ENV=development \
    FLASK_APP=src \
    SQLALCHEMY_DATABASE_URI=postgres://mpelsrzlxcmjzp:8a0130b05b865dd180d5bba8d6b54fbaba2e2886da2b6de127f4ee89bbab35fa@ec2-44-213-228-107.compute-1.amazonaws.com:5432/d2rhs4sdgd6ka7\
    TEST_DATABASE_URI=sqlite:///test.db \
    FLASK_DEBUG=1 \ 
    PORT=8080

# Expõe a porta em que sua aplicação estará ouvindo
CMD ["sh", "-c", "echo PORT=$PORT && python -m flask run --host=0.0.0.0 --port=$PORT"]