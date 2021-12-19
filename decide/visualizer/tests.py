from django.test import TestCase
import visualizer.views as vw

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from django.utils import timezone
from base.tests import BaseTestCase
from voting.tests import VotingTestCase
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from django.conf import settings
import time

# Create your tests here.

class VisualizerTestCase(TestCase):

    def testDateComparer(self):
        """
        Comprueba que la función DateComparer del views del
        módulo visualizer funciona correctamente.
        """
        fecha1="2021-12-18T10:48:22.969419Z"
        fecha2="2021-12-18T11:07:51.009086Z"
        resultado="0 días, 0 horas, 19 minutos y 28 segundos "
        diferencia = vw.dateComparer(fecha1,fecha2)[0]
        self.assertEqual(diferencia, resultado)
        
        