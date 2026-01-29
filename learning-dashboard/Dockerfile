# Use lightweight python image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install OS dependencies (needed for some python libs)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for docker cache)
COPY requirements.txt .

# Install python libs
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose streamlit default port
EXPOSE 8501

# Streamlit config to allow external access
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
