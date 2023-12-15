from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
import qrcode
from django.http import HttpResponse
from django.views import View
from rest_framework.authtoken.models import Token
from .models import Producer, Processor, ServiceProvider, ServiceRequest, Batch, Store
from .serializers import ProducerSerializer, ProcessorSerializer, ServiceRequestSerializer, ServiceProviderSerializer, BatchSerializer, StoreSerializer, StoreDetailSerializer

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 
    
class RegisterView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({'error': 'email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=email).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, password=password, first_name=username)
        login(request, user)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class IsLoginView(APIView):
    def get(self, request):
        if request.user:
            return Response({
                "success": True,
                "message": "Loggedin"
            })
        else:
            return Response({
                "success": False,
                "message": "Not Loggedin"
            })
        
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

class QRCodeView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

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
    
    def post(self, request, format=None):
        qr_code=request.data.get('qr_code')
        if qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_code)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            response = HttpResponse(content_type="image/png")
            img.save(response, "PNG")
            return response
        else:
            return Response({
                "success": False,
                "errors": "qr_code is required"
            }, status=status.HTTP_400_BAD_REQUEST)
    
class BatchView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        if pk is not None:
            batch = get_object_or_404(Batch, pk=pk)
            serializer = BatchSerializer(batch)
            return Response({
                "success": True,
                "message": "Batch details",
                "data": serializer.data
            })
        else:
            batches = Batch.objects.all()
            serializer = BatchSerializer(batches, many=True)
            return Response({
                "success": True,
                "message": "Batches",
                "data": serializer.data
            })

    def post(self, request, format=None):
        serializer = BatchSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            batch = serializer.save()
            return Response({
                "success": True,
                "message": "Batch created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        batch = Batch.objects.get(pk=pk)
        serializer = BatchSerializer(batch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Batch updated successfully",
                "data": serializer.data
            })
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        batch = get_object_or_404(Batch, pk=pk)
        batch.delete()
        return Response({
            "success": True,
            "message": "Batch deleted successfully",
            "data": None
        })
    
class BatchSearchView(generics.ListAPIView):
    serializer_class = BatchSerializer
    def get_queryset(self):
        batch_type = self.request.query_params.get('type', None)
        location = self.request.query_params.get('location', None)
        producer = Producer.objects.get(user=self.request.user)
        queryset = Batch.objects.filter(producer=producer)
        if batch_type:
            queryset = queryset.filter(type__icontains=batch_type)
        if location:
            queryset = queryset.filter(current_location__icontains=location)
        return queryset
    
class StoreView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        if pk is not None:
            store = get_object_or_404(Store, pk=pk)
            serializer = StoreDetailSerializer(store)
            return Response({
                "success": True,
                "message": "Store details",
                "data": serializer.data
            })
        else:
            stores = Store.objects.all()
            serializer = StoreDetailSerializer(stores, many=True)
            return Response({
                "success": True,
                "message": "Stores",
                "data": serializer.data
            })

    def post(self, request, format=None):
        serializer = StoreSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            store = serializer.save()
            return Response({
                "success": True,
                "message": "Store created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        store = Store.objects.get(pk=pk)
        serializer = StoreSerializer(store, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Store updated successfully",
                "data": serializer.data
            })
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        store = get_object_or_404(Store, pk=pk)
        store.delete()
        return Response({
            "success": True,
            "message": "Store deleted successfully",
            "data": None
        })
    
class MyStoreView(generics.ListAPIView):
    serializer_class = StoreSerializer
    def get_queryset(self):
        producer = Producer.objects.get(user=self.request.user)
        queryset = Store.objects.filter(producer=producer)
        return queryset