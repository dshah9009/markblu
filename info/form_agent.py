from django import forms
from .models_agent import PropertyVideo

class PropertyVideoForm(forms.ModelForm):
    class Meta:
        model = PropertyVideo
        fields = [ 'city', 'area', 'price_min', 'price_max',
            'property_type', 'market_price_per_sqft',
            'token_amount', 'property_size_sqft',
            'video',
        ]
        widgets = {
            'property_type': forms.Select(choices=PropertyVideo._meta.get_field('property_type').choices)
        }
