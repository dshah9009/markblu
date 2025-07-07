from django import forms
from .models_agent import PropertyVideo

class PropertyVideoForm(forms.ModelForm):
    class Meta:
        model = PropertyVideo
        fields = [ 'city', 'area', 'price', #'price_max',
            'property_type', 'properties', 'guideline_per_sqft',
            'token_amount', 'property_size_sqft', 'rera', 'payment_condition',
            'video',
        ]
        widgets = {
            'property_type': forms.Select(choices=PropertyVideo._meta.get_field('property_type').choices),
            'properties' : forms.Select(choices=PropertyVideo._meta.get_field('properties').choices),
            'rera' : forms.Select(choices=PropertyVideo._meta.get_field('rera').choices)
        }
