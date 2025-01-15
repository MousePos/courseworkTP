from django.db import models

# Create your models here.

class Settlement(models.Model):
    name = models.CharField('Название', max_length=50)
    type = models.CharField('Тип пункта', max_length=30)
    budget = models.IntegerField('Бюджет')
    population = models.IntegerField('Население')
    head = models.CharField('Глава н.п', max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Населённый пункт'
        verbose_name_plural = 'Населённые пункты'