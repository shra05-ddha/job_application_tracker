from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from app.models import JobApplication


class Command(BaseCommand):
    help = "Send email reminders for job applications with follow-up scheduled for today."

    def handle(self, *args, **options):
        today = timezone.localdate()
        applications = (
            JobApplication.objects
            .filter(follow_up_on=today)
            .select_related("user", "company")
        )

        if not applications.exists():
            self.stdout.write(self.style.WARNING("No reminders to send today."))
            return

        sent_count = 0

        for app in applications:
            user_email = app.user.email

            if not user_email:
                self.stdout.write(
                    self.style.WARNING(f"Skipped: No email for user {app.user.username}.")
                )
                continue

            subject = f"Follow-up Reminder: {app.title} at {app.company.name}"
            body = (
                f"Hi {app.user.username},\n\n"
                f"This is a reminder to follow up on your application for:\n"
                f"🔹 **{app.title}**\n"
                f"🔹 **{app.company.name}**\n\n"
                f"If you haven't reached out yet, today is the scheduled follow-up date.\n\n"
                f"Best of luck!\n"
                f"- Job Tracker"
            )

            try:
                send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,   # Sender
                    [user_email],
                    fail_silently=False,
                )
                sent_count += 1

            except BadHeaderError:
                self.stdout.write(
                    self.style.ERROR(f"Invalid header found when sending to {user_email}.")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error sending email to {user_email}: {e}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully sent {sent_count} follow-up reminder(s).")
        )
