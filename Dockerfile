# 1. Pin a specific Python version for reproducibility
FROM python:3.10-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Set working directory
WORKDIR /app

# 4. Install system dependencies, Google Cloud CLI, and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    apt-transport-https \
    ca-certificates \
    gnupg \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" > /etc/apt/sources.list.d/google-cloud-sdk.list \
    && apt-get update \
    && apt-get install -y google-cloud-cli \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. COPY DEPENDENCIES FIRST (To leverage Docker cache)
# Assuming you have a setup.py or requirements.txt
COPY setup.py . 
# If using requirements.txt, add: COPY requirements.txt .

# 6. Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .
# If using requirements.txt, replace above with: pip install --no-cache-dir -r requirements.txt

# 7. NOW copy the rest of the application code and PRE-TRAINED model
COPY . .

# 8. Expose the Flask port
EXPOSE 5000

# 9. Run the application
CMD ["python", "application.py"]