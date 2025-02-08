# Generated by Django 5.1.4 on 2025-02-08 04:00

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancel_date', models.DateTimeField(blank=True, null=True)),
                ('refund_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('booking_time', models.DateTimeField(auto_now_add=True)),
                ('store_pet', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cage',
            fields=[
                ('cage', models.AutoField(primary_key=True, serialize=False)),
                ('capacity', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('address', models.TextField(blank=True, max_length=100, null=True)),
                ('role', models.CharField(choices=[('user', 'User'), ('staff', 'Staff'), ('admin', 'Admin'), ('veterinarian', 'Veterinarian')], default='user', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancelled', models.BooleanField(default=False)),
                ('awaiting', models.BooleanField(default=False)),
                ('confirm', models.BooleanField(default=False)),
                ('success', models.BooleanField(default=False)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.booking')),
            ],
        ),
        migrations.CreateModel(
            name='CageStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacant', models.BooleanField(default=True)),
                ('in_use', models.BooleanField(default=False)),
                ('dirty', models.BooleanField(default=False)),
                ('cage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cage')),
            ],
        ),
        migrations.CreateModel(
            name='CageType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isolation', models.BooleanField(default=False)),
                ('recovery', models.BooleanField(default=False)),
                ('long_term', models.BooleanField(default=False)),
                ('short_term', models.BooleanField(default=False)),
                ('cage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cage')),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('extra_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_customer', models.CharField(max_length=100)),
                ('phone_number_customer', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('email_customer', models.EmailField(blank=True, max_length=254, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examine', models.BooleanField(default=False)),
                ('hospitalization', models.BooleanField(default=False)),
                ('vaccination', models.BooleanField(default=False)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species', models.CharField(max_length=50)),
                ('age', models.PositiveIntegerField()),
                ('name_pet', models.CharField(max_length=100)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pet_status', models.CharField(blank=True, max_length=50, null=True)),
                ('pet_type', models.CharField(blank=True, max_length=50, null=True)),
                ('is_male', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('disease', models.CharField(blank=True, max_length=255, null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Hospitalization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('symptom', models.TextField(blank=True, null=True)),
                ('cage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cage')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Examine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.TextField(blank=True, null=True)),
                ('symptom', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('treatment_process', models.TextField(blank=True, null=True)),
                ('result', models.TextField(blank=True, null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pet')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='pet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.pet'),
        ),
        migrations.CreateModel(
            name='PetStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('description', models.TextField(blank=True, null=True)),
                ('hospitalization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.hospitalization')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_customer', models.TextField(blank=True, null=True)),
                ('form_veterinarian', models.TextField(blank=True, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_staff', models.CharField(max_length=100)),
                ('phone_number_staff', models.CharField(blank=True, max_length=15, null=True)),
                ('email_staff', models.EmailField(blank=True, max_length=254, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.staff'),
        ),
        migrations.CreateModel(
            name='VaccinationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('vaccine_type', models.CharField(blank=True, max_length=255, null=True)),
                ('dosage', models.CharField(blank=True, max_length=50, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccination_histories', to='app.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Veterinarian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_veterinarian', models.CharField(max_length=100)),
                ('phone_number_veterinarian', models.CharField(blank=True, max_length=15, null=True)),
                ('specialization', models.CharField(blank=True, max_length=100, null=True)),
                ('email_vet', models.EmailField(blank=True, max_length=254, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('morning', models.BooleanField(default=False)),
                ('afternoon', models.BooleanField(default=False)),
                ('night', models.BooleanField(default=False)),
                ('veterinarian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.veterinarian')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='veterinarian',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.veterinarian'),
        ),
    ]
