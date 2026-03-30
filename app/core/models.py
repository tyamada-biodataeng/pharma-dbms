from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class CustomBaseModel(models.Model):
    created_at = CreationDateTimeField(_('created at'))
    updated_at = ModificationDateTimeField(_('updated at'))
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    def save(self, **kwargs):
        self.update_modified = kwargs.pop(
            'update_modified', getattr(self, 'update_modified', True)
        )
        super().save(**kwargs)

    class Meta:
        get_latest_by = 'updated_at'
        abstract = True
