FROM python:3.7

ARG RECAPTCHA_SECRET_KEY
ARG RECAPTCHA_SITE_KEY
ARG SENDGRID_API_KEY

ENV RECAPTCHA_SECRET_KEY=$RECAPTCHA_SECRET_KEY
ENV RECAPTCHA_SITE_KEY=$RECAPTCHA_SITE_KEY
ENV SENDGRID_API_KEY=$SENDGRID_API_KEY

WORKDIR /app

COPY ./ .

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

# RUN "python -m pytest"

EXPOSE 5001

CMD ["python", "server.py"]