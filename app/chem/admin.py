from django.contrib import admin

from core.admin import SoftDeleteAdmin

from .models import Compound, CompoundDescription, Project, ProjectDescription


class ProjectAdmin(SoftDeleteAdmin):
    model = Project
    list_display = ('name',)
    search_fields = ('name',)


class ProjectDescriptionAdmin(SoftDeleteAdmin):
    model = ProjectDescription
    list_display = (
        'project',
        'body',
    )
    search_fields = (
        'project__name',
        'body',
    )


class CompoundAdmin(SoftDeleteAdmin):
    model = Compound
    list_display = ('name',)
    search_fields = ('name',)


class CompoundDescriptionAdmin(SoftDeleteAdmin):
    model = CompoundDescription
    list_display = (
        'compound',
        'body',
    )
    search_fields = (
        'compound__name',
        'body',
    )


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectDescription, ProjectDescriptionAdmin)
admin.site.register(Compound, CompoundAdmin)
admin.site.register(CompoundDescription, CompoundDescriptionAdmin)
