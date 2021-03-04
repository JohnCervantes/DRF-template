from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication


from .permissions import *
from .serializers import *
from .models import *

# Create your views here.


class HelloAPIView(APIView):
    """ test API view"""
    serializer_class = HelloSerializer

    def get(self, request, format=None):
        """ Returns a list of APIViews features"""
        context = {'message_list': [
            'hello world!',
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional django view',
            'gives you the most control over your application',
            'Is mapped manually to URLs'
        ]}

        return Response(context, status=status.HTTP_201_CREATED)

    def post(self, request):
        """ Create a hello message with our name """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            context = {'message': f'Hello {name}'}
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """ handle full updating an object """
        return Response({'method': 'PUT'}, status=status.HTTP_201_CREATED)

    def patch(self, request, pk=None):
        """ handle partial update an object """
        return Response({'method': 'PATCH'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        """ handle partial update an object """
        return Response({'method': 'PATCH'}, status=status.HTTP_201_CREATED)


class UserProfileAPIView(APIView):
    """ Handle craeting and updating user profiles """
    serializer_class = UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile,)

    def get(self, request, id=None, format=None):
        """ Returns a list of User profiles"""
        if id is not None:
            queryset = UserProfile.objects.filter(id=id)
        else:
            queryset = UserProfile.objects.all()
        serializer = self.serializer_class(queryset, many=True)

        if len(serializer.data) != 0:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error_message': f"id \"{id}\" not found"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """ Create a User profile"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, pk=None):
        """ Replace a user with a new User object model """
        queryset = UserProfile.objects.get(id=id)
        serializer = self.serializer_class(queryset, data=request.data)
        self.check_object_permissions(request, queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, pk=None):
        """ Delete a user model object """
        queryset = UserProfile.objects.get(id=id)
        queryset.delete()
        self.check_object_permissions(request, queryset)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, id, pk=None):
        """ Replace a user with a new User object model """
        queryset = UserProfile.objects.get(id=id)
        serializer = self.serializer_class(
            queryset, data=request.data, partial=True)
        self.check_object_permissions(request, queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
