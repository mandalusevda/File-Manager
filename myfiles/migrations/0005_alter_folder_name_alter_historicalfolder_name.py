# Generated by Django 4.2.16 on 2024-11-14 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfiles', '0004_alter_file_file_alter_historicalfile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='historicalfolder',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
