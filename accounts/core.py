from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q
from django.conf import settings
import os
from io import BytesIO
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try: #to allow authentication through phone number or any other field, modify the below statement
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                with open(os.path.join(settings.USER_PROFILE_PIC,user.uid+".jpg"),'wb') as file_obj:
                    img_blob=settings.BUCKET.get_blob(user.uid+".jpg")
                    if not (img_blob is None):
                        settings.BUCKET.client.download_blob_to_file(img_blob, file_obj)
                    else:
                        with open(os.path.join(settings.STATICFILES_DIRS[1],'default-avatar.png'),'rb') as file:
                            file_obj.write(file.read())
                return user
        return None

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
    def check_user(self, username):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            return None

        return user