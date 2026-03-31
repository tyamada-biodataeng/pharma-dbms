from django import forms
from django.contrib import admin, messages
from django.contrib.admin.utils import model_ngettext
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords do not match.'))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'is_active', 'is_staff', 'deleted_at')

    def clean_password(self):
        return self.initial['password']


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = UserChangeForm
    add_form = UserCreationForm
    actions = ['soft_delete_selected', 'restore_selected']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')},
        ),
        (_('Important dates'), {'fields': ('last_login', 'deleted_at')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2', 'is_staff'),
            },
        ),
    )
    list_display = ('username', 'email', 'is_staff', 'is_active', 'deleted_at')
    list_display_links = ('username',)
    list_filter = ('is_staff', 'is_active', ('deleted_at', admin.EmptyFieldListFilter))
    readonly_fields = ('last_login', 'deleted_at')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_queryset(self, request):
        return self.model.objects.with_deleted()

    def delete_model(self, request, obj):
        obj.soft_delete()

    def delete_queryset(self, request, queryset):
        queryset.soft_delete()

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop('delete_selected', None)
        return actions

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


admin.site.register(CustomUser, CustomUserAdmin)
