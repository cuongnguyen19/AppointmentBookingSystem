from django.test.signals import setting_changed

from backend.utils.common import generate_settings, get_django_settings

PACKAGE_NAME = 'backend'
PACKAGE_OBJECT_NAME = 'BACKEND'

# DEFAULT CONFIGURATIONS
DEFAULT_SETTINGS = {

    # General settings
    'PROJECT_NAME': 'LearningPoint backend',
    'PROJECT_BASE_URL': '',

    # User fields to register and response to profile
    'USER_FIELDS': (
        'id',
        'username',
        'email',
        'password',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    ),
    'USER_READ_ONLY_FIELDS': (
        'is_superuser',
        'is_active',
    ),
    'USER_WRITE_ONLY_FIELDS': (
        'password',
    ),

    'USER_SERIALIZER': 'backend.api.user.UserSerializer',

    'USER_VERIFY_FIELD': 'is_active',

    # Activate user by token sent to email
    'USER_ACTIVATE_TOKEN_ENABLED': True,
    'USER_ACTIVATE_SUCCESS_TEMPLATE': '',
    'USER_ACTIVATE_FAILED_TEMPLATE': '',
    'USER_ACTIVATE_EMAIL_SUBJECT': 'Activate your account',
    'USER_ACTIVATE_EMAIL_TEMPLATE': '',

    # Profile
    'PROFILE_SERIALIZER': 'backend.api.profile.ProfileSerializer',
    'PROFILE_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # Register
    'REGISTER_SERIALIZER': 'backend.api.register.RegisterSerializer',
    'REGISTER_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'REGISTER_SEND_WELCOME_EMAIL_ENABLED': False,
    'REGISTER_SEND_WELCOME_EMAIL_SUBJECT': 'Welcome to the system',
    'REGISTER_SEND_WELCOME_EMAIL_TEMPLATE': '',

    # Appointment
    'APPOINTMENT_SERIALIZER': 'backend.serializers.AppointmentSerializer',
    'APPOINTMENT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # Update appointment
    'UPDATE_APPOINTMENT_SERIALIZER': 'backend.serializers.UpdateAppointmentSerializer',
    'UPDATE_APPOINTMENT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # Update Student, Tutor account, profile
    'UPDATE_STUDENT_SERIALIZER': 'backend.serializers.UpdateStudentSerializer',
    'UPDATE_TUTOR_SERIALIZER': 'backend.serializers.UpdateTutorSerializer',

    # Login
    'LOGIN_SERIALIZER': 'backend.api.login.LoginSerializer',
    'LOGIN_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    # For custom login username fields
    'LOGIN_USERNAME_FIELDS': ['username', 'email', ],

    'LOGOUT_REMOVE_TOKEN': False,

    # Change password
    'CHANGE_PASSWORD_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'CHANGE_PASSWORD_SERIALIZER': 'backend.api.change_password.ChangePasswordSerializer',

    # Reset password
    'RESET_PASSWORD_ENABLED': True,
    'RESET_PASSWORD_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'RESET_PASSWORD_SERIALIZER': 'backend.api.reset_password.ResetPasswordSerializer',
    'RESET_PASSWORD_EMAIL_SUBJECT': 'Reset Password',
    'RESET_PASSWORD_EMAIL_TEMPLATE': '',
    'RESET_PASSWORD_CONFIRM_TEMPLATE': '',
    'RESET_PASSWORD_SUCCESS_TEMPLATE': '',

    'EMAIL_BACKEND': 'django.core.mail.backends.console.EmailBackend',
}

backend_settings = generate_settings(get_django_settings(), DEFAULT_SETTINGS)


def settings_changed_handler(*args, **kwargs):
    """
    Listen user settings changed and update the backend_settings properties values
    """

    # Get the user setting values
    setting_values = kwargs['value']
    setting_key = kwargs['setting']

    # Check and update current serf settings
    if setting_values and setting_key == PACKAGE_OBJECT_NAME:
        for prop in setting_values:
            backend_settings[prop] = setting_values[prop]


setting_changed.connect(settings_changed_handler)
