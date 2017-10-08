from django.utils import timezone


def prepare_answer(str):
    return str.lower().replace(',', '.').replace(' ', '').replace('\t', '').replace('\n', '')


def get_timeout(time):
    return int((time - timezone.now()).total_seconds())
