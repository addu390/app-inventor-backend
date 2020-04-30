import uuid

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Application(BaseModel):
    user_id = models.CharField(max_length=255, null=False)
    app_id = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    request = models.TextField(null=True)
    description = models.TextField(null=True)
    name = models.CharField(max_length=50, null=False, default=uuid.uuid4().__str__())

    class Meta:
        db_table = "application"
        indexes = [
            models.Index(fields=['user_id'], name='user_application_idx'),
        ]
        unique_together = [['user_id', 'app_id']]

    def __str__(self):
        return self.name


class User(BaseModel):
    user_id = models.CharField(max_length=255, null=False, unique=True)
    email = models.CharField(max_length=50, null=False)
    display_name = models.CharField(max_length=50, null=True)
    image_url = models.TextField(max_length=255, null=True)
    access_token = models.TextField(null=True)
    refresh_token = models.TextField(null=True)
    id_token = models.TextField(null=True)

    class Meta:
        db_table = "user"
        indexes = [
            models.Index(fields=['user_id'], name='user_idx'),
        ]

    def __str__(self):
        return self.name


class Component(BaseModel):
    app_id = models.CharField(max_length=255, null=False)
    component_id = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    request = models.TextField(null=True)

    class Meta:
        db_table = "component"
        indexes = [
            models.Index(fields=['app_id'], name='app_component_idx'),
        ]
        unique_together = [['app_id', 'component_id']]

    def __str__(self):
        return self.name
