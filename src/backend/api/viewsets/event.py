from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from api.models import Event
from api.serializers.event import EventSerializer


@extend_schema(tags=['Event'])
class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()