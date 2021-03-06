from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


class MyAccountManager(BaseUserManager):
    # create_user deals with creating the user of costumer type
    def create_user(self, email, name=None, contact_number=None, viewpass=None, password=None, ):
        if not email:
            raise ValueError("enter email")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            contact_number=contact_number,
            viewpass=viewpass,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_vendor(self, shop_number, shop_name, shop_add, plan, gst, vendor, subscripton_amount):
    #
    #     user = self.model(
    #         shop_number=shop_number,
    #         shop_name=shop_name,
    #         shop_add=shop_add,
    #         plan=plan,
    #         gst=gst,
    #         vendor=vendor,
    #         subscripton_amount=subscripton_amount,
    #     )
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, email, name, contact_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            contact_number=contact_number,
            # viewpass=viewpass,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    viewpass = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True, default=00000)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_Vendor = models.BooleanField(default=False)
    is_Blogger = models.BooleanField(default=False)
    is_Affiliate = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_admin

def get_uplaod_file_name(userpic, filename,):
    return u'shop/%s/%s%s' % (str(userpic.vendor_id)+"/data","",filename)
def get_uplaod_file_name_blog(userpic, filename,):
    return u'blog/%s/%s%s' % (str(userpic.blogger_id)+"/template","",filename)

class InvestorAccount(models.Model):
    investor = models.OneToOneField(Account, default=None, on_delete=models.CASCADE, primary_key=True, )
    email = models.EmailField(verbose_name="email", max_length=100)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # objects= MyAccountManager()
    def __str__(self):
        return self.office_name

# only has permission to make changes or view anything in django administration can change it to staff later
#     def has_perm(self, perm,obj=None):
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         return True

def get_uplaod_startup(userpic, filename, ):
    return u'startup/%s/%s%s' % (str(userpic.email), "", filename)
class Startup(models.Model):
    startup = models.OneToOneField(Account, default=None, on_delete=models.CASCADE, primary_key=True, )
    email = models.EmailField(verbose_name="email", max_length=100)
    startup_name = models.CharField(max_length=30)
    batch_of= models.CharField(max_length=30)
    contact_number= models.IntegerField(null=True, blank=True)
    num_founders= models.IntegerField(null=True, blank=True)
    is_registered=models.BooleanField(default=False)
    as_participant=models.BooleanField(default=False)
    to_seek_help=models.BooleanField(default=False)
    cur_stage= models.CharField(max_length=50)
    vision = models.TextField()
    type = models.CharField(max_length=30)
    description = models.TextField()
    short_description = models.CharField(max_length=120)
    image=models.ImageField(upload_to=get_uplaod_startup,null=True, blank=True, )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)