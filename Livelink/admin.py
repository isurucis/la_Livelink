# Livelink/admin.py
from django.contrib import admin
from .models import Link, LinkCategory, Click
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.utils.http import urlencode
import random
import string

class BulkLinkCreationForm(forms.Form):
    category = forms.ModelChoiceField(queryset=LinkCategory.objects.all(), required=True)
    url = forms.URLField(required=True)
    campaign_name = forms.CharField(max_length=255, required=True)
    title = forms.CharField(max_length=255, required=True)
    channels = forms.MultipleChoiceField(
        choices=[
            ('email', 'Email'),
            ('facebook', 'Facebook'),
            ('instagram', 'Instagram'),
            ('youtube', 'YouTube')
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

def generate_unique_short_code():
    while True:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if not Link.objects.filter(short_code=short_code).exists():
            return short_code

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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk_create/', self.admin_site.admin_view(self.bulk_create_view), name='bulk_create')
        ]
        return custom_urls + urls

    def bulk_create_view(self, request):
        if request.method == 'POST':
            form = BulkLinkCreationForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data['category']
                url = form.cleaned_data['url']
                campaign_name = form.cleaned_data['campaign_name']
                title = form.cleaned_data['title']
                channels = form.cleaned_data['channels']
                
                # Generate and save links for each selected channel
                for channel in channels:
                    short_code = generate_unique_short_code()
                    utm_params = {
                        'utm_source': channel,
                        'utm_medium': 'social' if channel != 'email' else 'email',
                        'utm_campaign': campaign_name
                    }
                    full_url = f"{url}?{urlencode(utm_params)}"
                    Link.objects.create(
                        category=category,
                        url=full_url,
                        short_code=short_code,
                        title=title,
                        utm_enabled=True,
                        created_by=request.user
                    )
                self.message_user(request, f"Successfully created links for {len(channels)} channels.")
                return redirect('admin:Livelink_link_changelist')
        else:
            form = BulkLinkCreationForm()
        
        return render(request, 'admin/bulk_create_links.html', {'form': form})

    
# Registering the models with the admin site
admin.site.register(Link, LinkAdmin, BulkLinkCreationForm)
admin.site.register(LinkCategory)
admin.site.register(Click)
admin.site.site_header = "LiveLink Admin"
admin.site.site_title = "Live Link"
admin.site.index_title = "Livelink"