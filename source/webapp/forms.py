from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator, MinLengthValidator
from django.forms import Textarea

from webapp.models import Task


class CustomLengthValidator(BaseValidator):
    def __init__(self, limit_value=30):
        message = ('Максимальная длина заголовка %(limit_value)s. Вы ввели %(show_value)s символов.')
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return value > limit_value

    def clean(self, value):
        return len(value)


# Проверка на цифру в начале строки
def find_number_left(string):
    try:
        int(string[0])
    except ValueError:
        return
    raise ValidationError('Нельзя начинать с цифры!')


# Проверка регистра первого символа строки
def first_char_upper(string):
    res = (string[0]).isupper()
    if not res:
        raise ValidationError('Нельзя начинать с нижнего регистра!')


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        max_length=50,
        validators=(
            MinLengthValidator(
                limit_value=2,
                message='Минимальная длина заголовка - 2!'
            ),
            CustomLengthValidator(),
            find_number_left
        ),
        label='Заголовок задачи'
    )
    description = forms.CharField(
        max_length=3000,
        label='Описание задачи',
        widget=Textarea,
        validators=(first_char_upper,)
    )

    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'type')
        labels = {
            'title': 'Заголовок задачи',
            'description': 'Описание задачи',
            'status': 'Статус',
            'type': 'Тип'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise ValidationError('Заголовок должен быть длинее 2-ух символов')
        return title
