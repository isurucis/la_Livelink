# views.py
from django.shortcuts import get_object_or_404, redirect, render
from .models import Link, Click
from django.contrib import messages
from .forms import BulkLinkCreationForm

def forward_link(request, short_code):
    link = get_object_or_404(Link, short_code=short_code)
    Click.objects.create(link=link)  # Track the click
    link.clicks += 1
    link.save()
    return redirect(link.get_full_url())  # Redirect instantly

def link_in_bio(request):
    links = Link.objects.filter(in_bio=True).order_by('-created_at')
    return render(request, "link_in_bio.html", {"links": links})

def bulk_link_creation_view(request):
    if request.method == 'POST':
        form = BulkLinkCreationForm(request.POST)
        if form.is_valid():
            # Process the form and create links
            category = form.cleaned_data['category']
            url = form.cleaned_data['url']
            campaign_name = form.cleaned_data['campaign_name']
            title = form.cleaned_data['title']
            channels = form.cleaned_data['channels']

            for channel in channels:
                source = channel.lower()
                medium = 'social' if channel in ['facebook', 'instagram'] else 'email'
                Link.objects.create(
                    category=category,
                    url=url,
                    short_code=generate_unique_shortcode(),  # You can implement this function
                    campaign_name=campaign_name,
                    title=title,
                    utm_source=source,
                    utm_medium=medium
                )
            messages.success(request, "Links created successfully!")
            return redirect('admin:app_name_link_changelist')  # Redirect to the Link changelist in admin
    else:
        form = BulkLinkCreationForm()
    return render(request, 'admin/bulk_link_creation.html', {'form': form})