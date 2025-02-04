# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Print Chrome version for debugging
RUN google-chrome --version

# Install ChromeDriver using webdriver_manager (handled by your script)
# No need to manually install ChromeDriver here
# Download and install ChromeDriver
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.159/linux64/chromedriver-linux64.zip" \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip chromedriver-linux64

# After moving chromedriver to /usr/local/bin
RUN ls -l /usr/local/bin/chromedriver && chromedriver --version

# Install Python dependencies
RUN pip install --no-cache-dir packaging

# Copy the requirements file and install Python dependencies
ENV PATH="/usr/local/bin:${PATH}"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the command to run your Selenium bot
CMD ["python", "main.py"]
