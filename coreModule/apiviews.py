import uuid

from .constants import INVALID_TOKEN, AUTH, USER_ID
from .models import Application, User, Component
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ApplicationResourceSerializer, UserSerializer, ApplicationShortSerializer, ComponentSerializer
from rest_framework import status, generics
import json
from .services.helper import get_or_none, token_refresh, is_valid_user
from .services.transformer import ApplicationTransformers


class ComponentDetail(APIView):
    """
    Component : Refers to the UI components such as BUTTON, TEXT AREA, RADIO
    An Application can have several components (One to many)
    Request column of the component is flattened in the Response of GET response and reverted in PUT.
    """
    def get(self, request, user_id, app_id, component_id):
        if not is_valid_user(user_id, self.request.query_params.get(AUTH), True):
            return Response(INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST)
        component = get_object_or_404(Component, component_id=component_id, app_id=app_id)
        components = ApplicationTransformers.component_request_transformer([component])
        return Response(components[0])

    def put(self, request, user_id, app_id, component_id):
        """
        Update existing Component
        Note that the entire component has to be in the request,
        as this is a replacement of request object.
        @return Success/ Error object.
        """
        if not is_valid_user(user_id, self.request.query_params.get(AUTH), True):
            return Response(INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST)
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
        """
        TODO : Support soft deletes to support "UNDO" from the application.
        (Similar to GMAIL undo option after sending a message)
        """
        component = get_object_or_404(Component, component_id=component_id, app_id=app_id)
        component.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplicationDetail(APIView):
    """
    Each user can have several Applications (One to many)
    Each Application can have several Components.
    """
    def get(self, request, user_id, app_id):
        """
        From user_id (Auth token is validated) and app_id
        @return a LIST of flattened json of Components.
        """
        if not is_valid_user(user_id, self.request.query_params.get(AUTH), True):
            return Response(INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST)

        application_object = get_object_or_404(Application, app_id=app_id, user_id=user_id)
        application = ApplicationResourceSerializer(application_object).data

        components_object = Component.objects.filter(app_id=app_id)
        components = ApplicationTransformers.component_request_transformer(components_object)

        application["components"] = components
        return Response(application)

    def post(self, request, user_id, app_id):
        """
        Create or Update an Application
        If app_id is None - CREATION
        """
        if not is_valid_user(user_id, self.request.query_params.get(AUTH), True):
            return Response(INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST)

        application = {
            "user_id": user_id,
            "app_id": app_id,
            "name": request.data.get("name"),
            "description": request.data.get("description")
        }

        if app_id is None or app_id == "NULL":
            # If the path param app_id is not present, CREATE new Application.
            application["app_id"] = uuid.uuid4().__str__()
            serializer = ApplicationResourceSerializer(data=application)
        else:
            application_object = get_object_or_404(Application, app_id=app_id, user_id=user_id)
            serializer = ApplicationResourceSerializer(application_object, data=application)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id, app_id):
        """
        Component CREATION, return the unique identifier of the component.
        COMPONENT details are stored as a BLOB in "request" column.
        """
        if not is_valid_user(user_id, self.request.query_params.get(AUTH), True):
            return Response(INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST)
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
        if not is_valid_user(user_id, self.request.query_params.get(AUTH), True):
            return Response(INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST)

        application = get_object_or_404(Application, app_id=app_id,
                                        user_id=user_id)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):
    """
    User CREATION/ UPDATION
    Conversion from snake_case to camelCase for consistency with Google OAuth API response.
    """
    def post(self, request, user_id):
        user = get_or_none(User, user_id=user_id)
        data = UserSerializer(user).data

        # Move to a services/helper if required.
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
            update_user = {
                "user_id": user_id,
                "email": data.get("email"),
                "access_token": request.data.get("accessToken"),
                "id_token": request.data.get("idToken")
            }
            serializer = UserSerializer(user, data=update_user)
        else:
            serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            serializer.save()
            serializer_data = ApplicationTransformers.user_response_serializer(serializer.data)
            return Response(serializer_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id):
        """
        Validate AUTH token and get user details
        displayName and imageUrl is powered by USER GET API and not local storage
        """
        if not is_valid_user(user_id, self.request.query_params.get(AUTH), False):
            return Response(INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, user_id=user_id)

        data = UserSerializer(user).data
        serializer_data = ApplicationTransformers.user_response_serializer(data)

        return Response(serializer_data)


class ApplicationList(generics.ListAPIView):
    serializer_class = ApplicationShortSerializer

    def get_queryset(self):
        """
        This view should return a list of all the APPLICATION
        for the currently authenticated user (USER_ID).
        TODO : Validate if deactivating/ activating of APPLICATION needs to be supported
        """
        user_id = self.kwargs[USER_ID]
        if not is_valid_user(user_id, self.request.query_params.get(AUTH), True):
            return Response(INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST)
        return Application.objects.filter(user_id=user_id)


class GoogleOAuth(APIView):
    def post(self, request, user_id):
        if not is_valid_user(user_id, self.request.query_params.get(AUTH), False):
            return Response(INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST)
        response = token_refresh(user_id)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_201_CREATED)
        return Response(INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST)
