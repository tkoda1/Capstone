import datetime

def generate_time_choices():
    times = []
    start_time = datetime.datetime(2000, 1, 1, 0, 0)
    while start_time.time() < datetime.time(23, 45):
        times.append((start_time.time().strftime('%H:%M'), start_time.time().strftime('%I:%M %p')))
        start_time += datetime.timedelta(minutes=15)
    return times


DAYS_OF_WEEK = [
    ('MO', 'Monday'),
    ('TU', 'Tuesday'),
    ('WE', 'Wednesday'),
    ('TH', 'Thursday'),
    ('FR', 'Friday'),
    ('SA', 'Saturday'),
    ('SU', 'Sunday'),
]

DISPOSAL_TIMES = generate_time_choices()