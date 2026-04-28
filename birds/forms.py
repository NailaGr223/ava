from django import forms
from .models import Bird

class BirdForm(forms.ModelForm):
    class Meta:
        model = Bird
        fields = ['title', 'listing_type', 'breed', 'age', 'gender', 
                  'health_status', 'location', 'price', 'quantity', 
                  'image', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }