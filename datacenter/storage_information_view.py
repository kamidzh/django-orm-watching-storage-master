from datacenter.models import Passcard
from datacenter.models import Visit
from django.utils import timezone
import datetime
from django.shortcuts import render
from datacenter.models import get_duration, format_duration


def storage_information_view(request):
    non_closed_visits = []
    entered_visitors = Visit.objects.filter(leaved_at=None)


    for visitor in entered_visitors:
        entered_at = timezone.localtime(visitor.entered_at)
        duration = get_duration(visitor)
        owner_passcard = visitor.passcard
        non_closed_visits.append(
            {
                'who_entered': owner_passcard,
                'entered_at': entered_at,
                'duration': format_duration(duration),
            }
        )
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
