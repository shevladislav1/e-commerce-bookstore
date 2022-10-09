from .models import PaperBook


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if cart is None:
            cart = request.session['cart'] = {}
        else:
            self.session['cart'] = cart

        self.cart_storage = cart

    def add_product(self, pk: str):
        current_book = PaperBook.objects.get(pk=pk)
        self.cart_storage[pk] = {
            'quantity': 1,
            'title': current_book.title,
            'image': current_book.image,
            'price': current_book.price,
            'code': current_book.code,
        }

    def change_quantity(self, book_pk, unit):

        if unit == 'plus':
            self.cart_storage[book_pk]['quantity'] += 1
        elif unit == 'minus':
            self.cart_storage[book_pk]['quantity'] -= 1
        else:
            self.cart_storage[book_pk]['quantity'] = int(unit)

    def delete_from_cart(self, book_pk):
        del self.cart_storage[str(book_pk)]

    def get_amount_of_books(self):
        count = 0
        for item in self.cart_storage:
            count += self.cart_storage[item]['quantity'] * self.cart_storage[item]['price']
        return count

    def get_text_for_send(self):
        output_text = []
        for item in self.cart_storage:
            text = f'Назва: {self.cart_storage[item]["title"]}, \n' \
                   f'Кількість: {self.cart_storage[item]["quantity"]} шт. ,\n' \
                   f'Ціна за одиницю: {self.cart_storage[item]["price"]} грн,\n' \
                   f'Всього за книгу: {self.cart_storage[item]["price"] * self.cart_storage[item]["quantity"]} грн.\n' \
                   f'Код товара: {self.cart_storage[item]["code"]}\n'
            output_text.append(text)
        output_text = '\n'.join(output_text)
        return output_text
