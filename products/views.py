from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Product
from .serializers import ProductSerializer


class ProductView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        request.data['author'] = request.user.id
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        product = Product.objects.get(id=pk)
        if request.user != product.author:
            return Response({"message": "제품을 수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        product = Product.objects.get(id=pk)
        if request.user != product.author:
            return Response({"message": "제품을 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
