from datacenter.models import Visit
from django.utils import timezone
from django.shortcuts import render
from datacenter.models import get_duration, format_duration


def storage_information_view(request):
    serialized_visits = []
    not_finished_visits = Visit.objects.filter(leaved_at=None)
    for visit in not_finished_visits:
        entered_at = timezone.localtime(visit.entered_at)
        duration = get_duration(visit)
        owner_passcard = visit.passcard
        serialized_visits.append(
            {
                'who_entered': owner_passcard,
                'entered_at': entered_at,
                'duration': format_duration(duration),
            }
        )
    context = {
        'non_closed_visits': serialized_visits,
    }
    return render(request, 'storage_information.html', context)
