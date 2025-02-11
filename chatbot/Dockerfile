FROM python:3.10

WORKDIR /app

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ../custom_logic custom_logic

# ✅ Set PYTHONPATH so Python recognizes custom_logic as a module
ENV PYTHONPATH="/app"

# Expose chatbot API port
EXPOSE ${TTYD_API_PORT}

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
