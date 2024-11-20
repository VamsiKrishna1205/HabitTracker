from django.utils.timezone import now
from .models import HabitLog, Notification

def send_habit_reminders():
    today = now().date()
    incomplete_logs = HabitLog.objects.filter(date=today, completed=False)

    for log in incomplete_logs:
        user = log.habit.user
        message = f"Reminder: You haven't completed your habit '{log.habit.name}' today!"
        # Create a notification
        Notification.objects.create(user=user, message=message)


from celery import shared_task
from .tasks import send_habit_reminders

@shared_task
def habit_reminder_task():
    send_habit_reminders()
    
from celery import shared_task
from django.utils.timezone import now
from .models import HabitLog, Notification

@shared_task
def send_habit_reminders():
    """Send reminders for incomplete habits."""
    today = now().date()
    incomplete_logs = HabitLog.objects.filter(date=today, completed=False)

    for log in incomplete_logs:
        user = log.habit.user
        message = f"Reminder: You haven't completed your habit '{log.habit.name}' today!"
        Notification.objects.create(user=user, message=message)
    return f"Reminders sent for {len(incomplete_logs)} incomplete habits."

