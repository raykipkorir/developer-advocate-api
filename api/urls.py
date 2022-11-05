from django.urls import path

from . import views

urlpatterns = [

    path("advocates/", views.AdvocateListCreate.as_view(), name="advocates"),
    path("advocates/<str:username>/", views.AdvocateDetail.as_view(), name="advocate-detail"),

    path("companies/", views.CompanyList.as_view(), name="companies"),
    path("companies/<str:username>/", views.CompanyDetail.as_view(), name="company-detail"),
]
