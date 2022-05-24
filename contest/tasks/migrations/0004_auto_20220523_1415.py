# Generated by Django 2.2.19 on 2022-05-23 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20220522_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flexibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='Сложность')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Сложность',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='task',
            name='task_rating',
            field=models.IntegerField(default=10, verbose_name='Рейтинг задания'),
        ),
        migrations.AddField(
            model_name='task',
            name='flexibility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='tasks.Flexibility', verbose_name='Сложность'),
        ),
    ]