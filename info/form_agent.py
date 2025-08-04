from django import forms
from .models_agent import PropertyVideo


from django.core.exceptions import ValidationError

class PropertyVideoForm(forms.ModelForm):
    class Meta:
        model = PropertyVideo
        fields = '__all__'
        exclude = ['agent']

    def clean_video(self):
        video = self.cleaned_data.get('video', False)
        if video:
            valid_mime_types = valid_mime_types = [
    'video/mp4',
    'video/mpeg',
    'video/quicktime',
    'video/x-msvideo',
    'video/x-matroska',
    'video/webm',
    'video/3gpp',
    'video/3gpp2',
    'video/ogg',
    'video/x-flv',
    'video/MP2T',
    'application/x-mpegURL',
    'video/avi',
    'video/x-ms-wmv',
    'video/x-ms-asf',
    'video/vnd.dlna.mpeg-tts'
]
            if video.content_type not in valid_mime_types:
                raise ValidationError('Unsupported file type. Please upload a video file (mp4, mov, avi).')
            if video.size > 200 * 1024 * 1024:  # 200MB Limit
                raise ValidationError('Please keep filesize under 200MB.')
            return video
        else:
            raise ValidationError("Couldn't read uploaded file.")

# class PropertyVideoForm(forms.ModelForm):
#     class Meta:
#         model = PropertyVideo
#         fields = [ 'city', 'area', 'price', #'price_max',
#             'property_type', 'properties','project_name', 'guideline_per_sqft',
#             'token_amount', 'property_size_sqft', 'rera', 'payment_condition',
#             'video',
#         ]
#         widgets = {
#             'property_type': forms.Select(choices=PropertyVideo._meta.get_field('property_type').choices),
#             'properties' : forms.Select(choices=PropertyVideo._meta.get_field('properties').choices),
#             'rera' : forms.Select(choices=PropertyVideo._meta.get_field('rera').choices)
#         }
