from django.contrib import admin

from .models import Compound, CompoundDescription, Project, ProjectDescription


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ("name",)
    search_fields = ("name",)


class ProjectDescriptionAdmin(admin.ModelAdmin):
    model = ProjectDescription
    list_display = (
        "project",
        "description",
    )
    search_fields = (
        "project__name",
        "description",
    )


class CompoundAdmin(admin.ModelAdmin):
    model = Compound
    list_display = ("name",)
    search_fields = ("name",)


class CompoundDescriptionAdmin(admin.ModelAdmin):
    model = CompoundDescription
    list_display = (
        "compound",
        "description",
    )
    search_fields = (
        "compound__name",
        "description",
    )


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectDescription, ProjectDescriptionAdmin)
admin.site.register(Compound, CompoundAdmin)
admin.site.register(CompoundDescription, CompoundDescriptionAdmin)
