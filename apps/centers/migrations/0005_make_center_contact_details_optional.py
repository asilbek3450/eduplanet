from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("centers", "0004_alter_learningcenter_options_category_description_and_more")]

    operations = [
        migrations.AlterField(model_name="learningcenter", name="email", field=models.EmailField(blank=True, max_length=254)),
        migrations.AlterField(model_name="learningcenter", name="phone_number", field=models.CharField(blank=True, max_length=17)),
    ]
