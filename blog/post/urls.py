from django.urls import path

from post import views

app_name = 'post'
urlpatterns = [
    path('new/', views.new, name='new'),
    path('list/', views.list, name='list'),
    path('detail/<int:id>', views.detail, name='detail'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('comment_delete/<int:id>/<int:comment_id>', views.comment_delete, name='comment_delete'),
]