# Generated by Django 3.0.8 on 2020-08-08 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0011_auto_20200808_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(choices=[('chemistry', 'Chemistry'), ('physics', 'Physics'), ('math', 'Math'), ('economics', 'Economics'), ('english', 'English'), ('programming', 'Programming'), ('history', 'History')], default='chemistry', max_length=16),
        ),
        migrations.AlterField(
            model_name='user',
            name='subjects',
            field=models.ManyToManyField(blank=True, related_name='subjects', to='lms.Subject'),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(default='Lesson', max_length=128)),
                ('url', models.CharField(default='', max_length=256)),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]