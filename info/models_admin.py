from django.contrib import admin
from .models_agent import ContactLog

@admin.register(ContactLog)
class ContactLogAdmin(admin.ModelAdmin):
    list_display = ('contact_datetime', 'agent', 'user', 'video', 'contact_type')
    list_filter = ('contact_type', 'contact_datetime')
    search_fields = ('agent__user__username', 'user__username', 'video__city', 'video__area')
