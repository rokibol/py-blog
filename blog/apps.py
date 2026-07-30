from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    # সার্ভার বুট হওয়ার সময় সিগন্যাল ফাইলটি লোড করার পাইথনিক নিয়ম
    def ready(self):
        import blog.signals