# Generated by Django 5.0.1 on 2024-02-15 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novoprojeto', '0002_validacao_listagem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listagem',
            old_name='quantidade_projetos',
            new_name='qtd_projetos',
        ),
    ]
