from django.urls import path

from .views import BbIndexView, BbCreateView, BbDetailView, BbByRubricView
#from .views import index, by_rubric, add_and_save,

urlpatterns = [
    path ('add/', BbCreateView.as_view(), name='add'),
    path ('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path ('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path ('', BbIndexView.as_view(), name='index'),
    #path ('', index, name='index'),
    #path ('add/', add_and_save, name='add'),
    #path ('<int:rubric_id>/', by_rubric, name='by_rubric'),
]