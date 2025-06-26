from django.contrib import admin
from .models import Software

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'team_size', 'platform', 'price')
    list_filter = ('industry', 'team_size', 'platform')
    search_fields = ('name', 'features', 'tags')