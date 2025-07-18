from rest_framework import viewsets, permissions
from .models import Project, Module
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny 
from .serializers import ProjectSerializer, ModuleSerializer
from .permissions import IsDirector, IsAdmin, IsAdminOrDirector  
from rest_framework.response import Response

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'role') and user.role == 'manager':
            qs = Project.objects.filter(manager=user)
        elif hasattr(user, 'role') and user.role == 'director':
            qs = Project.objects.all()
        else:
            qs = Project.objects.none()
        
        if hasattr(user, 'organization') and user.organization:
            qs = qs.filter(organization=user.organization)
        
        if self.action in ['archive', 'destroy', 'update', 'partial_update', 'retrieve', 'archivedprojects']:
            return qs
        return qs.filter(is_archived=False)
        
    #     if self.action in ['archive', 'destroy', 'update', 'partial_update', 'retrieve', 'archivedprojects']:
    #         return Project.objects.all()  
    #     return Project.objects.filter(is_archived=False)
    # serializer_class = ProjectSerializer
    # permission_classes = [permissions.IsAuthenticated()]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrDirector(),]
        else:
            return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(
            director=self.request.user,
            organization=self.request.user.organization
            )
        
    @action(detail=False, methods=['get'], url_path='archivedprojects')
    def archivedprojects(self, request):
        archived = Project.objects.filter(is_archived=True)
        serializer = self.get_serializer(archived, many=True)
        return Response(serializer.data)        
        
    @action(detail=True, methods=['patch'], url_path='archive')
    def archive(self, request, pk=None):
        project = self.get_object()
        is_archived = request.data.get('is_archived')
        if is_archived is None:
            return Response({'detail': 'is_archived required'}, status=status.HTTP_400_BAD_REQUEST)
        project.is_archived = is_archived
        project.save()
        serializer = self.get_serializer(project)
        return Response(serializer.data)    

class ArchivedProjectsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_archived=True)
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated()]

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Module.objects.all()
        return Module.objects.filter(organization=user.organization)

    def perform_create(self, serializer):
        user = self.request.user

        if not user.organization:
            raise permissions.PermissionDenied("Вы не прикреплены к организации.")

        serializer.save(organization=user.organization)
        
#====================================================>>>>

# class ProjectViewSet(viewsets.ModelViewSet):
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.IsAuthenticated()]

#     def get_queryset(self):
#         user = self.request.user

#         if hasattr(user, 'role') and user.role == 'manager':
#             qs = Project.objects.filter(manager=user)
#         elif hasattr(user, 'role') and user.role == 'director':
#             qs = Project.objects.all()
#         else:
#             qs = Project.objects.none()

#         if hasattr(user, 'organization') and user.organization:
#             qs = qs.filter(organization=user.organization)

#         # Arxivlangan yoki boshqa actionlar uchun to‘liq ro‘yxat, aks holda faqat arxivlanmaganlar
#         if self.action in ['archive', 'destroy', 'update', 'partial_update', 'retrieve', 'archivedprojects']:
#             return qs
#         return qs.filter(is_archived=False)

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             return [permissions.IsAuthenticated(), IsDirector()]
#         return [permissions.IsAuthenticated()]

#     def perform_create(self, serializer):
#         serializer.save(director=self.request.user, organization=self.request.user.organization)

#     @action(detail=False, methods=['get'], url_path='archivedprojects')
#     def archivedprojects(self, request):
#         user = self.request.user
#         archived = Project.objects.filter(is_archived=True)
        
#         if hasattr(user, 'organization') and user.organization:
#             archived = archived.filter(organization=user.organization)

#         serializer = self.get_serializer(archived, many=True)
#         return Response(serializer.data)

#     @action(detail=True, methods=['patch'], url_path='archive')
#     def archive(self, request, pk=None):
#         project = self.get_object()
#         is_archived = request.data.get('is_archived')

#         if is_archived is None:
#             return Response({'detail': 'is_archived required'}, status=400)

#         project.is_archived = is_archived
#         project.save()
#         serializer = self.get_serializer(project)
#         return Response(serializer.data)

# class ArchivedProjectsViewSet(viewsets.ModelViewSet):
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.IsAuthenticated()]

#     def get_queryset(self):
#         user = self.request.user
#         qs = Project.objects.filter(is_archived=True)

#         if hasattr(user, 'organization') and user.organization:
#             qs = qs.filter(organization=user.organization)
#         return qs

# class ModuleViewSet(viewsets.ModelViewSet):
#     serializer_class = ModuleSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         qs = Module.objects.all()

#         if hasattr(user, 'organization') and user.organization:
#             qs = qs.filter(organization=user.organization)
#         return qs

#     def perform_create(self, serializer):
#         serializer.save(organization=self.request.user.organization)
        