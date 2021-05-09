from django.urls import path

from .views import BbCreateView, BbDetailView, BbByRubricView, index, edit, delete
#from .views import index, by_rubric, add_and_save, BbAddView, BbIndexView, BbEditView, BbDeleteView,

#app_name = 'bboard'
urlpatterns = [
    #path ('bb_confirm_delete/<int:pk>', BbDeleteView.as_view(), name='bb_confirm_delete'),
    #path ('bb_form/<int:pk>', BbEditView.as_view(), name='bb_form'),
    path ('add/', BbCreateView.as_view(), name='add'),
    path ('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path ('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    #path ('', BbIndexView.as_view(), name='index'),
    #path ('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbDetailView.as_view(), name='detail'),
    #path ('add/', BbAddView.as_view(), name='add'),
    path ('bb_confirm_delete/<int:pk>', delete, name='bb_confirm_delete'),
    path ('bb_form/<int:pk>', edit, name='bb_form'),
    path ('', index, name='index'),
    #path ('add/', add_and_save, name='add'),
    #path ('<int:rubric_id>/', by_rubric, name='by_rubric'),
]