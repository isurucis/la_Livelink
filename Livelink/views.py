# views.py
from django.shortcuts import get_object_or_404, redirect, render
from .models import Link, Click

def forward_link(request, short_code):
    link = get_object_or_404(Link, short_code=short_code)
    Click.objects.create(link=link)  # Track the click
    link.clicks += 1
    link.save()
    return redirect(link.get_full_url())  # Redirect instantly

def link_in_bio(request):
    links = Link.objects.filter(in_bio=True).order_by('-created_at')
    return render(request, "link_in_bio.html", {"links": links})
