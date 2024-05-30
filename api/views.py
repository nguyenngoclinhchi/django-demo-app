from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import Product
from .serializers import ProductSerializer
from rest_framework import status


class ProductCategoryApiView(APIView):
    # set in settings DEFAULT_RENDERER_CLASSES to JSON
    def get(self, request, category_id, format='json'):
        # ?order=price&limit=10
        limit = int(request.query_params.get(
            "limit")) if int(request.query_params.get("limit", 0)) > 0 else 12
        order = request.query_params.get("order") if request.query_params.get(
            "order") == "price" else "-price"
        items_product = Product.objects.filter(
            category=category_id, status="published").order_by(order+"_real")[:limit]
        items_product = ProductSerializer(items_product, many=True)
        for item in items_product.data:
            item['link'] = f"{item['slug']}-a{item['id']}.html"
        return Response(items_product.data)


class ProductRelatedApiView(APIView):
    # set in settings DEFAULT_RENDERER_CLASSES to JSON
    def get(self, request, product_id, format='json'):
        try:
            product = Product.objects.get(id=product_id, status="published")
            # ?order=price&limit=10
            limit = int(request.query_params.get(
                "limit")) if int(request.query_params.get("limit", 0)) > 0 else 10
            order = request.query_params.get("order") if request.query_params.get(
                "order") == "price" else "-price"
            items_product = Product.objects.filter(
                category=product.category, status="published").exclude(id=product_id).order_by(order+"_real")[:limit]
            items_product = ProductSerializer(items_product, many=True)
            for item in items_product.data:
                item['link'] = f"{item['slug']}-a{item['id']}.html"
            return Response(items_product.data)

        except Product.DoesNotExist:
            return Response({'error': "Product not found"}, status=status.HTTP_404_NOT_FOUND)
