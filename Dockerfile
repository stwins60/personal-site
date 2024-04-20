FROM python:3.7

WORKDIR /app

COPY ./ .

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 5001

CMD ["python", "server.py"]