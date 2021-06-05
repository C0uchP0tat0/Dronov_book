from django.forms import ModelForm, formset_factory
from django.forms import modelform_factory, DecimalField
from django.forms.widgets import Select
from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from django.core import validators


from .models import Bb, Rubric, Img


class BbForm(ModelForm):
    title = forms.CharField(label='Название товара')
    content = forms.CharField(label='Описание', 
              widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
             label='Рубрика', help_text='Не забудьте выбрать рубрику!',
             widget=forms.widgets.Select(attrs={'size': 8}))
    captcha = CaptchaField(label='Введите текст с картинки',
              error_messages={'invalid': 'Неправильный текст'})
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Укажите описание товара')
        if self.cleaned_data['price'] < 0:
            errors['price'] = ValidationError('Укажите не отрицательное значение цены')
        if errors:
            raise ValidationError(errors)

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
             label='Рубрика')

fs = formset_factory(SearchForm, extra=3, can_delete=True)

class ImgForm(forms.ModelForm):
    img = forms.ImageField(label='Изображение',
          validators=[validators.FileExtensionValidator(
          allowed_extensions=('gif', 'jpg', 'png'))],
          error_messages={'invalid_extension': 'Этот формат файла' + \
          'не поддерживается'})
    desc = forms.CharField(label='Описание',
                           widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'
        

'''class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Пароль (повторно)')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')'''
            
        
'''BbForm = modelform_factory(Bb,
         fields = ('title', 'content', 'price', 'rubric'),
         labels = {'title': 'Название товара'},
         help_texts = {'rubric': 'Не забудьте выбрать рубрику'},
         field_classes = {'price': DecimalField},
         widgets = {'rubric': Select(attrs={'size': 8})})'''

'''class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Название товара'}
        help_texts = {'rubric': 'Не забудьте выбрать рубрику'}
        field_classes = {'price': DecimalField}
        widgets = {'rubric': Select(attrs={'size': 8})}'''
        