import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods
from store.models import Vote
from voting.models import Voting
from census.models import Census



# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})

            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            context['voting'] = json.dumps(r[0])
            context['rank_order'] = int(r[0]['question']['option_types']) == 2
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context


class InicioView(TemplateView):
    template_name = 'booth/inicio.html'


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['listVotados']= self.get_queryset()[0]
        context['listNoVotados']= self.get_queryset()[1]
        context['usuario'] = self.request.user

        return context


    def get_queryset(self):
        votaciones = Voting.objects.all()
        mis_votos = Vote.objects.filter(voter_id= self.request.user.id)
        mis_censos = Census.objects.filter(voter_id= self.request.user.id)

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

        return list_votados, list_noVotados