from rest_framework.serializers import (
    ModelSerializer,
)
from ..models import Invitation


class InvitationSerializer(ModelSerializer):
    class Meta:
        model = Invitation
        fields = ('id', 'key', 'email',)
