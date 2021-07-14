from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, User
from .serializers import ProductSerialier
from .producer import publish
import random

class ProductViewSet(viewsets.ViewSet):
  def list(self, request):
    products = Product.objects.all()
    serializer = ProductSerialier(products, many=True)
    return Response(serializer.data)

  def create(self, request):
    serializer = ProductSerialier(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    publish('product_created', serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def retrieve(self, request, pk=None):
    product = Product.objects.get(id=pk)
    serializer = ProductSerialier(product)
    return Response(serializer.data)

  def update(self, request, pk=None):
    product = Product.objects.get(id=pk)
    serializer = ProductSerialier(instance=product, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    publish('product_updated', serializer.data)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

  def destroy(self, request, pk=None):
    product = Product.objects.get(id=pk)
    product.delete()
    publish('product_deleted', pk)
    return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
  # def create(self, request):
  #   user = User(id=5)
  #   user.save()
  #   return Response(status=status.HTTP_201_CREATED)

  def get(self, _):
    users = User.objects.all()
    user = random.choice(users)
    return Response({
      'id': user.id
    })