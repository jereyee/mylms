# Generated by Django 3.0.8 on 2020-08-06 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_auto_20200806_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lms.Subject'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(choices=[('chemistry', 'Chemistry'), ('physics', 'Physics'), ('math', 'Math'), ('economics', 'Economics'), ('english', 'English')], default='ch', max_length=16),
        ),
    ]