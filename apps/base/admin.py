class CheckGroupMixins:

    @staticmethod
    def check_group(request, group):
        return True if request.user.is_superuser or group in request.user.groups.values_list("name", flat=True) else False
