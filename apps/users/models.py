from django.db.models import Model, ForeignKey, IntegerField, CASCADE


class UserData(Model):
    phone = IntegerField()
    user = ForeignKey('auth.User', CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
