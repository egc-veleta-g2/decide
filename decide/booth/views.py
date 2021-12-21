import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404

from voting.models import Voting
from base import mods


# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        context = obtener_votacion(context, vid)
        return context


class BoothUrlView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vurl = kwargs.get('voting_url')

        v = get_object_or_404(Voting, url=vurl)

        context = obtener_votacion(self, context, v.id)

        return context


def obtener_votacion(self, context, vid):
    try:
        r = mods.get('voting', params={'id': vid})

        # Casting numbers to string to manage in javascript with BigInt
        # and avoid problems with js and big number conversion
        for k, v in r[0]['pub_key'].items():
            r[0]['pub_key'][k] = str(v)

        context['voting'] = json.dumps(r[0])

    except:
        raise Http404

    context['KEYBITS'] = settings.KEYBITS

    return context