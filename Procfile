web: gunicorn wsgi --log-file -

worker: python chesswithkate/manage.py rqworker high default low
