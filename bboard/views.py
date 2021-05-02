from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from .models import Bb, Rubric
from .forms import BbForm

class BbIndexView(TemplateView):
    template_name = 'bboard/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bbs'] = Bb.objects.all()
        context['rubrics'] = Rubric.objects.all()
        return context        

class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context
      
class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

'''def index(request):
    bbs = Bb.objects.order_by()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics' : rubrics}
    return TemplateResponse(request, 'bboard/index.html', context)'''

'''def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics' : rubrics, 'current_rubric': current_rubric}
    return render (request, 'bboard/by_rubric.html', context)''' 

'''def add_and_save(request):
    if request.method == 'POST':
        bbf=BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric', 
                   kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context={'form': bbf}
            return render (request, 'bboard/create.html', context)
    else:
        bbf=BbForm()
        context = {'form': bbf}
        return render (request, 'bboard/create.html', context)'''
