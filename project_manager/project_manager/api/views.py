from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ClientSerializer, ClientDetailSerializer, ProjectSerializer, ProjectDetailSerializer

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated]

class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        client = Client.objects.get(id=self.kwargs['pk'])
        serializer.save(client=client)

    def create(self, request, *args, **kwargs):
        client = Client.objects.get(id=self.kwargs['pk'])
        data = request.data
        project = Project.objects.create(project_name=data['project_name'], client=client, created_by=request.user)
        for user_data in data['users']:
            user = User.objects.get(id=user_data['id'])
            project.users.add(user)
        project.save()
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserProjectsView(generics.ListAPIView):
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)
