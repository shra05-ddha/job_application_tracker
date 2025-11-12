from django.contrib import admin
from .models import Company, JobApplication

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "website")

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "status", "applied_on", "follow_up_on", "user")
    list_filter = ("status", "company")
    search_fields = ("title", "company__name")
