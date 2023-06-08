from django.shortcuts import render
from google.auth import google_auth
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

# ...


class GoogleLoginView(APIView):
    def post(self, request):
        # Get the ID token from the request data
        id_token_data = request.data.get("id_token")

        try:
            # Verify the ID token with Google
            id_info = id_token.verify_oauth2_token(
                id_token_data, requests.Request(), settings.GOOGLE_CLIENT_ID
            )

            # Check if the ID token is issued for your client ID
            if id_info["aud"] != settings.GOOGLE_CLIENT_ID:
                return Response(
                    {"error": "Invalid client ID"}, status=status.HTTP_401_UNAUTHORIZED
                )

            # Get the user's email and other relevant information
            email = id_info["email"]
            # ...

            # Perform any necessary actions with the user information (e.g., create or update the user in your system)

            # Generate a JWT token for the authenticated user
            token = jwt.encode(
                {"user_id": user.id},
                settings.JWT_AUTH["JWT_SECRET_KEY"],
                algorithm=settings.JWT_AUTH["JWT_ALGORITHM"],
            )

            return Response({"token": token})

        except ValueError:
            # Invalid token
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )


class GoogleLoginView(APIView):
    def post(self, request):
        # Perform the authentication process with Google using the client ID and secret
        # obtained from the Google Cloud Console.

        # Once the user is successfully authenticated, create a JWT token.
        token = jwt.encode(
            {"user_id": user.id},
            settings.JWT_AUTH["JWT_SECRET_KEY"],
            algorithm=settings.JWT_AUTH["JWT_ALGORITHM"],
        )

        return Response({"token": token})
