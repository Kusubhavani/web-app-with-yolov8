FROM python:3.9-slim

# Install system dependencies - fixed for Debian
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY api/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the model download script
COPY scripts/download_model.sh /usr/local/bin/download_model.sh
RUN chmod +x /usr/local/bin/download_model.sh && \
    mkdir -p /app/models /app/output

# Copy the API source code
COPY api/main.py .

# Create entrypoint script
RUN echo '#!/bin/bash\nset -e\ndownload_model.sh\nexec uvicorn main:app --host 0.0.0.0 --port 8000' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]