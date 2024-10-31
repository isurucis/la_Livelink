from django import forms
from .models import Link, LinkCategory

class BulkLinkCreationForm(forms.Form):
    category = forms.ModelChoiceField(queryset=LinkCategory.objects.all(), required=True)
    url = forms.URLField(required=True)
    campaign_name = forms.CharField(required=True)
    title = forms.CharField(required=True)
    channels = forms.MultipleChoiceField(
        choices=[('email', 'Email'), ('facebook', 'Facebook'), ('instagram', 'Instagram'), ('youtube', 'YouTube')],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )