import jwt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from hwprovider.models import HomeWorkManager, HomeWork
from .requester import aiu_auth_token, aiu_hw_assign

class EmailHandlerAPIView(APIView):
    def post(self, request, format=None):
        """
        Returns same email sent in request and authenticates on the AIU.
        """
        student_email = request.data.get("email")
        homework_id = request.data.get("homework_id")

        if HomeWork.objects.filter(
                homework_num=homework_id,
                email=student_email
        ).distinct().count() > 0:
            return Response({
                "student_email": student_email,
                'homework_id': homework_id,
                "homework_assignment": {"answer": -2}
            })

        m1 = HomeWorkManager.objects.last()

        credentials = jwt.decode(m1.aiu_password, settings.SECRET_KEY)
        aiu_password = credentials.get("password")

        aiu_token = aiu_auth_token(m1.aiu_email, aiu_password)
        hw_assign_rsp = aiu_hw_assign(aiu_token, student_email, homework_id)

        if hw_assign_rsp['answer'] == 1:
            HomeWork.objects.create(email=student_email, homework_num=homework_id)

        return Response({
            "student_email": student_email,
            'homework_id': homework_id,
            "homework_assignment": hw_assign_rsp
        })

