import os
from xml.sax import handler, make_parser

from ProgWithAlice import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProgWithAlice.settings')

import django

django.setup()

from main_app.models import Answer, Question, Test


class Sax(handler.ContentHandler):
    def __init__(self):
        handler.ContentHandler.__init__(self)
        self.test = None
        self.cur_quest = None
        self.cur_ans = None

    def startDocument(self):
        pass

    def startElement(self, name, attrs):
        if name == "test":
            self.test = Test()
            self.test.tid = attrs.get("id")
            self.test.save()
        elif name == "question":
            self.cur_quest = Question()
            self.cur_quest.text = attrs.get("text")
            self.cur_quest.code = attrs.get("code")
            self.cur_quest.test_id = self.test
            self.cur_quest.save()
        elif name == "answer":
            self.cur_ans = Answer()
            self.cur_ans.correct = bool(attrs.get("correct"))
            self.cur_ans.text = attrs.get("text")
            self.cur_ans.question_id = self.cur_quest
            self.cur_ans.save()

    def endElement(self, name):
        pass

    def characters(self, content):
        pass

    def ignorableWhitespace(self, content):
        pass

    def processingInstruction(self, target, data):
        pass


def process_sax(xmlname):
    parser = make_parser()
    parser.setContentHandler(Sax())
    parser.parse(xmlname)

if __name__ == '__main__':
    Test.objects.all().delete()
    process_sax(settings.STATIC_ROOT+'/main_app/xml/test0_ru')
    process_sax(settings.STATIC_ROOT+'/main_app/xml/test0_en')


