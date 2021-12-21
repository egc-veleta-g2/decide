import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods


# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voting_id = kwargs.get('voting_id', 0)
        context['voting_id'] = voting_id
        question_id = kwargs.get('question_id', 0)
        context['question_id']=question_id

        context['token'], context['voter'], voter_id = get_user(self)
        context['KEYBITS'] = settings.KEYBITS

        try:
            r = mods.get('voting', params={'id': voting_id})
            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            number_of_questions = len(r[0]['question'])
            current_question_position = question_position_by_id(r[0]['question'], question_id)

            check_next_question(context, current_question_position, number_of_questions, r)

            store_voting_and_question(context, current_question_position, r)

            check_user_has_voted_question(context, voting_id, question_id, voter_id)

        except:
            raise Http404("This voting does not exist")

        return context
