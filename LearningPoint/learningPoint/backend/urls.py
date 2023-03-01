from django.urls import path

from backend import api

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login', api.LoginView.as_view(), name='login'),
    path('logout', api.LogoutView.as_view(), name='logout'),
    path('register', api.RegisterView.as_view(),
         name='register'),
    path('activate/<id>/<uidb64>/<token>',
         api.ActivateView.as_view(), name='activate'),
    path('profile', api.ProfileView.as_view(), name='profile'),
    path('update-profile/<id>', api.ProfileUpdateView.as_view(),
         name='update_profile'),
    path('change-password', api.ChangePasswordView.as_view(),
         name='change_password'),
    path('reset-password', api.ResetPasswordView.as_view(), name='reset_password'),
    path(
        'reset-password/<uidb64>/<token>',
        api.ResetPasswordConfirmView.as_view(),
        name='reset_password_confirm'
    ),
    path(
        'reset-password/complete',
        api.ResetPasswordCompleteView.as_view(),
        name='reset_password_complete'
    ),
    path('create-appointment', api.AppointmentCreateView.as_view(),
         name='create_appointment'),
    path('view-appointment-list', api.AppointmentListView.as_view(),
         name='view_appointment_list'),
    path('view-booked-appointment-list', api.AppointmentBookedListView.as_view(),
         name='view_booked_appointment_list'),
    path('update-appointment/<id>', api.AppointmentUpdateView.as_view(),
         name='update_appointment'),
    path('delete-appointment/<id>', api.AppointmentDeleteView.as_view(),
         name='delete_appointment'),
    path('book-appointment/<id>', api.AppointmentBookView.as_view(),
         name='book_appointment'),
    path('unbook-appointment/<id>', api.AppointmentUnbookView.as_view(),
         name='unbook_appointment'),
]
