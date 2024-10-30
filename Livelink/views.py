from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Link
from django.contrib.auth.decorators import login_required
import random
import string

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@login_required
def create_link(request):
    if request.method == 'POST':
        original_url = request.POST['original_url']
        utm_source = request.POST.get('utm_source')
        utm_medium = request.POST.get('utm_medium')
        utm_campaign = request.POST.get('utm_campaign')
        category = request.POST.get('category')
        show_in_bio = request.POST.get('show_in_bio') == 'on'
        
        short_code = generate_short_code()
        link = Link.objects.create(
            original_url=original_url,
            short_code=short_code,
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            category=category,
            creator=request.user,
            show_in_bio=show_in_bio
        )
        return HttpResponse(f"Short URL created: /{short_code}")
    return render(request, 'create_link.html')

def redirect_link(request, short_code):
    link = get_object_or_404(Link, short_code=short_code, is_deleted=False)
    link.clicks += 1
    link.save()
    return redirect(link.get_full_url())

@login_required
def edit_link(request, short_code):
    link = get_object_or_404(Link, short_code=short_code, creator=request.user)
    if request.method == 'POST':
        link.original_url = request.POST['original_url']
        link.utm_source = request.POST.get('utm_source')
        link.utm_medium = request.POST.get('utm_medium')
        link.utm_campaign = request.POST.get('utm_campaign')
        link.category = request.POST.get('category')
        link.show_in_bio = request.POST.get('show_in_bio') == 'on'
        link.save()
        return HttpResponse("Link updated successfully")
    return render(request, 'edit_link.html', {'link': link})

@login_required
def delete_link(request, short_code):
    link = get_object_or_404(Link, short_code=short_code, creator=request.user)
    link.is_deleted = True
    link.save()
    return HttpResponse("Link deleted successfully")

def link_in_bio(request):
    links = Link.objects.filter(show_in_bio=True, is_deleted=False)
    return render(request, 'link_in_bio.html', {'links': links})
