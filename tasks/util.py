from django.utils import timezone


def prepare_answer(str):
    return str.lower().replace(',', '.').replace(' ', '').replace('\t', '').replace('\n', '')


def get_timeout(time):
    return int((time - timezone.now()).total_seconds())


def get_delta_minute(start_time, end_time):
    return int((end_time - start_time).total_seconds() // 60)
