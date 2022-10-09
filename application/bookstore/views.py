import json

from liqpay.liqpay3 import LiqPay
from utilities.utilities import get_data_from_path, get_cities, get_warehouses_by_city
from application import settings
from bookstore.cart import Cart

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import F
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.list import MultipleObjectMixin
from django.shortcuts import redirect, render

from bookstore.forms import UserRegistrationForm, UserLoginForm, BookReviewForm
from bookstore.models import (
    SubCategory,
    PaperBook,
    BookReview, Author, Publisher, BookSeries, Order,
)


class BookListView(ListView):
    template_name = 'bookstore/books/index.html'
    paginate_by = 20
    model = PaperBook
    context_object_name = 'book_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = Cart(request=self.request)

        context = super().get_context_data()
        context['subcategories'] = SubCategory.objects.all()
        context['form'] = UserLoginForm()
        context['cart_storage'] = cart.cart_storage
        return context

    def get_queryset(self):
        # return queryset by sorting data
        if self.kwargs.get('sort_data'):
            sorting_data = get_data_from_path(self.kwargs.get('sort_data'))
            if sorting_data == 'rating':
                return PaperBook.objects.all().order_by(F(sorting_data).desc(nulls_last=True))
            return PaperBook.objects.all().order_by(sorting_data)

        # return queryset by subcategory
        return PaperBook.objects.all().order_by(
            F('rating').desc(nulls_last=True))

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        form = UserLoginForm(data)

        # Login block
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            login(request, user)
            return JsonResponse({'isInvalid': ''})
        else:
            return JsonResponse({
                'isInvalid': 'true',
                'textError': form.get_text_errors(),
            })
        # end login block

        return super().get(request)

    def get(self, request, **kwargs):
        cart = Cart(request)

        # Logout block
        if request.GET.get('logout') is not None:
            logout(request)
            return redirect(request.path)
        # end logout block

        # BLOCK CART
        # adding a product to the cart
        if request.GET.get('add-to-cart') is not None:
            cart.add_product(request.GET.get('add-to-cart'))
            return JsonResponse({'book_list': cart.cart_storage})
        # end adding block

        # change quantity in the cart
        if request.GET.get('changeQuantity'):
            book_pk_and_unit = request.GET.get('changeQuantity').split(':')
            cart.change_quantity(book_pk_and_unit[1], book_pk_and_unit[0])

        if request.GET.get('changeQuantityByInput'):
            book_pk_and_quantity = request.GET.get('changeQuantityByInput').split(':')
            cart.change_quantity(book_pk_and_quantity[0], book_pk_and_quantity[1])
        # end change quantity block

        # remove from cart
        if request.GET.get('deleteFromCart'):
            cart.delete_from_cart(request.GET.get('deleteFromCart'))
        # end remove block
        # END BLOCK CART

        return super().get(request)


class BookByCategoryListView(ListView):
    model = PaperBook
    paginate_by = 20
    template_name = 'bookstore/books/index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        # return queryset by sorting data and subcategory
        if self.kwargs.get('sort_data'):
            sorting_data = get_data_from_path(self.kwargs.get('sort_data'))
            if sorting_data == 'rating':
                return PaperBook.objects.filter(subcategory=SubCategory.objects.get(pk=self.kwargs.get('pk'))).order_by(
                    F(sorting_data).desc(nulls_last=True))
            return PaperBook.objects.filter(subcategory=SubCategory.objects.get(pk=self.kwargs.get('pk'))).order_by(
                sorting_data)

        # return queryset by subcategory
        return PaperBook.objects.filter(subcategory=SubCategory.objects.get(pk=self.kwargs.get('pk'))).order_by(
            F('rating').desc(nulls_last=True))

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = Cart(request=self.request)

        context = super().get_context_data()
        context['subcategories'] = SubCategory.objects.all()
        context['form'] = UserLoginForm()
        context['cart_storage'] = cart.cart_storage
        return context

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        form = UserLoginForm(data)

        # Login block
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            login(request, user)
            return JsonResponse({'isInvalid': ''})
        else:
            return JsonResponse({
                'isInvalid': 'true',
                'textError': form.get_text_errors(),
            })
        # end login block

        return super().get(request)

    def get(self, request, **kwargs):
        cart = Cart(request)

        # Logout block
        if request.GET.get('logout') is not None:
            logout(request)
            return redirect(request.path)
        # end logout block

        # BLOCK CART
        # adding a product to the cart
        if request.GET.get('add-to-cart') is not None:
            cart.add_product(request.GET.get('add-to-cart'))
            return JsonResponse({'book_list': cart.cart_storage})
        # end adding block

        # change quantity in the cart
        if request.GET.get('changeQuantity'):
            book_pk_and_unit = request.GET.get('changeQuantity').split(':')
            cart.change_quantity(book_pk_and_unit[1], book_pk_and_unit[0])

        if request.GET.get('changeQuantityByInput'):
            book_pk_and_quantity = request.GET.get('changeQuantityByInput').split(':')
            cart.change_quantity(book_pk_and_quantity[0], book_pk_and_quantity[1])
        # end change quantity block

        # remove from cart
        if request.GET.get('deleteFromCart'):
            cart.delete_from_cart(request.GET.get('deleteFromCart'))
        # end remove block
        # END BLOCK CART

        return super().get(request)


