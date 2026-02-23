from django.db import models
from django.urls import reverse

class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'commission type'
        verbose_name_plural = 'commission types'

class Commission(models.Model):
    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.CASCADE,
        related_name="commissions"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    updated_on = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return '{} from {}'.format(self.title, self.commission_type)
    
    def get_absolute_url(self):
        return reverse('requests')
    
    class Meta:
        ordering = ['created_on']
        verbose_name = 'commission'
        verbose_name_plural = 'commissions'



