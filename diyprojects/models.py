from django.db import models

class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ['name',]
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'

class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        related_name='projects',
        null=True
    )
    description = models.TextField(null=False, blank=False)
    materials = models.TextField(null=False, blank=False)
    steps = models.TextField(null=False, blank=False)
    created_on = models.DateTimeField(null=False)
    updated_on = models.DateTimeField(null=False)

    class Meta:
        ordering = ['created_on',]