class BookDetailView(DetailView, MultipleObjectMixin):
    model = PaperBook
    paginate_by = 4
    template_name = 'bookstore/books/product-details.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = Cart(request=self.request)

        object_list = BookReview.objects.filter(book=self.get_object()).order_by('-date')
        context = super(BookDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['subcategories'] = SubCategory.objects.all()
        context['length_list_review'] = len(object_list)
        context['form'] = UserLoginForm()
        context['review_form'] = BookReviewForm()
        context['cart_storage'] = cart.cart_storage
        return context

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        form = UserLoginForm(data)

        # Login block
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            login(request, user)
            return JsonResponse({'isInvalid': ''})
        else:
            return JsonResponse({
                'isInvalid': 'true',
                'textError': form.get_text_errors(),
            })
        # end login block

        return super().get(request)

    def get(self, request, **kwargs):
        cart = Cart(request)

        # push like
        if request.GET.get('pushlike'):
            review = BookReview.objects.get(pk=request.GET.get('pushlike'))

            if request.user.is_active:
                user = request.user
                result = review.push_like(user)
            else:
                result = 'userIsNotActive'

            return JsonResponse({'likeResult': result})
        # end block

        # form review block
        form = BookReviewForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            review = BookReview(
                book=self.get_object(),
                review_text=cd.get('review_text'),
                rating=cd.get('rating'),
            )

            if request.user.is_active:
                review.user = request.user
            else:
                review.user = User.objects.get(username='Гість')

            review.save()
            self.get_object().setup_rating()
            return redirect(request.path)
        # end review block

        # Logout block
        if request.GET.get('logout') is not None:
            logout(request)
            return redirect(request.path)
        # end logout block

        # BLOCK CART
        # adding a product to the cart
        if request.GET.get('add-to-cart') is not None:
            cart.add_product(request.GET.get('add-to-cart'))
            return JsonResponse({'book_list': cart.cart_storage})
        # end adding block

        # change quantity in the cart
        if request.GET.get('changeQuantity'):
            book_pk_and_unit = request.GET.get('changeQuantity').split(':')
            cart.change_quantity(book_pk_and_unit[1], book_pk_and_unit[0])

        if request.GET.get('changeQuantityByInput'):
            book_pk_and_quantity = request.GET.get('changeQuantityByInput').split(':')
            cart.change_quantity(book_pk_and_quantity[0], book_pk_and_quantity[1])
        # end change quantity block

        # remove from cart
        if request.GET.get('deleteFromCart'):
            cart.delete_from_cart(request.GET.get('deleteFromCart'))
        # end remove block
        # END BLOCK CART

        return super().get(request)


class BookListByCharacteristicView(ListView):
    model = PaperBook
    paginate_by = 20
    template_name = 'bookstore/books/books_by_characteristic.html'
    context_object_name = 'book_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = Cart(request=self.request)

        context = super().get_context_data()
        context['subcategories'] = SubCategory.objects.all()
        context['is_search_page'] = True
        context['form'] = UserLoginForm()
        context['cart_storage'] = cart.cart_storage

        if self.kwargs.get('characteristic') == 'author':
            context['current_object'] = Author.objects.get(pk=self.kwargs.get('pk'))
        elif self.kwargs.get('characteristic') == 'publisher':
            context['current_object'] = Publisher.objects.get(pk=self.kwargs.get('pk'))
        else:
            context['current_object'] = BookSeries.objects.get(pk=self.kwargs.get('pk'))

        return context

    def get_queryset(self):
        if self.kwargs.get('characteristic') == 'author':
            return PaperBook.objects.filter(author=Author.objects.get(pk=self.kwargs.get('pk')))
        elif self.kwargs.get('characteristic') == 'publisher':
            return PaperBook.objects.filter(publisher=Publisher.objects.get(pk=self.kwargs.get('pk')))
        else:
            return PaperBook.objects.filter(book_series=BookSeries.objects.get(pk=self.kwargs.get('pk')))

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        form = UserLoginForm(data)

        # Login block
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            login(request, user)
            return JsonResponse({'isInvalid': ''})
        else:
            return JsonResponse({
                'isInvalid': 'true',
                'textError': form.get_text_errors(),
            })
        # end login block

        return super().get(request)

    def get(self, request, **kwargs):
        cart = Cart(request)

        # Logout block
        if request.GET.get('logout') is not None:
            logout(request)
            return redirect(request.path)
        # end logout block

        # BLOCK CART
        # adding a product to the cart
        if request.GET.get('add-to-cart') is not None:
            cart.add_product(request.GET.get('add-to-cart'))
            return JsonResponse({'book_list': cart.cart_storage})
        # end adding block

        # change quantity in the cart
        if request.GET.get('changeQuantity'):
            book_pk_and_unit = request.GET.get('changeQuantity').split(':')
            cart.change_quantity(book_pk_and_unit[1], book_pk_and_unit[0])

        if request.GET.get('changeQuantityByInput'):
            book_pk_and_quantity = request.GET.get('changeQuantityByInput').split(':')
            cart.change_quantity(book_pk_and_quantity[0], book_pk_and_quantity[1])
        # end change quantity block

        # remove from cart
        if request.GET.get('deleteFromCart'):
            cart.delete_from_cart(request.GET.get('deleteFromCart'))
        # end remove block
        # END BLOCK CART

        return super().get(request)


class BookSearchListView(ListView):
    model = PaperBook
    paginate_by = 20
    template_name = 'bookstore/books/index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        if self.kwargs.get('search_request'):
            try:
                return PaperBook.objects.filter(title__icontains=self.kwargs['search_request'])
            except:
                return PaperBook.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = Cart(request=self.request)

        context = super().get_context_data()
        context['subcategories'] = SubCategory.objects.all()
        context['is_search_page'] = True
        context['form'] = UserLoginForm()
        context['cart_storage'] = cart.cart_storage
        return context

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        form = UserLoginForm(data)

        # Login block
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            login(request, user)
            return JsonResponse({'isInvalid': ''})
        else:
            return JsonResponse({
                'isInvalid': 'true',
                'textError': form.get_text_errors(),
            })
        # end login block

        return super().get(request)

    def get(self, request, **kwargs):
        cart = Cart(request)

        # Logout block
        if request.GET.get('logout') is not None:
            logout(request)
            return redirect(request.path)
        # end logout block

        # BLOCK CART
        # adding a product to the cart
        if request.GET.get('add-to-cart') is not None:
            cart.add_product(request.GET.get('add-to-cart'))
            return JsonResponse({'book_list': cart.cart_storage})
        # end adding block

        # change quantity in the cart
        if request.GET.get('changeQuantity'):
            book_pk_and_unit = request.GET.get('changeQuantity').split(':')
            cart.change_quantity(book_pk_and_unit[1], book_pk_and_unit[0])

        if request.GET.get('changeQuantityByInput'):
            book_pk_and_quantity = request.GET.get('changeQuantityByInput').split(':')
            cart.change_quantity(book_pk_and_quantity[0], book_pk_and_quantity[1])
        # end change quantity block

        # remove from cart
        if request.GET.get('deleteFromCart'):
            cart.delete_from_cart(request.GET.get('deleteFromCart'))
        # end remove block
        # END BLOCK CART

        return super().get(request)


class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'bookstore/authentication/registration.html'
    success_url = '/'

    def form_valid(self, form):
        cd = form.cleaned_data
        user = User.objects.create_user(
            username=cd.get('username'),
            email=cd.get('email'),
            password=cd.get('password')
        )
        return super().form_valid(form)


class CheckoutPageView(TemplateView):
    template_name = 'bookstore/checkout/checkout.html'

    def get_context_data(self, **kwargs):
        cart = Cart(request=self.request)
        context = super().get_context_data()
        context['cart'] = cart.cart_storage
        context['amount_of_books'] = cart.get_amount_of_books()
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('getCities'):
            return JsonResponse({'cities': get_cities()})
        if request.GET.get('getWarehouse'):
            return JsonResponse({'warehouses': get_warehouses_by_city(request.GET.get('getWarehouse'))})
        return super().get(request)

    def post(self, request, *args, **kwargs):
        cart = Cart(request=request)
        data = json.loads(request.body)

        if data['createNewOrder'] == 'True':
            order = Order(
                first_name=data['firstName'],
                last_name=data['lastName'],
                email=data['emailInput'],
                phone=data['phoneInput'],
                city=data['cityInput'],
                warehouse=data['warehouseInput'],
                pay_type=data['payType'],
                order_items=cart.get_text_for_send(),
            )
            if request.user.is_active:
                order.user = request.user
            order.save()

            del request.session['cart']

            return JsonResponse({'createNewOrder': 'true', 'orderPK': order.pk})

        return super().get(request)


class CheckoutApplicationStatusPageView(TemplateView):
    template_name = 'bookstore/checkout/checkout_application_status.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = Cart(request=self.request)

        context = super().get_context_data()
        context['subcategories'] = SubCategory.objects.all()
        context['form'] = UserLoginForm()
        context['cart_storage'] = cart.cart_storage
        return context


class PayView(TemplateView):
    template_name = 'bookstore/checkout/liqpay_api.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request=request)
        send_data = request.session['send_data']

        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': cart.get_amount_of_books(),
            'currency': 'UAH',
            'description': f'Інформація: \n'
                           f'\tІм\'я: {send_data.get("firstName")}\n'
                           f'\tФамілія: {send_data.get("lastName")}\n'
                           f'\tНомер телефону: {send_data.get("phoneInput")}\n'
                           f'Товари: {cart.get_text_for_send()}',
            'version': '3',
            'sandbox': 0,  # sandbox mode, set to 1 to enable it
            'server_url': settings.LIQPAY_SERVER_URL,  # url to callback view
            'verifycode': request.session.session_key
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data})


@method_decorator(csrf_exempt, name='dispatch')
class SaveSendingData(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        request.session['send_data'] = data
        if request.user.is_active:
            request.session['send_data']['username'] = request.user.username
        return JsonResponse({'success': 'OK!'})


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)

        def encode(self, session_dict):
            return SessionStore().encode(session_dict)

        if sign == signature:
            response = liqpay.decode_data_from_str(data)
            s = Session.objects.get(pk=response.get('verifycode'))
            session_dict = s.get_decoded()

            if response['status'] == 'success':
                order = Order(
                    first_name=session_dict['send_data']['firstName'],
                    last_name=session_dict['send_data']['lastName'],
                    email=session_dict['send_data']['emailInput'],
                    phone=session_dict['send_data']['phoneInput'],
                    city=session_dict['send_data']['cityInput'],
                    warehouse=session_dict['send_data']['warehouseInput'],
                    pay_type=session_dict['send_data']['payType'],
                    order_items=response['description'],
                )
                if session_dict['send_data']['username']:
                    order.user = User.objects.get(username=session_dict['send_data']['username'])
                order.save()

                del session_dict['cart']
                del session_dict['send_data']
                session_dict = encode(s, session_dict)
                s.session_data = session_dict
                s.save()

        return HttpResponse()
