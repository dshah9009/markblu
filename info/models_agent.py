from django.db import models
from django.contrib.auth.models import User

def agent_logo_upload_path(instance, filename):
    return f"agent_logo/{instance.user.username}/{filename}"

class AgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)
    company_name = models.CharField(max_length= 100)
    office_address = models.TextField()
    project_location = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to=agent_logo_upload_path,blank = True, null = True)
    company_rera_id = models.CharField(max_length=50, blank= True, null = True)

    def __str__(self):
        return self.user.username
    
PROPERTY_TYPES = [
    ('Buy', 'Buy'),
    ('Rent', 'Rent'),
]
PROPERTIES = [
    ('Plot','Plot'),
    ('1BHK','1BHK'),
    ('2BHK','2BHK'),
    ('3BHK','3BHK'),
    ('4BHK','4BHK'),
    
]

class PropertyVideo(models.Model):
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=150)
    price = models.IntegerField()
    #price_max = models.IntegerField()
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    properties = models.CharField(max_length=10 , choices=PROPERTIES)
    market_price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2)
    token_amount = models.DecimalField(max_digits=10, decimal_places=2)
    property_size_sqft = models.DecimalField(max_digits=10, decimal_places=2)
    video = models.FileField(upload_to='property_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.city} - {self.area} - {self.property_type}"


