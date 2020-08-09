# Generated by Django 3.0.8 on 2020-08-06 10:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0003_resource_filename'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('ch', 'Chemistry'), ('ph', 'Physics'), ('ma', 'Math'), ('ec', 'Economics'), ('en', 'English')], default='ch', max_length=4)),
                ('users', models.ManyToManyField(blank=True, related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
