from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveAPIView
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password, check_password


class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(TokenObtainPairView):
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Profile(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        username = self.kwargs['username']
        return User.objects.get(username=username)

    def get(self, request, *args, **kwargs):
        if request.user.username != kwargs['username']:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        return super().get(request, *args, **kwargs)


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class Update(APIView):
    def put(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    def put(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not request.user.check_password(old_password):
            return Response({'error': '잘못된 이전 비밀번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if old_password == new_password:
            return Response({'error': '새로운 비밀번호는 이전 비밀번호와 같을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(make_password(new_password))
        request.user.save()
        return Response({'message': '비밀번호 변경 완료.'}, status=status.HTTP_200_OK)


class Delete(APIView):
    def delete(self, request):
        password = request.data.get('password')
        if not password:
            return Response({'error': '비밀번호를 입력하세요'}, status=status.HTTP_400_BAD_REQUEST)
        if not check_password(password, request.user.password):
            return Response({'error': '비밀번호가 틀렸습니다'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.delete()
        return Response({'message': '계정이 삭제되었습니다'}, status=status.HTTP_204_NO_CONTENT)
