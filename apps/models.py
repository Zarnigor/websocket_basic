from django.contrib.auth.models import AbstractUser
from django.db.models import Model, DateTimeField, TextField, ForeignKey, CASCADE, FileField, SET_NULL, OneToOneField, \
    CharField, ManyToManyField
from django.db.models.functions import Now


# class User(AbstractUser):
#     is_online = False
#     phone

class TimeBasedModel(Model):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True, db_default=Now())

    class Meta:
        abstract = True


class Attachment(TimeBasedModel):
    file = FileField(upload_to='attachments/%Y/%m/%d/')


class Room(Model):
    name = CharField(max_length=128)
    online = ManyToManyField('auth.User', blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name}({self.get_online_count()})'


class Message(TimeBasedModel):
    from_user = ForeignKey('apps.User', CASCADE)
    room = ForeignKey('apps.Room', CASCADE)
    text = CharField(max_length=512)

    def __str__(self):
        return f'{self.User.username}: ({self.text} [{self.created_at}])'
