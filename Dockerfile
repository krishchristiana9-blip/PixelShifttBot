FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code and video file
COPY bot.py .
# Optional: Copy video file as fallback
COPY promo.mp4 ./ || echo "No video file found"

# Command to run the bot
CMD ["python", "bot.py"]
