from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from api.models import User
from api.serializers.user import UserSerializer


@extend_schema(tags=['User'])
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['get'], url_path='by_chat_id/(?P<chat_id>[^/.]+)')
    def get_product_by_category(self, request, chat_id=None):
        user = self.queryset.filter(chat_id=chat_id).first()
        serializer = self.serializer_class(user, many=False)
        return Response(serializer.data)