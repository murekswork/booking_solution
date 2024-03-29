class UserQuerySetMixin:
    user_field = 'user'
    allow_staff_view = False
    allow_superuser_view = True

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if self.allow_superuser_view is True and user.is_superuser:
            return qs
        lookup_data = {}
        lookup_data[self.user_field] = user
        return qs.filter(**lookup_data)
