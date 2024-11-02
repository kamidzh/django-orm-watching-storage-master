from datacenter.models import Passcard, Visit
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from datacenter.models import is_visit_long, get_duration, format_duration


def passcard_info_view(request, passcode):
    this_passcard_visits = []
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    for visit in visits:
        entered_at = timezone.localtime(visit.entered_at)
        duration = get_duration(visit)
        this_passcard_visits.append(
            {
                'entered_at': entered_at,
                'duration': format_duration(duration),
                'is_strange': is_visit_long(duration)
            }
        )


    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
