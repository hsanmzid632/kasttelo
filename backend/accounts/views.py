from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

User = get_user_model()

from rest_framework.response import Response
from rest_framework.views import APIView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Inscription réussie. Vous pouvez vous connecter immédiatement.'})
        else:
            return Response(serializer.errors, status=400)

class ActivateAccountView(APIView):
    pass  # Désactivé, plus d'activation par email
