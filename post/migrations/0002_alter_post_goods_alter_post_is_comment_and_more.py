# Generated by Django 4.1.5 on 2023-02-02 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='goods',
            field=models.PositiveIntegerField(default=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_comment',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_good',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='location',
            field=models.TextField(default=None, null=True),
        ),
    ]