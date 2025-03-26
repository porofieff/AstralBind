# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

'''
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   НЕ ТРОГАТЬ БЕЗ РАЗРЕШЕНИЯ ХОЗЯИНА      ┃
┃               (Егора)!!!                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

        ♛
       ( •_•)
          |
       /  | \
        /   \

         \_(_"_)_/  \_(_"_)_/
'''





class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class UserDescriptionTable(models.Model):
    user_id = models.ForeignKey('UserInfoTable', on_delete=models.PROTECT)
    user_description = models.CharField(max_length=255)
    user_values = models.CharField(max_length=255)
    user_children = models.IntegerField(blank=True, null=True)
    user_desc_children = models.CharField(max_length=255)
    user_hobbies = models.IntegerField(blank=True, null=True)
    user_personal_traits = models.CharField(max_length=255)
    user_target_life = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user_description_table'


class UserFavoritesLikes(models.Model):
    user_id = models.ForeignKey('UserInfoTable', on_delete=models.PROTECT)
    user_infavorit_id = models.IntegerField()
    user_messages = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'user_favorites_likes'


class UserInfoTable(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_age = models.IntegerField()
    user_location = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        managed = False
        db_table = 'user_info_table'


class UserMatches(models.Model):
    user_id_1 = models.ForeignKey('UserInfoTable', on_delete=models.PROTECT)
    #user_id_2 = models.IntegerField()
    user_id_2 = models.ManyToManyField('UserFavoritesLikes', related_name='user_infavorit_id')
    user_matches = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'user_matches'


class UserMessage(models.Model):
    user_id_1 = models.ForeignKey('UserInfoTable', on_delete=models.PROTECT)
    #user_id_2 = models.IntegerField()
    user_id_2 = models.ManyToManyField('UserMatches', related_name='user_id_2')
    messages = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'user_message'


class UserPersonalityData(models.Model):
    user_id = models.ForeignKey('UserInfoTable', on_delete=models.PROTECT)
    user_login = models.CharField(max_length=255)
    user_pwd = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user_personality_data'
