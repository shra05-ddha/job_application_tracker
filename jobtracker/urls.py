from django.contrib import admin
from django.urls import path, include
from app.views import LoginViewCustom, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),
    path("login/", LoginViewCustom.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]
