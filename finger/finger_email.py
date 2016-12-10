from django.core.mail import EmailMultiAlternatives

def send_email(subject, from_email=None, to_email_list=[], message=None, file_path=None):
    msg = EmailMultiAlternatives(subject, message, from_email, to_email_list)
    msg.attach_alternative(message, "text/html")
    try:
        msg.attach_file(file_path)
    except:
        pass
    return msg.send()



