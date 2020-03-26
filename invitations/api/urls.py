from django.conf.urls import url, include
from rest_framework import routers
from .views import InvitationViewSet

router = routers.DefaultRouter()
router.register(r'invitations', InvitationViewSet)

app_name = 'invitations'

urlpatterns = [
    url(r'^', include(router.urls)),
]
