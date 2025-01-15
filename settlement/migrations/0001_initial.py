# Generated by Django 5.1.3 on 2025-01-14 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settlement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('type', models.CharField(max_length=30, verbose_name='Тип пункта')),
                ('budget', models.IntegerField(max_length=30, verbose_name='Бюджет')),
                ('population', models.IntegerField(max_length=30, verbose_name='Население')),
                ('head', models.CharField(max_length=40, verbose_name='Глава н.п')),
            ],
            options={
                'verbose_name': 'Населённый пункт',
                'verbose_name_plural': 'Населённые пункты',
            },
        ),
    ]