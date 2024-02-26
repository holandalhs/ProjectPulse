# Generated by Django 5.0.1 on 2024-02-14 15:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novoprojeto', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Validacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resposta', models.BooleanField(default=False)),
                ('acertou', models.BooleanField(default=False)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='novoprojeto.novoprojeto')),
            ],
        ),
        migrations.CreateModel(
            name='Listagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao_home', models.TextField()),
                ('quantidade_projetos', models.IntegerField()),
                ('dificuldade', models.CharField(choices=[('D', 'Difícil'), ('M', 'Médio'), ('F', 'Fácil')], max_length=1)),
                ('categoria', models.ManyToManyField(to='novoprojeto.categoria')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('projetos', models.ManyToManyField(to='novoprojeto.validacao')),
            ],
        ),
    ]