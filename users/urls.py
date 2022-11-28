from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('personal', views.personal, name='personal'),
    path('appointment/<int:id>/<str:day>/<int:h>', views.appointment, name='appointment'),
    path('search/appointment', views.search_appointment, name = 'search_appointment'),
    path('search/appointment/<str:object>/<str:name>', views.search, name = 'search'),
    path('treatment', views.treatment, name='treatment'),
    path('send/<str:chatroom_id>', views.send, name="send"),
    path('updateMessages/<str:chatroom_id>', views.updateMessages, name='updateMessages')
]