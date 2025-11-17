FROM python:3.10-slim

# Install system packages required for pandas, numpy, scipy
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    libatlas-base-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:$PORT"]
