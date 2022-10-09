from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from bookstore.models import BookReview


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=25, label='Логін')
    password = forms.CharField(required=True, max_length=25, widget=forms.PasswordInput(), label='Пароль')
    password_confirm = forms.CharField(required=True, max_length=25, widget=forms.PasswordInput(),
                                       label='Повторити пароль')
    email = forms.EmailField(required=True, label='Електронна пошта')
    first_name = forms.CharField(required=True, label='Ім\'я')
    last_name = forms.CharField(required=True, label='Фамілія')

    username.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})
    password_confirm.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})
    first_name.widget.attrs.update({'class': 'form-control'})
    last_name.widget.attrs.update({'class': 'form-control'})

    error_css_class = 'error'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirm')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        check_mail = User.objects.filter(email=email)

        if len(check_mail) > 0:
            raise forms.ValidationError('Ця електронна адреса вже використовується')

        return email

    def clean_password_confirm(self):
        password_one = self.cleaned_data.get('password')
        password_two = self.cleaned_data.get('password_confirm')
        password_has_num = [True for sym in password_one if sym.isdigit()]

        if password_one != password_two:
            raise forms.ValidationError('Паролі не співпадають')
        if len(password_one) < 8:
            raise forms.ValidationError('Пароль має бути довше 8 символів')
        if not password_one[0].isalpha():
            raise forms.ValidationError('Перший символ у паролі має бути великою літерою')
        if not password_one[0].isupper():
            raise forms.ValidationError('Перший символ у паролі має бути великою літерою')
        if not sum(password_has_num) > 0:
            raise forms.ValidationError('Пароль повинен містити хоча б одне число')

        return password_two


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=25, label='Логін')
    password = forms.CharField(required=True, max_length=30, label='Пароль', widget=forms.PasswordInput())

    username.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})

    def get_text_errors(self):
        return ''.join([i for i in str(self.errors) if i.lower() in ' йцукенгшщзхїфівапролджєячсмитьбю']).strip()

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        check_username = User.objects.filter(username=username)

        if not len(check_username):
            raise ValidationError('Користувача с таким логіном не знайдено')

        check_password = authenticate(username=username, password=password)

        if check_password is None:
            raise forms.ValidationError('Неправильний пароль')

        return self.cleaned_data


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('review_text', 'rating')
