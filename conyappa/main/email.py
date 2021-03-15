from django.conf import settings
from django.core.mail import send_mass_mail


def send(users, msg_subject_formatter, msg_formatter, from_alias="no-reply"):
    from_domain = settings.EMAIL_HOST_USER.split("@")[1]
    from_ = f"{from_alias}@{from_domain}"
    datatuples = [(msg_subject_formatter(user), msg_formatter(user), from_, [user.email]) for user in users]
    return send_mass_mail(datatuples)
