# ১. পাইথনের অফিশিয়াল লাইটওয়েট ইমেজ ব্যবহার করা
FROM python:3.12-slim

# ২. ডকারের ভেতরে একটি কাজের ফোল্ডার সেট করা
WORKDIR /app

# ৩. সিস্টেমের কিছু প্রয়োজনীয় ডিপেন্ডেন্সি ইনস্টল করা
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ৪. রিকোয়ারমেন্ট ফাইল কপি করে প্যাকেজ ইনস্টল করা
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. প্রজেক্টের সব কোড ডকারের ভেতর কপি করা
COPY . .

# ৬. জ্যাঙ্গো পোর্ট এক্সপোজ করা
EXPOSE 8002

# 7. ডকার চালু হলে জ্যাঙ্গো সার্ভার রান করার কমান্ড
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]