# Generated by Django 3.0.8 on 2020-08-06 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0006_auto_20200806_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='content',
            field=models.TextField(default='', max_length=1028, verbose_name=''),
        ),
        migrations.AddField(
            model_name='update',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='update',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='resource',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.Subject'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(choices=[('chemistry', 'Chemistry'), ('physics', 'Physics'), ('math', 'Math'), ('economics', 'Economics'), ('english', 'English')], default='chemistry', max_length=16),
        ),
    ]
