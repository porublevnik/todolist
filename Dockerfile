FROM python:3.10-slim

WORKDIR = /opt/todolist

COPY requirements.txt .

RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN python3 -m pip install --no-cache -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
