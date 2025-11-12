from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from .models import JobApplication
from .forms import JobApplicationForm, CompanyForm
from .filters import JobApplicationFilter

class LoginViewCustom(LoginView):
    template_name = "app/login.html"

@login_required
def dashboard(request):
    qs = JobApplication.objects.filter(user=request.user)
    app_filter = JobApplicationFilter(request.GET, queryset=qs)
    return render(request, "app/dashboard.html", {
        "filter": app_filter,
        "applications": app_filter.qs,
    })

@login_required
def application_create(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Application saved.")
            return redirect("dashboard")
    else:
        form = JobApplicationForm()
    return render(request, "app/application_form.html", {"form": form, "action": "Create"})

@login_required
def application_edit(request, pk):
    obj = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Application updated.")
            return redirect("application_detail", pk=obj.pk)
    else:
        form = JobApplicationForm(instance=obj)
    return render(request, "app/application_form.html", {"form": form, "action": "Edit"})

@login_required
def application_detail(request, pk):
    obj = get_object_or_404(JobApplication, pk=pk, user=request.user)
    return render(request, "app/application_detail.html", {"app": obj})

@login_required
def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Company added.")
            return redirect("application_create")
    else:
        form = CompanyForm()
    return render(request, "app/application_form.html", {"form": form, "action": "Add Company"})

def logout_view(request):
    logout(request)
    return redirect("login")
