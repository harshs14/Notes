from django.urls import re_path
from . import views
from django.urls import include
from rest_framework.routers import DefaultRouter
from server.settings import STATIC_ROOT, STATIC_URL
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'notes', views.NotesView)

urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'^signup/$', views.UserSignupView.as_view(), name='signup'),
    re_path(r'^verify/(?P<userId>[0-9]+)/$', views.UserVerificationView.as_view(), name='verify'),
    re_path(r'^resend/(?P<userId>[0-9]+)/$', views.ResendOtpView.as_view(), name='resend'),
    re_path(r'^login/$', views.UserLoginView.as_view(), name='login'),
]
urlpatterns += static(STATIC_URL,document_root=STATIC_ROOT)
