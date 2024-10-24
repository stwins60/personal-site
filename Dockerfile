# Stage 1: Build stage
FROM python:3.13.0b2 AS build

ARG RECAPTCHA_SECRET_KEY
ARG RECAPTCHA_SITE_KEY
ARG SENDGRID_API_KEY

ENV RECAPTCHA_SECRET_KEY=$RECAPTCHA_SECRET_KEY
ENV RECAPTCHA_SITE_KEY=$RECAPTCHA_SITE_KEY
ENV SENDGRID_API_KEY=$SENDGRID_API_KEY

WORKDIR /app

COPY ./requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Stage 2: Production stage
FROM python:3.13-slim

ARG RECAPTCHA_SECRET_KEY
ARG RECAPTCHA_SITE_KEY
ARG SENDGRID_API_KEY

ENV RECAPTCHA_SECRET_KEY=$RECAPTCHA_SECRET_KEY
ENV RECAPTCHA_SITE_KEY=$RECAPTCHA_SITE_KEY
ENV SENDGRID_API_KEY=$SENDGRID_API_KEY

WORKDIR /app

# Copy only necessary files from build stage
COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY . . 

# Expose the application port
EXPOSE 5001

# Command to run the application
CMD ["python", "run.py"]
