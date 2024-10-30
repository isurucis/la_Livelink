# Livelink/admin.py
from django.contrib import admin
from .models import Link, LinkCategory, Click

class LinkAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'url', 'category', 'created_by', 'clicks', 'utm_enabled', 'in_bio')
    search_fields = ('short_code', 'url', 'category__name', 'created_by__username')
    list_filter = ('utm_enabled', 'in_bio', 'category')
    readonly_fields = ('clicks', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by during the first save
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Registering the models with the admin site
admin.site.register(Link, LinkAdmin)
admin.site.register(LinkCategory)
admin.site.register(Click)
admin.site.site_header = "LiveLink"
admin.site.site_title = "Live Link"
admin.site.index_title = "Livelink"