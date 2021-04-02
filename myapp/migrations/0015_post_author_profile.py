# Generated by Django 3.1.6 on 2021-04-01 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.profile'),
            preserve_default=False,
        ),
    ]
