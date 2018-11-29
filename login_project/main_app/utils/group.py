from django.contrib.auth.models import Group

exist_group_list = [g for g in Group.objects.all()]


def get_user_group_list(request):
    return [g for g in request.user.groups.all()]


def has_group_bool(request):
    user_belong_group_list = [g for g in request.user.groups.all()]
    # 共通のリストを抜きだし、その要素数が0以上(つまり、G所属している)はTrue
    common_list = set(exist_group_list) & set(user_belong_group_list)
    return True if len(common_list) > 0 else False


def belong_group_bool(request):
    user_belong_group_list = [g for g in request.user.groups.all()]
    return True if len(user_belong_group_list) > 0 else False