from django.utils.translation import gettext as _

# Email constants
DEFAULT_EMAIL_BODY = {
    'WELCOME': _('''
        <p>Hi,</p>
        <p>Welcome to the system!</p>
    '''),

    'ACTIVATE': _('''
    <p>By clicking on the following link, you are activating your account</p>
    <a href="{activate_link}">Activate Account</a>
    '''),

    'RESET_PASSWORD': _('''
    <p>Please go to the following page and choose a new password:</p>
    <a href="{reset_password_link}">Reset Password</a>
    ''')
}
