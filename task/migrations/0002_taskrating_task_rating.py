# Generated by Django 4.1.2 on 2023-03-13 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('excellent', 'Excellent'), ('good', 'Good'), ('poor', 'poor')], default='good', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='rating',
            field=models.ManyToManyField(blank=True, related_name='task_rating', to='task.taskrating'),
        ),
    ]
