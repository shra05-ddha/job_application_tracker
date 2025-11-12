from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("assessment", "Assessment"),
        ("interview", "Interview"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
        ("ghosted", "No Response"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    job_url = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    applied_on = models.DateField()
    follow_up_on = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_on", "-created_at"]

    def __str__(self):
        return f"{self.title} @ {self.company}"
