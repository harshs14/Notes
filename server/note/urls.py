from django.urls import re_path
from . import views
from django.urls import include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'notes', views.NotesView)

urlpatterns = [
    re_path(r'', include(router.urls)),
]
