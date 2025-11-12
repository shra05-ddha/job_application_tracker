from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from app.models import JobApplication

class Command(BaseCommand):
    help = "Send follow-up reminder emails for applications due today"

    def handle(self, *args, **options):
        today = timezone.localdate()
        due = JobApplication.objects.filter(follow_up_on=today)
        for app in due.select_related("user", "company"):
            if not app.user.email:
                continue
            subject = f"Follow up: {app.title} @ {app.company.name}"
            body = f"Reminder to follow up on {app.title} at {app.company.name}."
            send_mail(subject, body, None, [app.user.email])
        self.stdout.write(self.style.SUCCESS("Follow-up reminders sent"))
