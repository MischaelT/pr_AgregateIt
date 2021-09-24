import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_from', models.EmailField(max_length=32)),
                ('subject', models.CharField(max_length=128)),
                ('message', models.CharField(max_length=2047)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResponseLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status_code', models.PositiveSmallIntegerField()),
                ('path', models.CharField(max_length=255)),
                ('response_time', models.PositiveSmallIntegerField(help_text='in milliseconds')),
                ('request_method', models.CharField(choices=[('GET', 'Get'), ('POST', 'Post')], max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('code_name', models.CharField(editable=False, max_length=24, unique=True)),
                ('source_url', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ask', models.DecimalField(decimal_places=2, max_digits=4)),
                ('bid', models.DecimalField(decimal_places=2, max_digits=4)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('currency_name', models.CharField(choices=[('USD', 'Dollar'), ('EUR', 'Euro')], default='USD', max_length=3)),  # noqa
                ('currency_type', models.CharField(max_length=8)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='currency.source')),  # noqa
            ],
        ),
    ]
