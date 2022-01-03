import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import override_settings

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from store.models import Vote


class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_quick_poll(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q, poll=True)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def store_concrete_vote(self, v, voter):
        a, b = self.encrypt_msg(v.question.options.all()[0].number, v)
        data = {
            'voting': v.id,
            'voter': voter.voter_id,
            'vote': { 'a': a, 'b': b },
        }
        user = self.get_or_create_user(voter.voter_id)
        self.login(user=user.username)
        mods.post('store', json=data)

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')


    def test_delete_voting(self):
        self.login()
        #Eliminamos todas las votaciones que hay hasta el momento
        while Voting.objects.count() !=0:
            data = {'_selected_action':'1','action': 'delete_selected'}
            response = self.client.post('/admin/voting/voting/', data)
            self.assertEqual(response.status_code, 302)

    def test_choose_question(self):
        self.login()
        #Comprobamos que la vista de elección de tipo de pregunta funciona correctamente
        data = {'type_ratio': 'm'}
        response = self.client.post('/voting/type/', data)
        self.assertEqual(response.status_code, 302)

        data = {'type_ratio': 'd'}
        response = self.client.post('/voting/type/', data)
        self.assertEqual(response.status_code, 302)

    def test_dichotomous_voting(self):
        self.login()
        #Comporbamos que se puede realizar una pregunta dicotómica
        data = {'question_desc': 'Example','question_ratio':'SI/NO'}
        response = self.client.post('/voting/dichotomy', data)
        self.assertEqual(response.status_code, 301)

        #Comporbamos que se puede realizar una votación con la pregunta dicotómica creada anteriormente
        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})

        data = {'name': 'V1','desc':'Descrip','question':'Example','auths':a}
        response = self.client.put('/admin/voting/voting/add', data)
        self.assertEqual(response.status_code, 301)

    def create_dich_voting(self):
        q = Question(desc='Example')
        q.save()
        for i in range(2):
            if i == 0:
                o='SI'
            else:
                o='NO'
            opt = QuestionOption(question=q, option=o)
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def test_correct_option_question(self):
        self.login()
        #En esta función comprobaremos que los diferentes tipos de preguntas dicotómicas se crean con el nombre correcto
        v = self.create_dich_voting()
        self.create_voters(v)
        questSI = QuestionOption.objects.filter(question__desc='Example')[0]
        questNO = QuestionOption.objects.filter(question__desc='Example')[1]
        self.assertEqual(questSI.option,'SI')
        self.assertEqual(questNO.option,'NO')


    def test_update_dichotomous_voting(self):
        self.login()
        #Comprobamos que la votación con la pregunta dicotómica puede pasar por todos los estados correctamente
        data = {'_selected_action':'1','action': 'start'}
        response = self.client.post('/admin/voting/voting/', data)
        self.assertEqual(response.status_code, 302)

        data = {'_selected_action':'1','action': 'stop'}
        response = self.client.post('/admin/voting/voting/', data)
        self.assertEqual(response.status_code, 302)

        data = {'_selected_action':'1','action': 'tally'}
        response = self.client.post('/admin/voting/voting/', data)
        self.assertEqual(response.status_code, 302)

        data = {'_selected_action':'1','action': 'delete_selected'}
        response = self.client.post('/admin/voting/voting/', data)
        self.assertEqual(response.status_code, 302)

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_create_wrong_dichotomy_voting(self):
        # Creación con opciones de preguntas incorrectas
        descripcion = 'Descripción de ejemplo'
        data = {'question_desc': descripcion, 'question_ratio':'incorrecto'}
        self.login()
        response = self.client.put('/voting/dichotomy/', data, format='json')
        self.assertEqual(response.status_code, 200)

        data = {'question_desc': '', 'question_ratio':'SI/NO'}
        self.login()
        response = self.client.put('/voting/dichotomy/', data, format='json')
        self.assertEqual(response.status_code, 200)

        # Creación con ambos campos incorrectos
        data = {'question_desc': '', 'question_ratio':'incorrecto'}
        self.login()
        response = self.client.put('/voting/dichotomy/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_check_start_voting(self):
        self.login()
        v = self.create_voting()
        data = {'_selected_action':'1','action': 'reset'}
        self.client.post('/admin/voting/voting/', data)
        # Comprobamos que las fechas de inicio y fin de la votación han sido reseteadas
        self.assertEqual(Voting.objects.filter(id=v.id)[0].start_date, None)
        self.assertEqual(Voting.objects.filter(id=v.id)[0].end_date, None)

    def test_complete_quick_poll(self):
        v = self.create_quick_poll()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])


    def test_voting_list_undone(self):
        v = self.create_voting()
        self.create_voters(v)

        usuario = list(Census.objects.filter(voting_id=v.id))[0].voter_id

        votaciones = Voting.objects.all()
        mis_votos = Vote.objects.filter(voter_id=usuario)
        mis_censos = Census.objects.filter(voter_id=usuario)

        list_votados = set()
        for v in votaciones:
            for voto in mis_votos:
                if voto.voting_id == v.id:
                    list_votados.add(v)

        list_noVotados = []
        for v in votaciones:
            for c in mis_censos:
                if v.id == c.voting_id and v not in list_votados:
                    list_noVotados.append(v)

        self.assertEquals(list_noVotados[0], v)


    def test_voting_list_done(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        usuario = list(Census.objects.filter(voting_id=v.id))[0]

        self.store_concrete_vote(v, usuario)

        votaciones = Voting.objects.all()
        mis_votos = Vote.objects.filter(voter_id=usuario.voter_id)

        list_votados = set()
        for v in votaciones:
            for voto in mis_votos:
                if voto.voting_id == v.id:
                    list_votados.add(v)

        self.assertEquals(list(list_votados)[0], v)

    def test_quick_poll_list_undone(self):
        v = self.create_quick_poll()
        self.create_voters(v)

        usuario = list(Census.objects.filter(voting_id=v.id))[0].voter_id

        votaciones = Voting.objects.all()
        mis_votos = Vote.objects.filter(voter_id=usuario)
        mis_censos = Census.objects.filter(voter_id=usuario)

        list_votados = set()
        for v in votaciones:
            for voto in mis_votos:
                if voto.voting_id == v.id:
                    list_votados.add(v)

        list_noVotados = []
        for v in votaciones:
            if v.poll == True and v not in list_votados:
                list_noVotados.append(v)
            else:
                for c in mis_censos:
                    if v.id == c.voting_id and v not in list_votados:
                        list_noVotados.append(v)

        self.assertEquals(list_noVotados[0], v)


    def test_quick_poll_list_done(self):
        v = self.create_quick_poll()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        usuario = list(Census.objects.filter(voting_id=v.id))[0]

        self.store_concrete_vote(v, usuario)

        votaciones = Voting.objects.all()
        mis_votos = Vote.objects.filter(voter_id=usuario.voter_id)

        list_votados = set()
        for v in votaciones:
            for voto in mis_votos:
                if voto.voting_id == v.id:
                    list_votados.add(v)

        self.assertEquals(list(list_votados)[0], v)