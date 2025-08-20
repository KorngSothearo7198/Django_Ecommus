from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token  #  correct


# class ProtectedAPIView(APIView):
#     permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     return Response({
    #         'message': 'Welcome, you are authenticated!',
    #         'user': str(request.user)
    #     })

    # def post(self, request):
    #     return Response({
    #         'message': 'Welcome, you are authenticated!',
    #         'user': str(request.user)
    #     })
    

class ProtectedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": f"Hello {request.user.username}, your token is valid!"
        })





