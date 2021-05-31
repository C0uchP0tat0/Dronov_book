from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, HttpResponseForbidden
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.dates import ArchiveIndexView, DateDetailView
from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from precise_bbcode.bbcode import get_parser

from .models import Bb, Rubric
from .forms import BbForm

class BbRedirectView(RedirectView):
    url='/bboard/'

def index(request):
    
        bbs = Bb.objects.order_by()
        rubrics = Rubric.objects.all()
        paginator = Paginator(bbs, 2)
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        context = {'bbs': page.object_list, 'rubrics' : rubrics, 'page': page}
        return render(request, 'bboard/index.html', context)

def search(request):
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            bbs = Bs.objects.filter()
            context = {'bbs': bbs}
            return render(request, 'bboard/search_result.html', context)
    else:
        sf = SearchForm()
    context = {'form': sf}
    return render(request, 'bboard/search.html', context)

    

'''class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context'''     

class BbByRubricView(SingleObjectMixin,ListView):
    template_name = 'bboard/by_rubric.html'
    pk_url_kwarg = 'rubric_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset = Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_rubric'] = self.object
        context['rubrics'] = Rubric.objects.all()
        context['bbs'] = context['object_list']
        return context

    def get_queryset(self):
        return self.object.bb_set.all()
      
class BbCreateView(LoginRequiredMixin, CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

'''class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context'''

def edit(request, pk):
    bb = Bb.objects.get(pk=pk)
    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            bb.save()
            return HttpResponseRedirect(reverse('by_rubric',
                   kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_form.html', context)
    else:
        bbf = BbForm(instance=bb)
        context = {'form': bbf}
        return render(request, 'bboard/bb_form.html', context)

'''class BbDeleteView(DeleteView):
    model = Bb
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context'''

def delete(request, pk):
    parser = get_parser()
    bb = Bb.objects.get(pk=pk)
    parsed_content = parser.render(bb.content)
    if request.method == 'POST':
        bb.delete()
        return HttpResponseRedirect(reverse('by_rubric',
               kwargs={'rubric_id': bb.rubric.pk}))
    else:
        context = {'bb': bb}
        return render(request, 'bboard/bb_confirm_delete.html', context)

class BbDetailView(DetailView):
    model = Bb
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

@login_required(login_url='/accounts/login/')
def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name',),
                                          can_delete=True, can_order=True,)
    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    rubric = form.save(commit=False)
                    rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    rubric.save()
            return redirect('index')
    else:
        formset = RubricFormSet()
    context = {'formset': formset}
    return render(request, 'bboard/rubrics.html', context)

def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.method == 'POST':
        formset = BbsFormSet(request.POST, instance=rubric)
        if formset.is_valid():
            formset.save()
            return redirect('index')
    else:
        formset = BbsFormSet(instance=rubric)
    context = {'formset': formset, 'current_rubric': rubric}
    return render(request, 'bboard/bbs.html', context)
'''def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name',),
                                                 can_delete=True)
    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('index')
    else:
        formset = RubricFormSet()
    context = {'formset': formset}
    return render(request, 'bboard/rubrics.html', context)'''


'''class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context'''

'''class BbDetailView(DateDetailView):
    model = Bb
    date_field = 'published'
    month_format = '%m'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context'''

'''class BbIndexView(TemplateView):
    template_name = 'bboard/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bbs'] = Bb.objects.all()
        context['rubrics'] = Rubric.objects.all()
        return context'''

'''class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price' : 0.0}

    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('by_rubric',
            kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})'''

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
