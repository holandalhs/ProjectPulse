# Generated by Django 5.0.1 on 2024-02-16 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novoprojeto', '0004_rename_qtd_projetos_listagem_quantidade_projetos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listagem',
            name='descricao_home',
            field=models.CharField(max_length=100),
        ),
    ]
