from django.db import models

# Create your models here.

'''
class PhoneUserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError('Users must have an phone')

        user = self.model(
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        u = self.create_user(phone, password=password)
        u.is_admin = True
        u.save(using=self._db)
        return u


class PhoneUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, blank=True)
    phone = models.CharField(_('phone'), max_length=30, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_of_birth = models.DateField()

    objects = PhoneUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        app_label = 'auth'

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

    def __unicode__(self):
        return self.phone

    # Maybe required?
    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # Admin required fields
    @property
    def is_staff(self):
        return self.is_admin
'''        