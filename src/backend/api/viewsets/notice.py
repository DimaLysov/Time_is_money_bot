from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from api.models import Notice
from api.serializers.notice import NoticeSerializer


@extend_schema(tags=['Notice'])
class NoticeViewSet(ModelViewSet):
    serializer_class = NoticeSerializer
    queryset = Notice.objects.all()