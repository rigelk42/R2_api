from identity.models import CustomUser


class DjangoUserRepository:
    def get_by_id(self, user_id: int) -> CustomUser:
        return CustomUser.objects.get(pk=user_id)

    def get_by_email(self, email: str) -> CustomUser:
        return CustomUser.objects.get(email=email)

    def save(self, user: CustomUser) -> CustomUser:
        user.save()
        return user
