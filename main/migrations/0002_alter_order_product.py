# Generated by Django 4.1 on 2025-05-09 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="product",
            field=models.ForeignKey(
                blank=True,
                db_column="ProductID",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.techlist",
            ),
        ),
    ]
