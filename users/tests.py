from django.core.mail import send_mail

send_mail(
    'Test Email', 
    'This is a test email from Django.', 
    '99mominur@gmail.com', 
    ['999mominur@gmail.com', "heymominur@gmail.com"],  # Replace with the recipient's email
    fail_silently=False,
)
