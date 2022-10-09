from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    UserRegistrationView,
    BookByCategoryListView,
    BookSearchListView,
    BookListByCharacteristicView,
    CheckoutPageView, CheckoutApplicationStatusPageView, PayView, PayCallbackView, SaveSendingData,
)

urlpatterns = [
    # all books and all boks by sort data
    path('', BookListView.as_view(), name='book_list'),
    path('sort_<str:sort_data>/', BookListView.as_view(), name='book_list_by_sort_data'),
    # books by category and sort data
    path('books_by_category/<int:pk>/', BookByCategoryListView.as_view(), name='book_list_by_category'),
    path('books_by_category/<int:pk>/sort_<str:sort_data>/', BookByCategoryListView.as_view(),
         name='book_list_by_category_and_sort_data'),
    # books by search
    path('books_by_search/<str:search_request>/', BookSearchListView.as_view(), name='book_list_by_search'),
    # books by author, publsiher, series
    path('books_by_<str:characteristic>/<int:pk>/', BookListByCharacteristicView.as_view(),
         name='book_list_by_characteristic'),
    # current book detail
    path('current_book/<int:pk>/', BookDetailView.as_view(), name='book_page'),
    # authentication
    path('authentication/registration', UserRegistrationView.as_view(), name='registration_page'),
    # checkout
    path('checkout/', CheckoutPageView.as_view(), name='checkout_page'),
    path('checkout/application_status/', CheckoutApplicationStatusPageView.as_view(),
         name='application_status_page'),
    path('checkout/pay', PayView.as_view(), name='pay_view'),
    path('checkout/pay-callback', PayCallbackView.as_view(), name='pay_callback'),
    path('checkout/save-data', SaveSendingData.as_view(), name='save_sending_data'),
]
