from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Producer
from .serializers import ProducerSerializer

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 
    
class ProducerView(APIView):
    # authentication_classes = [CsrfExemptSessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        if pk is not None:
            producer = get_object_or_404(Producer, pk=pk)
            serializer = ProducerSerializer(producer)
            return Response({
                "success": True,
                "message": "Producer details",
                "data": serializer.data
            })
        else:
            producers = Producer.objects.all()
            serializer = ProducerSerializer(producers, many=True)
            return Response({
                "success": True,
                "message": "Produceres",
                "data": serializer.data
            })

    def post(self, request, format=None):
        serializer = ProducerSerializer(data=request.data)
        if serializer.is_valid():
            producer = serializer.save()
            return Response({
                "success": True,
                "message": "Producer created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        producer = get_object_or_404(Producer, pk=pk)
        serializer = ProducerSerializer(producer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Producer updated successfully",
                "data": serializer.data
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        producer = get_object_or_404(Producer, pk=pk)
        producer.delete()
        return Response({
            "success": True,
            "message": "Producer deleted successfully",
            "data": None
        })
