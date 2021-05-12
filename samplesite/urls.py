
from django.contrib import admin
from django.urls import path, include
from bboard.views import BbRedirectView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView,\
                                      PasswordChangeDoneView, PasswordResetView, \
                                      PasswordResetDoneView, PasswordResetConfirmView,\
                                      PasswordResetCompleteView

urlpatterns = [
    path('', BbRedirectView.as_view(), name='old_index' ),
    #path('',include('bboard.urls',namespace=''))
    path('bboard/', include('bboard.urls')), 
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='index'), name='logout'),
    #path('accounts/password_change/', PasswordChangeView.as_view(
         #template_name='registartion/change_password.html'), name='password_change'),
    #path('accounts/password_change/done/', PasswordChangeDoneView.as_view(
         #template_name='registartion/change_password.html'), name='password_change_done'),
    path('accounts/password_reset', PasswordResetView.as_view(),
         #template_name='registartion/reset_password.html', 
         #subject_template_name='registartion/reset_subject.txt',
         #email_template_name='registartion/reset_email.html'),
         name='password_reset'),
    #path('accounts/password_reset/done/', PasswordResetDoneView.as_view(
         #template_name='registartion/email_sent.html'), name='password_reset_done'),
    #path('accounts/reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(
         #template_name='registartion/confirm_password.html'), name='password_reset_confirm'),
    #path('accounts/reset/done/', PasswordResetCompleteView.as_view(
         #template_name='registartion/password_confirmed.html'), name='password_reset_complete'),
    path('accounts/password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
