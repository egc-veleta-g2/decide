from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from base.tests import BaseTestCase
from census.models import Census
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption


# Create your tests here.
class BoothTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def create_voting_url(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q, url='palabra')
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

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

    def test_custom_url(self):
        v = self.create_voting_url()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        response = self.client.get('/booth/palabra', format = 'json')
        self.assertEqual(response.status_code,301)

    def test_custom_no_url(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        response = self.client.get('/booth/'+str(v.id), format = 'json')
        self.assertEqual(response.status_code,301)

    def test_custom_no_slash(self):
        v = self.create_voting()
        self.create_voters(v)

        palabra = '/'

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        response = self.client.get('/booth/'+palabra, format = 'json')
        self.assertEqual(response.status_code,404)




