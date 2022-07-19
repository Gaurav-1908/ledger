from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    #path('studentLogin', views.studentLogin),
    path('studentDash', views.studentDash),
    path('register', views.register),
    # path('teacherLogin', views.teacherLogin),
    # path('adminLogin', views.adminLogin),
    path('teacherDash', views.teacherDash),
    path('logout',views.logout),
    # path('adminDash', views.adminDash),
    # path('acceptUser', views.acceptUser),
    # path('rejectUser', views.rejectUser),
    # path('add-teacher', views.add_teacher),
    # path('add-admin', views.add_admin),
    # path('accepted',views.accepted),
    # path('removeTeacher', views.remove_teacher),
    # path('deleteAdmin', views.delete_admin),
    path('createEvent', views.createEvent),
    path('login', views.login),
]