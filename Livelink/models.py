from django.db import models
from django.contrib.auth.models import User

class Link(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    clicks = models.PositiveIntegerField(default=0)
    show_in_bio = models.BooleanField(default=False)

    def get_full_url(self):
        if any([self.utm_source, self.utm_medium, self.utm_campaign]):
            utm_params = [
                f"utm_source={self.utm_source}" if self.utm_source else "",
                f"utm_medium={self.utm_medium}" if self.utm_medium else "",
                f"utm_campaign={self.utm_campaign}" if self.utm_campaign else ""
            ]
            return f"{self.original_url}?{'&'.join(filter(None, utm_params))}"
        return self.original_url
