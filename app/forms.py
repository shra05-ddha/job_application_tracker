from django import forms
from .models import JobApplication, Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "website"]

class JobApplicationForm(forms.ModelForm):
    follow_up_on = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    applied_on = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = JobApplication
        fields = [
            "title", "company", "job_url", "location", "salary",
            "status", "applied_on", "follow_up_on", "notes"
        ]
