from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
import qrcode
from django.http import HttpResponse
from django.views import View
from rest_framework.authtoken.models import Token
from .models import Producer, Processor, ServiceProvider, ServiceRequest
from .serializers import ProducerSerializer, ProcessorSerializer, ServiceRequestSerializer, ServiceProviderSerializer

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 
    
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({'error': 'email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=email).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, password=password, first_name=username)

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        logout(request)
        return Response({'success': 'Logout successful'}, status=status.HTTP_200_OK)
    
class ProducerView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

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
        serializer = ProducerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
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
        producer = Producer.objects.get(user=request.user)
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

class ServiceRequestView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        if pk is not None:
            service_request = get_object_or_404(ServiceRequest, pk=pk)
            serializer = ServiceRequestSerializer(service_request)
            return Response({
                "success": True,
                "message": "Service Request details",
                "data": serializer.data
            })
        else:
            service_request = ServiceRequest.objects.all().filter(producer=request.user)
            serializer = ServiceRequestSerializer(service_request, many=True)
            return Response({
                "success": True,
                "message": "Service Requests",
                "data": serializer.data
            })

    def post(self, request, format=None):
        serializer = ServiceRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Service Request created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        service_request.delete()
        return Response({
            "success": True,
            "message": "Service Request deleted successfully",
            "data": None
        })
    
class ProcessorView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        if pk is not None:
            processor = get_object_or_404(Processor, pk=pk)
            serializer = ProcessorSerializer(processor)
            return Response({
                "success": True,
                "message": "Processor details",
                "data": serializer.data
            })
        else:
            processors = Processor.objects.all()
            serializer = ProcessorSerializer(processors, many=True)
            return Response({
                "success": True,
                "message": "Processors",
                "data": serializer.data
            })

    def post(self, request, format=None):
        serializer = ProcessorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Processor created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        processor = Processor.objects.get(user=request.user)
        serializer = ProcessorSerializer(processor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Processor updated successfully",
                "data": serializer.data
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        processor = get_object_or_404(Processor, pk=pk)
        processor.delete()
        return Response({
            "success": True,
            "message": "Processor deleted successfully",
            "data": None
        })
    
class ServiceProviderView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        if pk is not None:
            service_provider = get_object_or_404(ServiceProvider, pk=pk)
            serializer = ServiceProviderSerializer(service_provider)
            return Response({
                "success": True,
                "message": "Service Provider details",
                "data": serializer.data
            })
        else:
            service_provider = ServiceProvider.objects.all()
            serializer = ServiceProviderSerializer(service_provider, many=True)
            return Response({
                "success": True,
                "message": "Service Providers",
                "data": serializer.data
            })

    def post(self, request, format=None):
        serializer = ServiceProviderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Service Provider created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        service_provider = ServiceProvider.objects.get(user=request.user)
        serializer = ServiceProviderSerializer(service_provider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Service Provider updated successfully",
                "data": serializer.data
            })
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        service_provider = get_object_or_404(ServiceProvider, pk=pk)
        service_provider.delete()
        return Response({
            "success": True,
            "message": "Service Provider deleted successfully",
            "data": None
        })

class QRCodeView(View):
    def get(self, request, pk):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(pk)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response