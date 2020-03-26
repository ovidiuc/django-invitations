from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import InvitationSerializer
from ..models import Invitation


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    @action(detail=False, methods=['get', 'post'])
    def verify_invite(self, request):
        key = request.data['key'] if 'key' in request.data else None
        invitation = Invitation.verify_invitation(key)
        if(invitation is not None):
            serializer = InvitationSerializer(invitation)
            return Response(serializer.data)
        else:
            return Response({'detail': 'mot found'}, status=status.HTTP_410_GONE)
