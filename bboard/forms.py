from django.forms import ModelForm
from django.forms import modelform_factory, DecimalField
from django.forms.widgets import Select
from django import forms
from django.core.exceptions import ValidationError


from .models import Bb, Rubric


class BbForm(ModelForm):
    title = forms.CharField(label='Название товара')
    content = forms.CharField(label='Описание', 
              widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
             label='Рубрика', help_text='Не забудьте выбрать рубрику!',
             widget=forms.widgets.Select(attrs={'size': 8}))
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
        