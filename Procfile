#web: flask run --host 0.0.0.0 --port $PORT --no-reload --managed=False
# web: gunicorn src:__init__.py --no-cython
web: gunicorn -w 4 -k gevent app:app --managed=False