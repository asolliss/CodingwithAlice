import random
import time
from django.test import LiveServerTestCase
from django.test import TestCase
from django.test import override_settings
from mixer.main import mixer
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.safari.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from main_app.models import User


class LoginTest(TestCase):
    def setUp(self):
        self.user = User(login='alice', password='alice')
        self.user.save()

    def testExists(self):
        self.assertEqual(User.objects.get(login='alice', password='alice'), self.user)
        self.assertFalse(User.objects.filter(login='alice1', password='alice').exists(), False)

    def testInsert(self):
        st = time.time()
        u = User(login='aaa', password='aaa')
        u.save()
        print(time.time() - st)

        assert True


class SeleniumTestCase(LiveServerTestCase):
    def setUp(self):
        u = User(login='alice', password='alice')
        u.save()

        self.wd = WebDriver()

    def tearDown(self):
        self.wd.quit()

    def test_login_success(self):
        self.wd.get("http://127.0.0.1:8000")
        self.wd.find_element_by_id('login').send_keys("alice")
        self.wd.find_element_by_id("password").send_keys('alice')
        self.wd.find_element_by_id('sign_in').click()

        time.sleep(3)

        assert "Level map" or "Карта уровней" in self.wd.title

    def test_login_fail(self):
        self.wd.get("http://127.0.0.1:8000")
        self.wd.find_element_by_id('login').send_keys("something")
        self.wd.find_element_by_id("password").send_keys('else')
        self.wd.find_element_by_id('sign_in').click()

        time.sleep(3)

        assert "Login" or "Логин" in self.wd.title

    def test_register_success(self):
        self.wd.get("http://127.0.0.1:8000/register")
        self.wd.find_element_by_name('fname').send_keys("something")
        self.wd.find_element_by_name('lname').send_keys("something")
        self.wd.find_elements_by_css_selector("input[type='radio'][value='m']")[0].click()
        self.wd.find_element_by_name('email').send_keys("some@gmail.com")
        self.wd.find_element_by_name('phone').send_keys("+38(099)-111-11-11")
        self.wd.find_element_by_name('login').send_keys("some")
        self.wd.find_element_by_name('password').send_keys("some")
        self.wd.find_element_by_name('rep-password').send_keys("some")
        self.wd.find_element_by_id('submit-reg').click()

        time.sleep(3)

        assert "First test" or "Начальный тест" in self.wd.title

    def test_register_fail_login_not_unique(self):
        self.wd.get("http://127.0.0.1:8000/register")
        self.wd.find_element_by_name('fname').send_keys("something")
        self.wd.find_element_by_name('lname').send_keys("something")
        self.wd.find_elements_by_css_selector("input[type='radio'][value='m']")[0].click()
        self.wd.find_element_by_name('email').send_keys("some@gmail.com")
        self.wd.find_element_by_name('phone').send_keys("+38(099)-111-11-11")
        self.wd.find_element_by_name('login').send_keys("alice")
        self.wd.find_element_by_name('password').send_keys("some")
        self.wd.find_element_by_name('rep-password').send_keys("some")
        self.wd.find_element_by_id('submit-reg').click()

        time.sleep(3)

        assert "Registration" or "Регистрация" in self.wd.title

    def test_register_fail_passwords_not_match(self):
        self.wd.get("http://127.0.0.1:8000/register")
        self.wd.find_element_by_name('fname').send_keys("something")
        self.wd.find_element_by_name('lname').send_keys("something")
        self.wd.find_elements_by_css_selector("input[type='radio'][value='m']")[0].click()
        self.wd.find_element_by_name('email').send_keys("some@gmail.com")
        self.wd.find_element_by_name('phone').send_keys("+38(099)-111-11-11")
        self.wd.find_element_by_name('login').send_keys("some")
        self.wd.find_element_by_name('password').send_keys("some")
        self.wd.find_element_by_name('rep-password').send_keys("not some")
        self.wd.find_element_by_id('submit-reg').click()

        time.sleep(3)

        assert "Registration" or "Регистрация" in self.wd.title

    def test_change_info_on_my_page(self):
        self.wd.get("http://127.0.0.1:8000")
        self.wd.find_element_by_id('login').send_keys("alice")
        self.wd.find_element_by_id("password").send_keys('alice')
        self.wd.find_element_by_id('sign_in').click()

        time.sleep(3)

        self.wd.get("http://127.0.0.1:8000/my_page")

        self.wd.find_element_by_id('fname').send_keys("something")
        self.wd.find_element_by_id('sbm-changes').click()

        time.sleep(3)

        assert self.wd.find_element_by_id('fname').get_attribute('value') == 'something'
