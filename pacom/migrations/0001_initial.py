# Generated by Django 3.1.6 on 2021-05-08 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PairsOfOptionsPARK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('already_range', models.BooleanField(default=False)),
                ('already_find_winner', models.BooleanField(default=False)),
                ('is_not_comparable', models.BooleanField(default=False)),
                ('init_file', models.BooleanField(default=False)),
                ('flag_winner_option', models.IntegerField(default=-1)),
                ('compensable_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='park_compensable_option', to='model.option')),
                ('id_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.model')),
                ('id_option_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_park_option_1', to='model.option')),
                ('id_option_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_park_option_2', to='model.option')),
            ],
        ),
        migrations.CreateModel(
            name='PerfectAlternativePARK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacom.pairsofoptionspark')),
            ],
        ),
        migrations.CreateModel(
            name='ValueOfPerfectAlternativePARK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(null=True)),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.criterion')),
                ('perfect_alternative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacom.perfectalternativepark')),
            ],
        ),
        migrations.CreateModel(
            name='RangeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(null=True)),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.criterion')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.option')),
                ('pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacom.pairsofoptionspark')),
            ],
        ),
        migrations.CreateModel(
            name='HistoryAnswerPACOM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=1000)),
                ('answer', models.CharField(max_length=255)),
                ('id_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.model')),
                ('pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pair_pacom', to='pacom.pairsofoptionspark')),
            ],
        ),
    ]
