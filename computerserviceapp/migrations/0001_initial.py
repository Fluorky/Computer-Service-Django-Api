# Generated by Django 4.2.7 on 2023-11-23 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=11)),
                ('address_line1', models.CharField(blank=True, max_length=255, null=True)),
                ('address_line2', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField(default=0)),
                ('surname', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('quantity_in_stock', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Part',
                'verbose_name_plural': 'Parts',
            },
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField(default=0)),
                ('surname', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Service Request',
                'verbose_name_plural': 'Service Requests',
            },
        ),
        migrations.CreateModel(
            name='ServiceTechnician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=11)),
                ('specialization', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Service Technician',
                'verbose_name_plural': 'Service Technicians',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('servicerequest_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='computerserviceapp.servicerequest')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
            bases=('computerserviceapp.servicerequest',),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='owned_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='computerserviceapp.servicetechnician'),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='requested_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='computerserviceapp.customer'),
        ),
    ]
