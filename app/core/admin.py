from django.contrib import admin, messages
from django.contrib.admin.utils import model_ngettext
from django.utils.translation import gettext_lazy as _


class SoftDeleteAdmin(admin.ModelAdmin):
    actions = ['soft_delete_selected', 'restore_selected']
    list_filter = (('deleted_at', admin.EmptyFieldListFilter),)

    def get_queryset(self, request):
        return self.model.objects.with_deleted()

    @admin.action(description=_('Soft delete selected %(verbose_name_plural)s'))
    def soft_delete_selected(self, request, queryset):
        count = queryset.soft_delete()
        self.message_user(
            request,
            _('Successfully soft-deleted %(count)d %(items)s.')
            % {'count': count, 'items': model_ngettext(self.opts, count)},
            messages.SUCCESS,
        )

    @admin.action(description=_('Restore selected %(verbose_name_plural)s'))
    def restore_selected(self, request, queryset):
        count = queryset.restore()
        self.message_user(
            request,
            _('Successfully restored %(count)d %(items)s.')
            % {'count': count, 'items': model_ngettext(self.opts, count)},
            messages.SUCCESS,
        )
