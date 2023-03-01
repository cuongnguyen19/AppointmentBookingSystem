from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from backend.constants import DEFAULT_EMAIL_BODY
from backend.settings import backend_settings
from backend.tokens import activation_token, reset_password_token
from backend.utils.users import (
    has_user_activate_token,
    has_user_verify_code,
    has_user_verified,
    generate_uid_and_token,
    generate_uid_and_token_to_reset,
)


def send_verify_email(user, domain='', id=''):
    """
    Send verify email to user's valid email

    Args:
        user (object): The user instance
        domain (str): The domain value
    """

    if has_user_activate_token():
        send_activate_token_email(user, domain, id)


def send_activate_token_email(user, domain, id):
    """
    Send activate token to user email

    Args:
        user (object): The user instance
        domain (str): The current domain
    """

    # Get activate link
    activate_link = domain + \
        reverse('activate', kwargs=generate_uid_and_token(
            user, activation_token, id))

    # Default template message
    default_message = DEFAULT_EMAIL_BODY['ACTIVATE'].format(
        activate_link=activate_link)

    html_template = backend_settings.USER_ACTIVATE_EMAIL_TEMPLATE

    html_message = render_to_string(
        html_template, {
            'activate_link': activate_link,
            'domain': domain
        }
    ) if html_template else None

    send_mail(
        subject=backend_settings.USER_ACTIVATE_EMAIL_SUBJECT,
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email, ],
        html_message=html_message or default_message
    )


def send_email_welcome(user):
    """
    Send welcome email to verified user if REGISTER_SEND_WELCOME_EMAIL_ENABLED is True

    Args:
        user (object): The user instance
    """

    # Check to send welcome email to verified user
    if has_user_verified(user) and backend_settings.REGISTER_SEND_WELCOME_EMAIL_ENABLED:

        # Default template message
        default_message = DEFAULT_EMAIL_BODY['WELCOME']

        html_template = backend_settings.REGISTER_SEND_WELCOME_EMAIL_TEMPLATE

        html_message = render_to_string(
            html_template, {'user': user}
        ) if html_template else None

        send_mail(
            subject=backend_settings.REGISTER_SEND_WELCOME_EMAIL_SUBJECT,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email, ],
            html_message=html_message or default_message
        )


def send_reset_password_token_email(user, domain):
    """
    Send reset password token to user email

    Args:
        user (object): The user instance
        domain (string): The current domain
    """

    # Get activate link
    reset_password_link = domain + reverse(
        'reset_password_confirm',
        kwargs=generate_uid_and_token_to_reset(user, reset_password_token)
    )

    # Default template message
    default_message = DEFAULT_EMAIL_BODY['RESET_PASSWORD'].format(
        reset_password_link=reset_password_link)

    html_template = backend_settings.RESET_PASSWORD_EMAIL_TEMPLATE

    html_message = render_to_string(
        html_template, {
            'reset_password_link': reset_password_link,
            'domain': domain
        }
    ) if html_template else None

    send_mail(
        subject=backend_settings.RESET_PASSWORD_EMAIL_SUBJECT,
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email, ],
        html_message=html_message or default_message
    )
