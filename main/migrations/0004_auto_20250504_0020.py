from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0003_alter_techlist_stock_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='TechList',
            name='author',
            field=models.ForeignKey(
                db_column='author_id',
                null=True,
                on_delete=models.CASCADE,
                related_name='products',
                to='main.User',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='TechList',
            name='stars',
            field=models.DecimalField(
                db_column='Rating',
                decimal_places=1,
                default=0.0,
                max_digits=3,
            ),
            preserve_default=False,
        ),
    ]