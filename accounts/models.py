from django.contrib.auth.models import AbstractBaseUser, UserManager, \
    PermissionsMixin
from django.core import validators
from django.db import models
from django.utils import timezone

from accounts import constants


class User(AbstractBaseUser, PermissionsMixin):
    #: The Permission level for this user
    permission = models.CharField(max_length=40, blank=True, null=True,
                                  choices=constants.PERMISSION_CHOICES)
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(
        'username', max_length=30, unique=True, help_text=_(
            'Required. 30 characters or fewer. Letters, digits and '
            '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$', _(
                'Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    email = models.EmailField('email address', blank=True)
    is_staff = models.BooleanField(
        'staff status', default=False,
        help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    company = models.ForeignKey('company.Company', on_delete=models.SET_NULL)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def get_content_data(self):
        content = {
            'permission': self.permission,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_staff': self.is_staff,
            'is_active': self.is_active,
            'date_joined': self.date_joined,
        }

        return content

    def __unicode__(self):
        if self.first_name:
            if self.last_name:
                return "{0} {1}'s Profile".format(
                    self.first_name, self.last_name)
            else:
                return "{0}'s Profile".format(self.first_name)
        else:
            return "{0}'s Profile".format(self.username)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
