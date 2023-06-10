from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import UserData
from apps.users.tasks import send_sms


class SendVerificationCode(APIView):
    permission_classes = ()

    def post(self, request):
        phone = request.data['phone']
        user = UserData.objects.filter(phone=phone)
        if user:
            send_sms.delay(phone)
        else:
            return Response({'success': False, 'message': 'Bunday foydalanuvchi mavjud emas!'})
        return Response({'success': True, 'message': 'Yuborildi'})
