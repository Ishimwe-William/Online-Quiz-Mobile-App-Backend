from django.urls import path

from quiz_api.views import QuizListCreate, QuizDetails, QuestionsListCreate, QuestionDetails

app_name = 'quiz_api'

urlpatterns = [
    # Quiz endpoints
    path('', QuizListCreate.as_view(), name='quizzes-list-create'),
    path('<int:pk>/', QuizDetails.as_view(), name='Quiz-view-update-details'),

    # Question endpoints
    path('<int:pk>/questions/', QuestionsListCreate.as_view(), name='questions-list-create'),
    path('<int:pk>/questions/<int:question_pk>/', QuestionDetails.as_view(), name='Question-view-update-delete'),
]
