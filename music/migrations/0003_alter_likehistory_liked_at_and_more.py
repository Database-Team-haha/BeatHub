# Generated by Django 5.1.3 on 2024-11-30 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_alter_likehistory_liked_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likehistory',
            name='liked_at',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='listeninghistory',
            name='listened_at',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]