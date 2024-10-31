# Livelink/admin.py
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin
from .models import Link, LinkCategory, Click
from .forms import BulkLinkCreationForm

class LinkAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'url', 'category', 'created_by', 'clicks', 'utm_enabled', 'in_bio')
    search_fields = ('short_code', 'url', 'category__name', 'created_by__username')
    list_filter = ('utm_enabled', 'in_bio', 'category')
    readonly_fields = ('clicks', 'created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        # Make short_code readonly when editing an existing object
        if obj:  # When editing (obj is not None)
            return self.readonly_fields + ('short_code',)
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by during the first save
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def bulk_link_creation_button(self, request):
        url = reverse('bulk_link_creation')
        return format_html(f'<a class="button" href="{url}">Bulk Create Links</a>')

    bulk_link_creation_button.short_description = 'Bulk Link Creation'
    bulk_link_creation_button.allow_tags = True
    
    change_list_template = 'admin/link_changelist.html'




# Registering the models with the admin site
admin.site.register(Link, LinkAdmin)
admin.site.register(LinkCategory)
admin.site.register(Click)
admin.site.site_header = "LiveLink Admin"
admin.site.site_title = "Live Link"
admin.site.index_title = "Livelink"