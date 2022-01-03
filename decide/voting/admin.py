from django.contrib import admin
from django.utils import timezone

from .models import QuestionOption
from .models import Question
from .models import Voting
from store.models import Vote
from django.contrib import messages

from .filters import StartedFilter


def start(modeladmin, request, queryset):
    votaciones_empezadas = ""
    votaciones_ya_empezadas = ""
    for v in queryset.all():
        if v.start_date != None:
            votaciones_ya_empezadas = votaciones_ya_empezadas + ", " + v.name
        else:
            votaciones_empezadas = votaciones_empezadas + ", " + v.name
            v.create_pubkey()
            v.start_date = timezone.now()
            v.save()
    if votaciones_empezadas != "":
        messages.add_message(request, messages.INFO, 'Las votaciones [' + votaciones_empezadas[2:] + "] han sido iniciadas correctamente")
    if votaciones_ya_empezadas != "":
        messages.add_message(request, messages.WARNING, 'Las votaciones [' + votaciones_ya_empezadas[2:] + "] ya habían sido iniciadas anteriormente")


def stop(ModelAdmin, request, queryset):
    votaciones_paradas = ""
    votaciones_no_paradas = ""
    votaciones_ya_paradas = ""
    for v in queryset.all():
        if v.start_date == None:
            votaciones_no_paradas = votaciones_no_paradas + ", " + v.name
        elif v.end_date != None:
            votaciones_ya_paradas = votaciones_ya_paradas + ", " + v.name
        else:
            v.end_date = timezone.now()
            v.save()
            votaciones_paradas = votaciones_paradas + ", " + v.name
    if votaciones_paradas != "":
        messages.add_message(request, messages.INFO, 'Las votaciones [' + votaciones_paradas[2:] + "] han sido detenidas correctamente")
    if votaciones_no_paradas != "":
        messages.add_message(request, messages.ERROR, 'Las votaciones [' + votaciones_no_paradas[2:] + "] no se pueden detener porque no han sido iniciadas anteriormente")
    if votaciones_ya_paradas != "":
        messages.add_message(request, messages.WARNING, 'Las votaciones [' + votaciones_ya_paradas[2:] + "] ya habían sido detenidas anteriormente")


def tally(ModelAdmin, request, queryset):
    votaciones_recontadas = ""
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')
        v.tally_votes(token)
        votaciones_recontadas = votaciones_recontadas + ", " + v.name
    if votaciones_recontadas != "":
        messages.add_message(request, messages.INFO, 'Las votaciones [' + votaciones_recontadas[2:] + "] han sido recontadas correctamente")


def reset(ModelAdmin, request, queryset):
    votaciones_reseteadas = ""
    for v in queryset.all():
        votaciones_reseteadas = votaciones_reseteadas + ", " + v.name
        v.start_date = None
        v.end_date = None
        Vote.objects.filter(voting_id=v.id).delete()
        v.save()
    messages.add_message(request, messages.INFO, 'Las votaciones [' + votaciones_reseteadas[2:] + "] han sido reseteadas correctamente")

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally, reset ]


admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)
