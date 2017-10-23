from django.core.files.storage import FileSystemStorage
from django.db import models

from ProgWithAlice import settings

fs = FileSystemStorage(location=settings.STATIC_ROOT)


class User(models.Model):
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, null=True)
    photo = models.ImageField(upload_to="main_app/img", storage=fs)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    login = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return "User: " + self.login


class UserLearningDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cur_level = models.IntegerField(default=-1)


class Test(models.Model):
    tid = models.CharField(max_length=5)

    def __str__(self):
        return "Test: " + self.tid

    def get_questions(self):
        return Question.objects.filter(test_id=self).order_by('?')


class Question(models.Model):
    code = models.TextField()
    text = models.TextField()
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return "Question: " + self.text

    def get_answers(self):
        return Answer.objects.filter(question_id=self).order_by('?')


class Answer(models.Model):
    text = models.TextField()
    correct = models.BooleanField()
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return "Answer: " + self.text


class Statistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return "Statistics: user -" + self.user.__str__() + ", test -" + self.test.__str__() + \
               ", score -" + str(self.score)
