# Generated by Django 4.2.14 on 2024-09-08 13:54

import apps.base.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opportunities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signoff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], max_length=64)),
                ('sub_stage', models.DecimalField(decimal_places=2, max_digits=4)),
                ('turn_around_time', models.PositiveIntegerField()),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opportunities.opportunity')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opportunities.stage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'opportunity', 'status', 'sub_stage', 'stage')},
            },
            bases=(models.Model, apps.base.models.SelfAwareModelMixin),
        ),
    ]
