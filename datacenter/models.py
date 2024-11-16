from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def is_visit_long(duration, minutes=60):
    seconds_in_one_minute = 60
    duration_min = duration.total_seconds() // seconds_in_one_minute
    return duration_min > minutes


def get_duration(visit):
    entered_at = timezone.localtime(visit.entered_at)
    if not visit.leaved_at:
        now = timezone.localtime(timezone.now())
        duration = now - entered_at
    else:
        leaved_at = timezone.localtime(visit.leaved_at)
        duration = leaved_at - entered_at
    return duration


def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    seconds_in_one_hour = 3600
    seconds_in_one_minute = 60
    hours = total_seconds // seconds_in_one_hour
    minutes = (total_seconds % seconds_in_one_hour) // seconds_in_one_minute
    seconds = total_seconds % seconds_in_one_minute
    return f'{hours}:{minutes}:{seconds}'
