from django.urls import path

from . import views

urlpatterns = [
    path("contents/", views.ContentView.as_view()),
    path("contents/<int:content_id>/", views.ContentDetailView.as_view()),
    path("contents/filter/", views.ContentTitleView.as_view())
]
