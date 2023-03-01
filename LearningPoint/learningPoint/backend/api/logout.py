from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.settings import backend_settings
from backend.utils.users import remove_user_token


class LogoutView(APIView):
    """
    This is used to Logout system.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Override post method to remove token and custom response
        """

        # Remove user token
        if backend_settings.LOGOUT_REMOVE_TOKEN:
            remove_user_token(self.request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)
