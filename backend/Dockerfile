FROM python:3.9

WORKDIR /code

# Update package lists and install netcat-traditional
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./assets ./assets
COPY alembic.ini .
COPY ./alembic ./alembic
COPY docker-entrypoint.sh .

# Make the entrypoint shell script executable
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
