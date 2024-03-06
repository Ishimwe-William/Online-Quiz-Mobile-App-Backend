from django.db import models
from django.utils.text import slugify

from users.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, editable=False,)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generate the slug only if the instance is being created
        if not self.id:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    point_value = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.text} (Quiz: {self.quiz.title})"


class Option(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text} (Question: {self.question.text})"


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, db_index=True)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_score(self):
        user_answers = UserAnswer.objects.filter(question__quiz=self.quiz, user=self.user,
                                                 selected_option__is_correct=True)
        score = sum(answer.question.point_value for answer in user_answers)
        return score

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - Score: {self.score}"


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    selected_option = models.ForeignKey('Option', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')
