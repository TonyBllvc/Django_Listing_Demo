from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None): #when password is none, no account is created
        if not email:
            raise ValueError(_("Please enter a valid email address"))
               
        email = self.normalize_email(email) #converts your email " ..@email.com" to all small lowercases
        email = email.lower() #converts the name of the email to lowercases

        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db) #saves in specific database

        return user
     
     
    def create_realtor(self, email, name, password=None):
        user = self.create_user(email, name, password)

        user.is_realtor = True #sets realtor flag(within the model) to true
        user.save(using=self._db) #saves in specific database

        return user
    
    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
    
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db) #saves in specific database

        return user