# Generated by Django 4.2.14 on 2024-09-08 13:54

import apps.base.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('company_name', models.CharField(blank=True, max_length=24, null=True)),
                ('service_type', models.CharField(max_length=24)),
                ('desired_outcome', models.TextField()),
                ('product', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price (USD)')),
                ('is_sales_qualified', models.BooleanField()),
                ('expected_date', models.DateField()),
                ('sales_advisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_advisor_opportunities', to=settings.AUTH_USER_MODEL)),
                ('solution_architect', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solution_architect_opportunities', to=settings.AUTH_USER_MODEL)),
                ('solution_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solution_manager_opportunities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Opportunity',
                'verbose_name_plural': 'Opportunities',
            },
            bases=(models.Model, apps.base.models.SelfAwareModelMixin),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('SERVICE_DELIVERY_OUTPUT', 'SERVICE_DELIVERY_OUTPUT'), ('STATEMENT_OF_WORK', 'STATEMENT_OF_WORK')], max_length=64)),
                ('document', models.FileField(upload_to='')),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opportunities.opportunity')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, apps.base.models.SelfAwareModelMixin),
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('stage', models.CharField(choices=[('INITIAL', 'INITIAL'), ('SCOPING', 'SCOPING'), ('BID', 'BID'), ('PROJECT', 'PROJECT'), ('OPERATIONS', 'OPERATIONS')], max_length=64)),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opportunities.opportunity')),
            ],
            options={
                'unique_together': {('opportunity', 'stage')},
            },
            bases=(models.Model, apps.base.models.SelfAwareModelMixin),
        ),
    ]
