
from django.db import models
from django.utils import timezone

from .manager import BaseManager
from django.conf import settings
from copa.utils.app_utils.generators import id_generater, ID_LENGTH


class BaseModel(models.Model):
    """
    General model to implement common fields and soft delete
    Attr:
        created_at: Holds date/time for when an object was created.
        updated_at: Holds date/time for last update on an object.
        deleted_at: Holds date/time for soft-deleted objects.
        deleted_at: Holds user who soft-deleted an objects.
        objects: Return objects that have not been soft-deleted.
        all_objects: Return all objects(soft-deleted inclusive)
    """
    id = models.CharField(max_length=ID_LENGTH,
                          default=id_generater,
                          primary_key=True,
                          editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE, blank=True,
                                   null=True)

    objects = BaseManager()
    all_objects = BaseManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, user=None):
        self.deleted_at = timezone.now()
        if user is not None:
            self.deleted_by = user
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()

    def can_be_deleted_by(self, user, user_column="user"):
        """
        Check if a user can delete this instance
        Args:
            user(Object): user instance
            user_column(str): user column name, the foreign key
                            used to reference the user if not provided
                            'user' will be considered
        Returns:
            True: if the user is an admin or is the owner of this instance
                else False
        """

        if getattr(self, user_column, None) == user or user.is_admin:
            return True
        return False
