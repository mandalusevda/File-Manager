# Generated by Django 4.2.16 on 2024-11-13 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'Video')], default=12, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalfile',
            name='file_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'Video')], default=56, max_length=10),
            preserve_default=False,
        ),
    ]