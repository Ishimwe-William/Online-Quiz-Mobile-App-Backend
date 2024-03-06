from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404  # Import get_object_or_404

from quiz_api.models import Quiz, Question, Option
from quiz_api.serializers import QuizSerializer, QuestionSerializer, OptionSerializer


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
        question = get_object_or_404(Question, pk=question_pk, quiz__pk=quiz_id)
        return question


class OptionsListCreate(generics.ListCreateAPIView):
    serializer_class = OptionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        quiz_id = self.kwargs['pk']
        question_id = self.kwargs['question_pk']
        question = get_object_or_404(Question, quiz__pk=quiz_id, pk=question_id)

        # Return only options related to the specified question
        return Option.objects.filter(question=question)

    def perform_create(self, serializer):
        quiz_id = self.kwargs['pk']
        question_id = self.kwargs['question_pk']

        # Make sure the question is related to the specified quiz
        question = get_object_or_404(Question, pk=question_id, quiz__pk=quiz_id)

        # Set the question field before saving
        serializer.save(question=question)


class OptionDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        question_id = self.kwargs['question_pk']
        option_pk = self.kwargs['option_pk']
        question = get_object_or_404(Option, pk=option_pk, question_id=question_id)
        return question
