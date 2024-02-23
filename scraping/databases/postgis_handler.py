import psycopg2
import os
import sys
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# from config import settings

class PostgisHandler:
  def __init__(self):
    # self.connection_params = {
    #   'host': settings.DB_HOST,
    #   'port': settings.DB_PORT,
    #   'database': settings.DB_NAME,
    #   'user': settings.DB_USER,
    #   'password': settings.DB_PASSWORD,
    # }

    print(os.environ.get('POSTGRES_ENDPOINT'))
    self.connection_params = {
      'host': os.environ.get('POSTGRES_ENDPOINT'),
      'port': os.environ.get('PORT_POSTGRES'),
      'database': os.environ.get('POSTGRES_DATABASE'),
      'user': os.environ.get('POSTGRES_USER'),
      'password': os.environ.get('POSTGRES_PASSWORD'),
    }

  def __enter__(self):
    try:
      self.conn = psycopg2.connect(**self.connection_params)
      return self
    except psycopg2.Error as e:
      print(f"Error connecting to the database: {e}")
      raise

  def __exit__(self, exc_type, exc_value, traceback):
    try:
      self.conn.close()
    except psycopg2.Error as e:
      print(f"Error closing the database connection: {e}")

  def insert(self, query, params=None):
    try:
      with self.conn.cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchone()

      self.conn.commit()

      if result:
        return result[0]
    except psycopg2.Error as e:
      print(f"Error executing INSERT query: {e}")
      raise

  def select(self, query, params=None):
    try:
      with self.conn.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()
    except psycopg2.Error as e:
      print(f"Error executing SELECT query: {e}")
      raise

  def alter_table(self, query, params=None):
    try:
      with self.conn.cursor() as cursor:
        cursor.execute(query, params)
      
      self.conn.commit()
    except psycopg2.Error as e:
      print(f"Error executing ALTER TABLE query: {e}")
      raise