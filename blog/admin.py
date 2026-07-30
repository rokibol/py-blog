from django.contrib import admin
from .models import Post

# আমাদের পোস্ট মডেলটিকে অ্যাডমিন প্যানেলে যুক্ত করে দিলাম
admin.site.register(Post)
