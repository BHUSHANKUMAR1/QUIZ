from django.db import models
from django.contrib.auth.models import User
import random

class Quiz_category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

# class Quiz(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.ForeignKey(Quiz_category,on_delete=models.CASCADE)
#     desc = models.CharField(max_length=500)    
#     number_of_questions = models.IntegerField(default=1)
#     time = models.IntegerField(help_text="Duration of the quiz in seconds", default="1")
    
#     def __str__(self):
#         return self.name

#     def get_questions(self):
#         return self.question_set.all()
    

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)    
    number_of_questions = models.IntegerField(default=1)
    time = models.IntegerField(help_text="Duration of the quiz in minutes", default="1")
    
    def __str__(self):
        return self.name

    def get_questions(self):
        return self.question_set.all()
    
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.content
    
    def get_answers(self):
        return self.answer_set.all()
        
class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"question: {self.question.content}, answer: {self.content}, correct: {self.correct}"
    
class Marks_Of_User(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    score = models.FloatField()
    user_responses = models.JSONField()
    
    def __str__(self):
        return f'{self.user.id} {self.user} {self.quiz} {self.score} '
