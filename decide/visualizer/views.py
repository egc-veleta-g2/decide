import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from voting.models import Voting
from census.models import Census
from datetime import datetime
from base import mods


class VisualizerInicioView(TemplateView):
    template_name = 'visualizer/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        votaciones_finalizadas = Voting.objects.filter(end_date__isnull=False, tally__isnull=False)
        context['vot_finalizadas'] = votaciones_finalizadas
        return context


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
            lista_votos= r[0]['tally']
            cantidad_votos= len(lista_votos)
            context['cantidad_votos'] = cantidad_votos
            cantidad_votantes =Census.objects.filter(voting_id=vid).all().count()
            context['cantidad_votantes'] = cantidad_votantes
            abstencion = 100 - (cantidad_votos/cantidad_votantes)*100
            context['abstencion'] = abstencion
            fecha_inicio=r[0]['start_date']
            fecha_fin= r[0]['end_date']
            fechas = dateComparer(fecha_inicio,fecha_fin)
            context['duracion'] = fechas[0]
            context['inicio'] = fechas[1]
            context['fin'] = fechas[2]
        except:
            raise Http404

        return context
    
def dateComparer(start_date,end_date):

    #2021-12-18T11:07:51.009086Z
    anyo1= start_date[0:4]
    mes1= start_date[5:7]
    dia1= start_date[8:10]
    hora1= start_date[11:13]
    minuto1= start_date[14:16]
    segundo1= start_date[17:19]
    microsegundo1=start_date[20:-1]

    anyo2= end_date[0:4]
    mes2= end_date[5:7]
    dia2= end_date[8:10]
    hora2= end_date[11:13]
    minuto2= end_date[14:16]
    segundo2= end_date[17:19]
    microsegundo2=end_date[20:-1]

    fecha_inicio= datetime(int(anyo1),int(mes1),int(dia1),int(hora1),int(minuto1),int(segundo1),int(microsegundo1))
    fecha_fin= datetime(int(anyo2),int(mes2),int(dia2),int(hora2),int(minuto2),int(segundo2),int(microsegundo2))
    fecha_inicio_string = "Día: " + dia1 + "-"+ mes1 + "-" +anyo1 +" Hora " + hora1+":"+minuto1+":"+segundo1
    fecha_fin_string = "Día: " + dia2 + "-"+ mes2 + "-" +anyo2+ " Hora " + hora2+":"+minuto2+":"+segundo2 

    #parseamos la diferencia entre las fechas
    diferencia = fecha_fin - fecha_inicio

    return [dateParser(diferencia),fecha_inicio_string,fecha_fin_string]

def dateParser(diferencia):
    dias= diferencia.days
    if(dias<0):
        dias=0
    sec= diferencia.seconds
    if(sec>60):
        min= sec//60
        sec= sec%60
    if(min>60):
        horas= min//60
        min= min%60
    else:
        horas= 0
    return str(dias) + " días, "+str(horas)+ " horas, "+str(min)+" minutos y "+str(sec)+" segundos "