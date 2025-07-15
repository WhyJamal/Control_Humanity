from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Organization
from .serializers import RegisterSerializer, UserSerializer, OrganizationRegisterSerializer, OrganizationSerializer
from .permissions import IsDirector, IsManager, IsAdmin

User = get_user_model()

class OrganizationRegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = OrganizationRegisterSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({
                "user": UserSerializer(result["user"]).data,
                "organization": OrganizationSerializer(result["organization"]).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = User.objects.all()

        if not user.is_superuser:
            qs = qs.filter(organization=user.organization)
        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

    def perform_create(self, serializer):
        user = self.request.user

        if not user.organization:
            raise permissions.PermissionDenied("Ваша учетная запись не привязана к организации.")

        serializer.save(organization=user.organization)

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def managers(self, request):
        qs = self.get_queryset().filter(role='manager')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def employees(self, request):
        qs = self.get_queryset().filter(role='employee')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


#=======================================================>>>>
# old code!!!
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_permissions(self):
#         if self.action == 'create':
#             return [permissions.AllowAny()]
#         return super().get_permissions()

#     def get_queryset(self):
#         qs = User.objects.all()
#         user = self.request.user

#         if user.is_superuser == False:
#             qs = qs.filter(organization=user.organization)
#         return qs
    
#     def perform_create(self, serializer):
#         serializer.save(organization=self.request.user.organization)
    
#     def get_serializer_class(self):
#         if self.action == 'create':
#             return RegisterSerializer
#         return UserSerializer

#     def destroy(self, request, *args, **kwargs):
#         user_to_delete = self.get_object()

#         if request.user.role == 'employee':
#             return Response(
#                 {"detail": "Sizda bu amalni bajarish huquqi yoʻq."},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         if user_to_delete.is_superuser:
#             return Response(
#                 {"detail": "Superuserni oʻchirib boʻlmaydi."},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         if user_to_delete == request.user:
#             return Response(
#                 {"detail": "Oʻzingizni oʻchirib boʻlmaysiz."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def managers(self, request):
        qs = self.get_queryset().filter(role='manager')

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def employees(self, request):
        qs = self.get_queryset().filter(role='employee')

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
       
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, IsDirector, IsManager, IsAdmin]

class BindTelegramView(APIView):
    permission_classes = [permissions.AllowAny()]

    def post(self, request):
        phone = request.data.get("phone")
        telegram_id = request.data.get("telegram_id")

        if not phone or not telegram_id:
            return Response({"error": "phone va telegram_id talab qilinadi."}, status=400)

        try:
            user = User.objects.get(phone=phone)
            user.telegram_id = telegram_id
            user.save()
            return Response({"message": "Telegram ID muvaffaqiyatli bog‘landi."})
        except User.DoesNotExist:
            return Response({"error": "Bu telefon raqam bilan foydalanuvchi topilmadi."}, status=404)
