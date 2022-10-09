# Generated by Django 4.1.1 on 2022-09-20 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name="Повне ім'я")),
                ('image', models.CharField(blank=True, max_length=255, verbose_name='*Зображення')),
                ('biography', models.TextField(blank=True, verbose_name='Біографія')),
            ],
        ),
        migrations.CreateModel(
            name='BookSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Серія книг')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Категорія')),
            ],
        ),
        migrations.CreateModel(
            name='Illustrations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name="Повне ім'я")),
            ],
        ),
        migrations.CreateModel(
            name='Interpreter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name="Повне ім'я")),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Назва видавництва')),
                ('image', models.CharField(blank=True, max_length=255, verbose_name='*Зображення')),
                ('information', models.TextField(blank=True, verbose_name='Інформація про видавництво')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Підкатегорія')),
                ('image', models.ImageField(blank=True, upload_to='images/subcategory', verbose_name='Зображення')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.category', verbose_name='Категорія')),
            ],
        ),
        migrations.CreateModel(
            name='PaperBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, null=True, verbose_name='*Код книги')),
                ('title', models.CharField(max_length=100, verbose_name='*Назва книги')),
                ('format', models.CharField(max_length=100, verbose_name='*Формат')),
                ('language', models.CharField(choices=[('Російська', 'Російська'), ('Українська', 'Українська'), ('Англійська', 'Англійська')], max_length=100, verbose_name='*Мова')),
                ('book_cover', models.CharField(choices=[('Тверда', 'Тверда'), ("М'яка", "М'яка")], max_length=100, verbose_name='*Палітурка')),
                ('price', models.IntegerField(verbose_name='*Ціна (грн)')),
                ('image', models.CharField(max_length=255, verbose_name='*Зображення')),
                ('about_the_book', models.TextField(verbose_name='*Усе про книжку')),
                ('isbn', models.CharField(blank=True, max_length=100, null=True, verbose_name='ISBN')),
                ('Illustrations', models.CharField(blank=True, choices=[('Немає ілюстрацій', 'Немає ілюстрацій'), ('Чорно-білі', 'Чорно-білі'), ('Кольорові', 'Кольорові')], max_length=100, null=True, verbose_name='*Ілюстрації')),
                ('number_of_pages', models.CharField(blank=True, max_length=100, null=True, verbose_name='Кількість сторінок')),
                ('year_first_publishing', models.IntegerField(blank=True, null=True, verbose_name='Рік першого видавництва')),
                ('year_publication', models.IntegerField(blank=True, null=True, verbose_name='Рік видання')),
                ('weight', models.CharField(blank=True, max_length=100, null=True, verbose_name='Вага')),
                ('edition', models.IntegerField(blank=True, null=True, verbose_name='Тираж')),
                ('paper', models.CharField(blank=True, choices=[('Офсетний', 'Офсетний'), ('Книжкова', 'Книжкова'), ('Крейдований', 'Крейдований')], max_length=100, null=True, verbose_name='Папір')),
                ('period_literature', models.CharField(blank=True, choices=[('Література XX ст.', 'Література ХХ ст.'), ('Сучасна література', 'Сучасна література')], max_length=100, null=True, verbose_name='Література за періодами')),
                ('author', models.ManyToManyField(blank=True, to='bookstore.author', verbose_name='Автор')),
                ('book_series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bookstore.bookseries', verbose_name='Серія')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bookstore.category', verbose_name='*Категорія')),
                ('illustrator', models.ManyToManyField(blank=True, to='bookstore.illustrations', verbose_name='Ілюстратор')),
                ('interpreter', models.ManyToManyField(blank=True, to='bookstore.interpreter', verbose_name='Перекладач')),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bookstore.publisher', verbose_name='*Видавництво')),
                ('subcategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bookstore.subcategory', verbose_name='*Суб-категорія')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
