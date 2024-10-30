# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
import string
import random

class LinkCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Link(models.Model):
    url = models.URLField()
    #short_code = models.SlugField(unique=True)
    short_code = models.CharField(max_length=10, unique=True, blank=True, editable=True)
    title = models.CharField(max_length=255)  
    category = models.ForeignKey(LinkCategory, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    utm_enabled = models.BooleanField(default=False)
    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)
    utm_term = models.CharField(max_length=100, blank=True, null=True)
    utm_content = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    clicks = models.PositiveIntegerField(default=0)
    in_bio = models.BooleanField(default=False)

    def generate_unique_short_code(self):
        length = 6  # or any preferred length
        charset = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(charset) for _ in range(length))
            if not Link.objects.filter(short_code=short_code).exists():
                return short_code
            
    def get_full_url(self):
        """Return URL with UTM parameters if enabled."""
        if self.utm_enabled:
            utm_params = {
                "utm_source": self.utm_source,
                "utm_medium": self.utm_medium,
                "utm_campaign": self.utm_campaign,
                "utm_term": self.utm_term,
                "utm_content": self.utm_content,
            }
            query_string = "&".join([f"{k}={v}" for k, v in utm_params.items() if v])
            return f"{self.url}?{query_string}"
        return self.url

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_unique_short_code()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.short_code} - {self.url}"

class Click(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Click on {self.link.short_code} at {self.timestamp}"
