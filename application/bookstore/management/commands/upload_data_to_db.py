import json
import os

from django.core.management.base import BaseCommand
from bookstore.models import (
    PaperBook,
    Author,
    Publisher,
    Interpreter,
    Illustrations,
    BookSeries,
    SubCategory,
    Category,
)


class Command(BaseCommand):
    help = 'uploading data to the database in json format'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='absolute path to data in json format')

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        os.chdir(path)

        with open('books.json', 'r', encoding='utf-8') as file:
            book_list = json.load(file)


            counter = 1
            for item in book_list:
                try:
                    print(counter)
                    counter += 1

                    current_book = PaperBook()

                    # mandatory characteristics
                    current_book.title = item['title']
                    current_book.format = item['format']
                    current_book.language = item['language']
                    current_book.book_cover = item['book_cover']
                    current_book.price = item['price']
                    current_book.image = item['image']
                    current_book.about_the_book = item['description']
                    current_book.code = item['code']
                    current_book.category = Category.objects.get(title='Книжки')
                    current_book.subcategory = SubCategory.objects.get(title='Дитяча література')

                    publisher = Publisher.objects.get_or_create(
                        title=item['publisher']['title'],
                        image=item['publisher']['image'],
                        information=item['publisher']['information']
                    )[0]

                    # optional characteristics
                    try:
                        current_book.isbn = item['isbn']
                    except:
                        pass

                    try:
                        current_book.number_of_pages = item['number_of_pages']
                    except:
                        pass

                    try:
                        current_book.Illustrations = item['Illustrations']
                    except:
                        pass

                    try:
                        current_book.year_publication = item['year_publication']
                    except:
                        pass

                    try:
                        current_book.period_literature = item['period_literature'].strip()
                    except:
                        pass

                    try:
                        current_book.paper = item['paper']
                    except:
                        pass

                    try:
                        current_book.edition = int(item['edition'])
                    except:
                        pass

                    try:
                        current_book.weight = item['weight']
                    except:
                        pass

                    try:
                        current_book.year_first_publishing = item['year_first_publishing']
                    except:
                        pass

                    try:
                        book_series = BookSeries.objects.get_or_create(
                            title=item['book_series']['title']
                        )[0]
                    except:
                        pass

                    try:
                        illustrator = Illustrations.objects.get_or_create(
                            title=item['illustrator']['title']
                        )[0]
                    except:
                        pass

                    try:
                        interpreter = Interpreter.objects.get_or_create(
                            title=item['interpreter']['title']
                        )[0]
                    except:
                        pass

                    try:
                        author = Author.objects.get_or_create(
                            title=item['author']['title'],
                            image=item['author']['image'],
                            biography=item['author']['biography']
                        )[0]
                    except:
                        pass

                    # relationship

                    try:
                        current_book.book_series = book_series
                    except:
                        pass

                    current_book.publisher = publisher
                    current_book.save()

                    try:
                        current_book.author.add(author)
                    except:
                        pass

                    try:
                        current_book.interpreter.add(interpreter)
                    except:
                        pass

                    try:
                        current_book.illustrator.add(illustrator)
                    except:
                        pass
                except:
                    self.stdout.write('error')

