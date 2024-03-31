from django.db.models import QuerySet


class UserQuerySetMixin:
    user_field = 'user'
    allow_staff_view = False
    allow_superuser_view = True

    def get_queryset(self) -> QuerySet:
        user = self.request.user  # type: ignore
        qs = super().get_queryset()  # type: ignore
        if self.allow_superuser_view is True and user.is_superuser:
            return qs
        lookup_data = {self.user_field: user}
        return qs.filter(**lookup_data)
