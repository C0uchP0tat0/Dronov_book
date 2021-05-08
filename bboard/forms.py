from django.forms import ModelForm
from django.forms import modelform_factory, DecimalField
from django.forms.widgets import Select


from .models import Bb, Rubric

'''BbForm = modelform_factory(Bb,
         fields = ('title', 'content', 'price', 'rubric'),
         labels = {'title': 'Название товара'},
         help_texts = {'rubric': 'Не забудьте выбрать рубрику'},
         field_classes = {'price': DecimalField},
         widgets = {'rubric': Select(attrs={'size': 8})})'''

class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Название товара'}
        help_texts = {'rubric': 'Не забудьте выбрать рубрику'}
        field_classes = {'price': DecimalField}
        widgets = {'rubric': Select(attrs={'size': 8})}
        