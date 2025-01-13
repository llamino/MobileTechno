# Generated by Django 5.1.4 on 2025-01-13 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0003_rename_url_mobile_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobile',
            name='id',
        ),
        migrations.AddField(
            model_name='mobile',
            name='product_id',
            field=models.IntegerField(db_index=True, default=2026, primary_key=True, serialize=False, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mobile',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
