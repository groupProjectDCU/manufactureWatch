FROM python:3.11-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

ENV DJANGO_SETTINGS_MODULE=manufactureWatch.settings

EXPOSE 8000

ENTRYPOINT ["bash", "./entrypoint.sh"]