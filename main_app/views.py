from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import translation

from django.views.generic import TemplateView

from main_app.mixins import NonAuthenticatedMixin, LevelUndefinedMixin, LevelNotEnoughMixin, LevelAlreadyDefined
from main_app.models import User, Test, Answer, UserLearningDetail, Statistics


class HomePageView(TemplateView):
    template_name = "main_app/index.html"

    def post(self, request, **kwargs):
        login = request.POST.get("login")
        password = request.POST.get("password")

        u = User.objects.filter(login=login, password=password).first()

        if u is None:
            return render(request, "main_app/index.html", {'error': 'Invalid login credentials'})
        else:
            request.session['user'] = u.pk
            return render(request, "main_app/map.html", {'user': u})


class LogoutView(NonAuthenticatedMixin, TemplateView):
    template_name = "main_app/index.html"

    def get(self, request, **kwargs):
        if request.session['user'] is not None:
            del request.session['user']

        return render(request, self.template_name, {})


class RegistrationView(TemplateView):
    template_name = "main_app/registration.html"

    def post(self, request, **kwargs):
        fname = request.POST.get('fname').strip()
        lname = request.POST.get('lname').strip()
        gender = request.POST.get('gender')
        login = request.POST.get('login').strip()
        email = request.POST.get('email').strip()
        phone = request.POST.get('phone').strip()
        password = request.POST.get('password').strip()
        rpassword = request.POST.get('rep-password').strip()

        try:
            photo = request.FILES['photo']
        except:
            if gender is None or gender == 'm':
                photo = '/main_app/img/male.jpg'
            else:
                photo = '/main_app/img/female.png'

        if User.objects.filter(login=login).first() is not None:
            return render(request, "main_app/registration.html", {'error': 'Login is not unique'})

        if password != rpassword:
            return render(request, "main_app/registration.html", {'error': 'Passwords should match'})

        u = User(fname=fname, lname=lname, gender=gender, login=login, email=email, phone=phone, password=password,
                 photo=photo)
        u.save()
        request.session['user'] = u.pk

        user_details = UserLearningDetail(user=u)
        user_details.save()

        return redirect('/first_test')


class FirstTestView(NonAuthenticatedMixin, LevelAlreadyDefined, TemplateView):
    template_name = "main_app/first_test.html"

    def get(self, request, **kwargs):
        test = Test.objects.filter(tid='1-' + translation.get_language()).first()
        return render(request, self.template_name, {'test': test})

    def post(self, request, **kwargs):
        answers = []
        test = Test.objects.filter(tid='1-' + translation.get_language()).first()
        questions = test.get_questions()

        for quest in questions:
            answers.append(int(request.POST.get('group' + str(quest.pk), -1)))

        score = 0
        for ans in answers:
            if ans != -1:
                a = Answer.objects.filter(pk=ans).first()
                if a.correct:
                    score += 1

        percent = score * 100 / len(questions)

        user_id = request.session['user']

        statistics = Statistics(user=User.objects.filter(id=user_id).first(), test=test, score=percent)
        statistics.save()

        cur_level = 1 if percent // 10 == 0 else percent // 10

        user_details = UserLearningDetail.objects.filter(user_id=user_id).first()
        user_details.cur_level = cur_level
        user_details.save()

        percent = str(percent) + "%"

        return render(request, self.template_name, {'res': percent, 'test': test})


class MyPageView(NonAuthenticatedMixin, TemplateView):
    template_name = "main_app/my_page.html"

    def get(self, request, **kwargs):
        u = User.objects.filter(pk=request.session['user']).first()
        d = UserLearningDetail.objects.filter(user_id=u.pk).first()
        return render(request, self.template_name, {"user": u, "detail": d})

    def post(self, request):
        user = User.objects.filter(pk=request.session['user'])
        u = user.first()

        u.fname = request.POST.get('fname', u.fname)
        u.lname = request.POST.get('lname', u.lname)
        u.login = request.POST.get('login', u.login)
        u.email = request.POST.get('email', u.email)
        u.phone = request.POST.get('phone', u.phone)
        try:
            u.photo = request.FILES['photo']
        except:
            pass

        u.save()

        return redirect("/my_page")


class MapView(NonAuthenticatedMixin, LevelUndefinedMixin, TemplateView):
    template_name = 'main_app/map.html'


class Level1View(LevelNotEnoughMixin, TemplateView):
    template_name = 'main_app/lvl1.html'


class Level2View(LevelNotEnoughMixin, TemplateView):
    template_name = 'main_app/lvl2.html'


class Level3View(LevelNotEnoughMixin, TemplateView):
    template_name = 'main_app/lvl3.html'


class Level4View(LevelNotEnoughMixin, TemplateView):
    template_name = 'main_app/lvl4.html'


class Level5View(LevelNotEnoughMixin, TemplateView):
    template_name = 'main_app/lvl5.html'


def go_to_level(request, num):
    return HttpResponse("lvl" + num)


def change_lang(request):
    if 'ru' in request.GET:
        translation.activate('ru')
        request.session['lang'] = 'ru'
    else:
        translation.activate('en')
        request.session['lang'] = 'en'

    request.session[translation.LANGUAGE_SESSION_KEY] = translation.get_language()

    return redirect("/")


def error404(request):
    return render(request, 'main_app/404.html', {'error': request.path + " not found"}, status=404)
