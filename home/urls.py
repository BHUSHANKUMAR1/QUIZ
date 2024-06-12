from django.urls import path
from . import views

urlpatterns = [

    path("signup/", views.Signup, name="signup"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
  
    path("", views.qzz, name="qzz"),
    path("<int:quiz_id>/", views.quiz_questions, name="quiz_questions"),
    path('<int:quiz_id>/submit/', views.submit, name='submit'),
    path("result/", views.result, name="result"),
    path("result/<int:res_id>/", views.result_description, name="result_description"),
    path("add_quiz", views.add_quiz, name="add_quiz"),
    path("add_question/", views.add_question, name="add_question"),
    path("add_option/<int:que_id>/", views.add_option, name="add_option"),
    path("delete_result/<int:res_id>/", views.delete_result, name="delete_result"),
    path("delete_question/<int:que_id>/", views.delete_question, name="delete_question"),
    path("delete_quiz/<int:quiz_id>/", views.delete_quiz, name="delete_quiz"),
    path("search_quiz", views.search_quiz, name="search_quiz"),
    
]
