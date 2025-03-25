from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email from Django.',
    'jodiemcquade@icloud.com',  # Your email as the sender
    fail_silently=False,
)
