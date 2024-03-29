from django.urls import path

from quiz_api.views import QuizListCreate, TakeQuiz, QuestionsListCreate, QuestionDetails, OptionsListCreate, \
    OptionDetails, QuestionWithOptions, RetrieveUpdateDeleteQuiz

app_name = 'quiz_api'

urlpatterns = [
    # Quiz endpoints
    path('', QuizListCreate.as_view(), name='quizzes-list-create'),
    path('<int:pk>/', RetrieveUpdateDeleteQuiz.as_view(), name='Quiz-view-update-details'),

    # Question endpoints
    path('<int:pk>/questions/', QuestionsListCreate.as_view(), name='questions-list-create'),
    path('<int:pk>/questions/<int:question_pk>/', QuestionDetails.as_view(), name='Question-view-update-delete'),

    # Option endpoints
    path('<int:pk>/questions/<int:question_pk>/options/', OptionsListCreate.as_view(), name='options-list-create'),
    path('<int:pk>/questions/<int:question_pk>/options/<int:option_pk>/', OptionDetails.as_view(),
         name='option-view-update-delete'),

    # UserAnswer endpoints
    path('<int:pk>/questions/<int:question_pk>/take-quiz/', QuestionWithOptions.as_view(), name='question-with-options'),
    # take quiz endpoints
    path('<int:pk>/take-quiz/', TakeQuiz.as_view(), name='take-quiz'),

]
