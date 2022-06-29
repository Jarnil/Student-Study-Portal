from django.urls import path, include
from Dashboard import views

app_name = 'Dashboard'

urlpatterns = [
    path('',views.index,name='index'),
    path('index/', views.index,name='index'),
    path('user_index/',views.user_index,name='user_index'),
    path('notes/',views.notes,name='notes'),
    path('delete_notes/<int:pk>',views.delete_notes,name='delete_notes'),
    path('notes_detail/<int:pk>',views.NotesDetailView.as_view(),name='notes_detail'),
    path('youtube/',views.youtube,name='youtube'),
    path('wikipedia/',views.wikipedia,name='wikipedia'),
    path('homework/',views.homework,name="homework"),
    path('update_homework/<int:pk>',views.update_homework,name="update_homework"),
    path('delete_homework/<int:pk>',views.delete_homework,name="delete_homework"),
    path('books/',views.books,name="books"),
    path('todo/',views.todo,name='todo'),
    path('update_todo/<int:pk>',views.update_todo,name="update_todo"),
    path('delete_todo/<int:pk>',views.delete_todo,name="delete_todo"),
    path('dictionary/',views.dictionary,name='dictionary'),
    path('profile/',views.profile,name='profile'),
]
