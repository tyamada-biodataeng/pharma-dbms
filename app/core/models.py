from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class SoftDeleteQuerySet(models.QuerySet):

    def soft_delete(self):
        return self.update(deleted_at=timezone.now())

    def alive(self):
        return self.filter(deleted_at__isnull=True)


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class CustomBaseModel(models.Model):
    objects = SoftDeleteManager()
    created_at = CreationDateTimeField(_("created at"))
    updated_at = ModificationDateTimeField(_("updated at"))
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    def save(self, **kwargs):
        self.update_modified = kwargs.pop(
            "update_modified", getattr(self, "update_modified", True)
        )
        super().save(**kwargs)

    class Meta:
        get_latest_by = "updated_at"
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "updated_at"])
