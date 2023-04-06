FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ .

RUN python3 manage.py migrate

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]