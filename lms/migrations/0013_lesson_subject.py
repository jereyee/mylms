# Generated by Django 3.0.8 on 2020-08-08 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0012_auto_20200809_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lms.Subject'),
        ),
    ]
