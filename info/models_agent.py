from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField


def agent_logo_upload_path(instance, filename):
    return f"agent_logo/{instance.user.username}/{filename}"

DEAL = [
    ('All','All'),
    ('Plot','Plot'),
    ('Flat','Flat'),
    ('Raw House','Row House'),
    
]
class DealType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class AgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)
    company_name = models.CharField(max_length= 100, blank= True, null = True)
    office_address = models.TextField()
    project_location = models.CharField(max_length=100)
    experience = models.IntegerField()
    deal = models.ManyToManyField(DealType)
    company_logo = models.ImageField(upload_to=agent_logo_upload_path,blank = True, null = True)
    company_rera_id = models.CharField(max_length=50, blank= True, null = True)
    role = models.CharField( max_length= 10, default= 'Agent')

    def __str__(self):
        return self.user.username
    
PROPERTY_TYPES = [
    ('Buy', 'Buy'),
    ('Rent', 'Rent'),
]
PROPERTIES = [
    ('Plots & Houses', [
        ('Plot', 'Plot'),
        ('Raw House', 'Raw House'),
    ]),
    ('Residential', [
        ('1BHK', '1BHK'),
        ('2BHK', '2BHK'),
        ('3BHK', '3BHK'),
        ('4BHK', '4BHK'),
    ]),
    ('Commercial', [
        ('Office', 'Office'),
        ('Shop', 'Shop'),
        ('Showroom', 'Showroom'),
    ]),
]
rera_approval = [
    ('Approved', 'Approved'),
    ('Pending', 'Pending'),
]

class PropertyVideo(models.Model):
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=150)
    price = models.IntegerField()
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    properties = models.CharField(max_length=10 , choices=PROPERTIES)
    project_name = models.CharField(max_length=100, blank=True, null=True)
    guideline_per_sqft = models.IntegerField()
    token_amount = models.DecimalField(max_digits=10, decimal_places=2)
    property_size_sqft = models.IntegerField()
    rera = models.CharField(max_length=10, choices=rera_approval, blank=True, null=True)
    payment_condition = models.CharField(max_length=150, blank=True, null=True)
    video = models.FileField(upload_to='property_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.city} - {self.area} - {self.property_type}"

class ContactLog(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('WhatsApp', 'WhatsApp'),
        ('Call', 'Call'),
    ]
    agent = models.ForeignKey('AgentProfile', on_delete=models.CASCADE)
    agent_mobile = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user_mobile = models.CharField(max_length=15, blank=True, null=True)
    video = models.ForeignKey('PropertyVideo', on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=10, choices=CONTACT_TYPE_CHOICES)
    contact_datetime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} ➔ {self.agent} ({self.contact_type})"

