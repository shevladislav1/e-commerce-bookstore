from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Категорія')

    def __str__(self) -> str:
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категорія')
    title = models.CharField(max_length=100, verbose_name='Підкатегорія')
    image = models.ImageField(upload_to='images/subcategory', blank=True, verbose_name='Зображення')

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('book_list_by_category', args=(self.pk,))


class PaperBook(models.Model):
    LANGUAGES_CHOICES = [
        ('Російська', 'Російська'),
        ('Українська', 'Українська'),
        ('Англійська', 'Англійська'),
    ]

    PAPER_CHOICES = [
        ('Офсетний', 'Офсетний'),
        ('Книжкова', 'Книжкова'),
        ('Крейдований', 'Крейдований'),
    ]

    BOOK_COVER_CHOICES = [
        ('Тверда', 'Тверда'),
        ('М\'яка', 'М\'яка'),
    ]

    ILLUSTRATIONS_CHOICES = [
        ('Немає ілюстрацій', 'Немає ілюстрацій'),
        ('Чорно-білі', 'Чорно-білі'),
        ('Кольорові', 'Кольорові'),
    ]

    PERIOD_LITERATURE_CHOICES = [
        ('Література XX ст.', 'Література ХХ ст.'),
        ('Сучасна література', 'Сучасна література'),
    ]

    # mandatory characteristics
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='*Категорія')
    subcategory = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True, verbose_name='*Суб-категорія')
    code = models.CharField(max_length=100, null=True, verbose_name='*Код книги')
    title = models.CharField(max_length=100, verbose_name='*Назва книги')
    format = models.CharField(max_length=100, verbose_name='*Формат')
    language = models.CharField(max_length=100, choices=LANGUAGES_CHOICES, verbose_name='*Мова')
    book_cover = models.CharField(max_length=100, choices=BOOK_COVER_CHOICES, verbose_name='*Палітурка')
    price = models.IntegerField(verbose_name='*Ціна (грн)')
    image = models.CharField(max_length=255, verbose_name='*Зображення')
    about_the_book = models.TextField(verbose_name='*Усе про книжку')
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True, verbose_name='*Видавництво')

    # optional characteristics
    isbn = models.CharField(max_length=100, blank=True, null=True, verbose_name='ISBN')
    Illustrations = models.CharField(max_length=100, choices=ILLUSTRATIONS_CHOICES, blank=True, null=True,
                                     verbose_name='Ілюстрації')
    number_of_pages = models.CharField(max_length=100, blank=True, null=True, verbose_name='Кількість сторінок')
    author = models.ManyToManyField('Author', blank=True, verbose_name='Автор')
    interpreter = models.ManyToManyField('Interpreter', blank=True, verbose_name='Перекладач')
    illustrator = models.ManyToManyField('Illustrations', blank=True, verbose_name='Ілюстратор')
    book_series = models.ForeignKey('BookSeries', on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Серія')
    year_first_publishing = models.IntegerField(blank=True, null=True, verbose_name='Рік першого видавництва')
    year_publication = models.IntegerField(blank=True, null=True, verbose_name='Рік видання')
    weight = models.CharField(max_length=100, blank=True, null=True, verbose_name='Вага')
    edition = models.IntegerField(blank=True, null=True, verbose_name='Тираж')
    paper = models.CharField(max_length=100, choices=PAPER_CHOICES, blank=True, null=True, verbose_name='Папір')
    period_literature = models.CharField(
        max_length=100, choices=PERIOD_LITERATURE_CHOICES, blank=True, null=True,
        verbose_name='Література за періодами')
    rating = models.FloatField(null=True, default=0)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('book_page', args=(self.pk,))

    def setup_rating(self):
        review_list = BookReview.objects.filter(book=self.pk).aggregate(Sum('rating'))
        avr_rating = round(review_list.get('rating__sum') / len(BookReview.objects.filter(book=self.pk)), 1)
        self.rating = avr_rating
        self.save()

    def get_float_rating(self):
        if self.rating is None:
            return 0.0
        return self.rating

    def get_integer_rating(self):
        return int(self.rating)

    def dict_rating(self):
        review_qs = BookReview.objects.filter(book=self.pk)

        rating_one = BookReview.objects.filter(book=self.pk, rating=1)
        rating_two = BookReview.objects.filter(book=self.pk, rating=2)
        rating_three = BookReview.objects.filter(book=self.pk, rating=3)
        rating_four = BookReview.objects.filter(book=self.pk, rating=4)
        rating_five = BookReview.objects.filter(book=self.pk, rating=5)

        if len(review_qs) > 0:
            percentage_one = int(len(rating_one) * 100 / len(review_qs))
            percentage_two = int(len(rating_two) * 100 / len(review_qs))
            percentage_three = int(len(rating_three) * 100 / len(review_qs))
            percentage_four = int(len(rating_four) * 100 / len(review_qs))
            percentage_five = int(len(rating_five) * 100 / len(review_qs))
        else:
            percentage_one = 0
            percentage_two = 0
            percentage_three = 0
            percentage_four = 0
            percentage_five = 0

        return {
            '1': len(rating_one),
            '2': len(rating_two),
            '3': len(rating_three),
            '4': len(rating_four),
            '5': len(rating_five),
            'percentage_one': percentage_one,
            'percentage_two': percentage_two,
            'percentage_three': percentage_three,
            'percentage_four': percentage_four,
            'percentage_five': percentage_five,
        }


class Author(models.Model):
    title = models.CharField(max_length=100, verbose_name='Повне ім\'я')
    image = models.CharField(max_length=255, blank=True, verbose_name='*Зображення')
    information = models.TextField(blank=True, verbose_name='Біографія')

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('book_list_by_characteristic', args=('author', self.pk,))


class Publisher(models.Model):
    title = models.CharField(max_length=100, verbose_name='Назва видавництва')
    image = models.CharField(max_length=255, blank=True, verbose_name='*Зображення')
    information = models.TextField(blank=True, verbose_name='Інформація про видавництво')

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('book_list_by_characteristic', args=('publisher', self.pk,))


class Interpreter(models.Model):
    title = models.CharField(max_length=100, verbose_name='Повне ім\'я')

    def __str__(self) -> str:
        return self.title


class Illustrations(models.Model):
    title = models.CharField(max_length=100, verbose_name='Повне ім\'я')

    def __str__(self) -> str:
        return self.title


class BookSeries(models.Model):
    title = models.CharField(max_length=100, verbose_name='Серія книг')

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('book_list_by_characteristic', args=('series', self.pk,))


class BookReview(models.Model):
    book = models.ForeignKey('PaperBook', on_delete=models.CASCADE, null=True, verbose_name='Книга')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Користувач')
    review_text = models.CharField(max_length=300, verbose_name='Зміст рецензії')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    class Rating(models.IntegerChoices):
        Жахливо = 1
        Погано = 2
        Середньо = 3
        Чудово = 4
        Ідеально = 5

    rating = models.IntegerField(choices=Rating.choices, null=True, verbose_name='Рейтинг')

    def amount_likes(self):
        return len(LikeReview.objects.filter(review=self.pk))

    def push_like(self, user):
        try:
            like = LikeReview.objects.get(review=self.pk, user=user)
        except:
            like = None

        if like is None:
            book_review = BookReview.objects.get(pk=self.pk)
            like = LikeReview.objects.create(review=book_review, user=user)
            like.save()
            result = 'plusOne'
        else:
            like.delete()
            result = 'minusOne'

        return result


class LikeReview(models.Model):
    review = models.ForeignKey('BookReview', on_delete=models.CASCADE, null=True, verbose_name='Рецензія')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Користувач')


class Order(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=25)
    city = models.CharField(max_length=150)
    warehouse = models.CharField(max_length=150)
    pay_type = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_items = models.TextField(null=True)



