FROM public.ecr.aws/docker/library/python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    curl \
    python3-dev \
    py3-pip && \
    wget -qO- https://raw.githubusercontent.com/eficode/wait-for/v2.2.3/wait-for > /usr/local/bin/wait-for && \
    chmod +x /usr/local/bin/wait-for

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./liquidaciones ./liquidaciones

EXPOSE 5000

CMD ["flask", "--app", "liquidaciones.api:init_app()", "run", "--host", "0.0.0.0"]
