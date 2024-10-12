from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer

# Create your views here.
class UserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()
    
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = User.objects.get(pk=self.request.user.id)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass