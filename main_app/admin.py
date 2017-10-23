from django.contrib import admin

from main_app.models import User, Test, Question, Answer, UserLearningDetail, Statistics

admin.site.register(User)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserLearningDetail)
admin.site.register(Statistics)
