from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404  # Import get_object_or_404

from quiz_api.models import Quiz, Question
from quiz_api.serializers import QuizSerializer, QuestionSerializer


class QuizListCreate(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]


class CreateQuiz(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]


class QuizDetails(generics.RetrieveUpdateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]


class QuestionsListCreate(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        quiz_id = self.kwargs['pk']  # Get the quiz ID from the URL parameters
        quiz = get_object_or_404(Quiz, pk=quiz_id)  # Get the quiz or return a 404 response if not found
        return Question.objects.filter(quiz=quiz)  # Filter questions based on the specified quiz

    def perform_create(self, serializer):
        # Get the quiz instance based on the quiz_id in the request data
        quiz_id = self.kwargs['pk']
        quiz = get_object_or_404(Quiz, pk=quiz_id)

        # Set the quiz field before saving
        serializer.save(quiz=quiz)


class QuestionDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        quiz_id = self.kwargs['pk']
        question_pk = self.kwargs['question_pk']
        quiz = get_object_or_404(Question, pk=question_pk, quiz_id=quiz_id)
        return quiz
