FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ফাস্টএপিআই এর জন্য ৮০০3 পোর্ট এক্সপোজ করা
EXPOSE 8003

# ডকার চালু হলে উডিকর্ন দিয়ে ফাস্টএপিআই রান করার কমান্ড
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8003"]
