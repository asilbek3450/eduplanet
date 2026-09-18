from django.db import migrations


def add_directions(apps, schema_editor):
    Category = apps.get_model('centers', 'Category')
    for slug, name in [('frontend', 'Frontend'), ('backend', 'Backend'), ('design', 'Dizayn'), ('smm', 'SMM'), ('mobile', 'Mobil dasturlash'), ('data-ai', 'Data va AI'), ('devops', 'DevOps'), ('other', 'Boshqa yo‘nalishlar')]:
        Category.objects.using(schema_editor.connection.alias).get_or_create(slug=slug, defaults={'name': name})


class Migration(migrations.Migration):
    dependencies = [('courses', '0008_course_category_course_instructor')]
    operations = [migrations.RunPython(add_directions, migrations.RunPython.noop)]
