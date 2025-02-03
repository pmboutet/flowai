FROM python:3.11.8

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "flowai.wsgi:application"]