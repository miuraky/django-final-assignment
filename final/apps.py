# final/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save


def create_default_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    # 一般ユーザグループ
    general_group, _ = Group.objects.get_or_create(name="GeneralUser")
    perms = Permission.objects.filter(
        codename__in=[
            "view_product",
            "view_stockhistory",
            "add_stockhistory",
        ]
    )
    general_group.permissions.set(perms)

    # 管理者グループ
    admin_group, _ = Group.objects.get_or_create(name="ProductAdmin")
    perms = Permission.objects.filter(
        codename__in=[
            "add_product",
            "change_product",
            "delete_product",
            "view_product",
            "view_stockhistory",
            "add_stockhistory",
        ]
    )
    admin_group.permissions.set(perms)


def add_user_to_general_group(sender, instance, created, **kwargs):
    """ユーザ作成時に GeneralUser グループへ自動追加"""
    if created:
        from django.contrib.auth.models import Group
        try:
            general_group = Group.objects.get(name="GeneralUser")
            instance.groups.add(general_group)
        except Group.DoesNotExist:
            pass


class FinalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'final'

    def ready(self):
        post_migrate.connect(create_default_groups, sender=self)

        from django.contrib.auth import get_user_model
        User = get_user_model()
        post_save.connect(add_user_to_general_group, sender=User)
