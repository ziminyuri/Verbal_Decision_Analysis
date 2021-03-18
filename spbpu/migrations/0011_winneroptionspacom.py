# Generated by Django 3.1.6 on 2021-03-18 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spbpu', '0010_pairsofoptionspark_compensable_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='WinnerOptionsPACOM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identical', models.BooleanField(default=False)),
                ('incomparable', models.BooleanField(default=False)),
                ('id_option_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_winner_pacom_option_1', to='spbpu.option')),
                ('id_option_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_winner_pacom_option_2', to='spbpu.option')),
            ],
        ),
    ]
