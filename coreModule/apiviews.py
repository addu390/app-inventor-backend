import uuid

from .constants import JSON_REQUEST, APP_ID, USER_ID
from .models import Application, User, Component
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ApplicationResourceSerializer, UserSerializer, ApplicationShortSerializer, \
    ApplicationUpdateSerializer, ComponentSerializer
from rest_framework import status, generics
import json
from .services.helper import get_or_none
from .services.transformer import ApplicationTransformers


class ComponentDetail(APIView):
    def get(self, request, user_id, app_id, component_id):
        component = get_object_or_404(Component, component_id=component_id, app_id=app_id)
        components = ApplicationTransformers.component_request_transformer([component])

        return Response(components[0])

    def put(self, request, user_id, app_id, component_id):
        component_object = get_object_or_404(Component, component_id=component_id, app_id=app_id)
        component = {
            "app_id": app_id,
            "component_id": component_id,
            "request": json.dumps(request.data)
        }
        serializer = ComponentSerializer(component_object, data=component)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, app_id, component_id):
        component = get_object_or_404(Component, component_id=component_id, app_id=app_id)
        component.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplicationDetail(APIView):
    def get(self, request, user_id, app_id):
        application_object = get_object_or_404(Application, app_id=app_id, user_id=user_id)
        application = ApplicationResourceSerializer(application_object).data
        components_object = Component.objects.filter(app_id=app_id)
        components = ApplicationTransformers.component_request_transformer(components_object)

        application["components"] = components
        return Response(application)

    # App creation
    def post(self, request, user_id, app_id):
        application = {
            "user_id": user_id,
            "app_id": app_id,
            "name": request.data.get("name"),
            "description": request.data.get("description")
        }
        if app_id is None or app_id == "NULL":
            application["app_id"] = uuid.uuid4().__str__()
            serializer = ApplicationResourceSerializer(data=application)
        else:
            application_object = get_object_or_404(Application, app_id=app_id, user_id=user_id)
            serializer = ApplicationResourceSerializer(application_object, data=application)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Updates component addition only
    # Request should be a Component
    def put(self, request, user_id, app_id):
        application = get_object_or_404(Application, app_id=app_id,
                                        user_id=user_id)
        component = {
            "app_id": app_id,
            "component_id": uuid.uuid4().__str__(),
            "request": json.dumps(request.data)
        }
        serializer = ComponentSerializer(data=component)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, app_id):
        application = get_object_or_404(Application, app_id=app_id,
                                        user_id=user_id)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):
    def post(self, request, user_id):
        user = get_or_none(User, user_id=user_id)
        user_data = {
            "user_id": request.data.get("userId"),
            "display_name": request.data.get("displayName"),
            "image_url": request.data.get("imageUrl"),
            "refresh_token": request.data.get("refreshToken"),
            "email": request.data.get("email"),
            "access_token": request.data.get("accessToken"),
            "id_token": request.data.get("idToken"),
        }
        if user:
            serializer = UserSerializer(user, data=user_data)
        else:
            serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            serializer_data = {
                "userId": serializer.data.get("user_id"),
                "displayName": serializer.data.get("display_name"),
                "imageUrl": serializer.data.get("image_url"),
                "refreshToken": serializer.data.get("refresh_token"),
                "email": serializer.data.get("email"),
                "accessToken": serializer.data.get("access_token"),
                "idToken": serializer.data.get("id_token"),
            }
            return Response(serializer_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id):
        user = get_object_or_404(User, user_id=user_id)
        data = UserSerializer(user).data
        serializer_data = {
            "userId": data.get("user_id"),
            "displayName": data.get("display_name"),
            "imageUrl": data.get("image_url"),
            "refreshToken": data.get("refresh_token"),
            "email": data.get("email"),
            "accessToken": data.get("access_token"),
            "idToken": data.get("id_token"),
        }

        return Response(serializer_data)


class ApplicationList(generics.ListAPIView):
    serializer_class = ApplicationShortSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user_id = self.kwargs['user_id']
        return Application.objects.filter(user_id=user_id)
