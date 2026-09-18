from django.db import migrations


def add_language_category(apps, schema_editor):
    Category = apps.get_model('centers', 'Category')
    Category.objects.using(schema_editor.connection.alias).get_or_create(
        slug='languages',
        defaults={
            'name': 'Til',
            'description': 'Chet tillari, suhbat amaliyoti va til imtihonlariga tayyorgarlik kurslari.',
            'icon': 'mdi-translate',
            'translations': {
                'name': {'uz': 'Til', 'en': 'Languages', 'ru': 'Языки'},
                'description': {
                    'uz': 'Chet tillari, suhbat amaliyoti va til imtihonlariga tayyorgarlik kurslari.',
                    'en': 'Foreign languages, conversation practice and language exam preparation.',
                    'ru': 'Иностранные языки, разговорная практика и подготовка к языковым экзаменам.',
                },
            },
        },
    )


class Migration(migrations.Migration):
    dependencies = [('courses', '0009_course_directions')]
    operations = [migrations.RunPython(add_language_category, migrations.RunPython.noop)]
