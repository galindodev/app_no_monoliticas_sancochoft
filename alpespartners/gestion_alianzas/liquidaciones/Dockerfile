FROM public.ecr.aws/docker/library/python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    py3-pip && \
    wget -qO- https://raw.githubusercontent.com/eficode/wait-for/v2.2.3/wait-for > /usr/local/bin/wait-for

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["/wait-for", "db_liquidaciones:5432", "--", "gunicorn", "-k", "gevent", "--bind", "0.0.0.0:5000", "src.api:app"]
