from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from order.serializer import OrderSerializer


class OrderView(ModelViewSet):
    @action(detail=True, methods=["post"])
    def product(self, request, pk):
        """For adding products in particular category."""
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product_id=pk, user=request.user)
        return Response(serializer.data)
