FROM public.ecr.aws/docker/library/python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    py3-pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./alianzas_bff ./alianzas_bff

EXPOSE 5000

CMD ["gunicorn", "-k", "gevent", "--bind", "0.0.0.0:5000", "alianzas_bff.api:app"]
