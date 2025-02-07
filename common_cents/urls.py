from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("webapp.urls")),
    path("calculators/mortgage/", include("mortgage_calculator.urls")),
]
