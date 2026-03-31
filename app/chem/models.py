from django.db import models

from core.models import CustomBaseModel


class Project(CustomBaseModel):
    name = models.CharField(max_length=50)

    unique_together_with_deleted_at = ['name']

    class Meta:
        db_table = 'project'


class ProjectDescription(CustomBaseModel):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='description')
    body = models.TextField()

    unique_together_with_deleted_at = ['project']

    class Meta:
        db_table = 'project_description'


class Compound(CustomBaseModel):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='compounds')

    unique_together_with_deleted_at = ['name']

    class Meta:
        db_table = 'compound'


class CompoundDescription(CustomBaseModel):
    compound = models.OneToOneField(Compound, on_delete=models.CASCADE, related_name='description')
    body = models.TextField()

    unique_together_with_deleted_at = ['compound']

    class Meta:
        db_table = 'compound_description'
