from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render, redirect

from main_app.models import UserLearningDetail


class NonAuthenticatedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('user', -1) == -1:
            return render(request, 'main_app/index.html', {'error': 'Authenticate first'})

        return super(NonAuthenticatedMixin, self).dispatch(request, *args, **kwargs)


class LevelUndefinedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user_id = request.session['user']
        user_details = UserLearningDetail.objects.filter(user_id=user_id).first()
        if user_details.cur_level == -1:
            return render(request, 'main_app/first_test.html', {'error': 'You should pass this test first'})

        return super(LevelUndefinedMixin, self).dispatch(request, *args, **kwargs)


class LevelAlreadyDefined(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user_id = request.session['user']
        user_details = UserLearningDetail.objects.filter(user_id=user_id).first()
        if user_details.cur_level != -1:
            return render(request, 'main_app/map.html', {'error': 'You have already passed the first test'})

        return super(LevelAlreadyDefined, self).dispatch(request, *args, **kwargs)


class LevelNotEnoughMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user_id = request.session['user']
        user_details = UserLearningDetail.objects.filter(user_id=user_id).first()

        url = request.path.split('/')
        lvl = url[len(url) - 1]

        num = lvl[3:]

        if user_details.cur_level < int(num):
            return render(request, 'main_app/map.html', {'error': 'Your level is not enough for this level'})

        return super(LevelNotEnoughMixin, self).dispatch(request, *args, **kwargs)
