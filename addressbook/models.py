from django.db import models
from django.contrib.localflavor.us.models import USStateField, PhoneNumberField
from django.contrib.auth.models import User

ADR_TYPES = (
#    ('INTL', 'INTL'),
#    ('POSTAL', 'POSTAL'),
#    ('PARCEL', 'PARCEL'),
    ('WORK', 'WORK'),
#    ('DOM', 'DOM'),
    ('HOME', 'HOME'),
#    ('PREF', 'PREF'),
)

TEL_TYPES = (
    ('HOME', 'HOME'),
#    ('MSG', 'MSG'),
    ('WORK', 'WORK'),
#    ('PREF', 'PREF'),
    ('FAX', 'FAX'),
    ('CELL', 'CELL'),
)

EMAIL_TYPES = (
    ('HOME', 'HOME'),
    ('WORK', 'WORK'),
#    ('INTERNET', 'INTERNET'),
#    ('PREF', 'PREF'),
)

class ContactGroup(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length = "40", verbose_name = 'Group Name')

    class Meta:
        unique_together = ('user','name') 

    def __unicode__(self):
        return self.name   

class Contact(models.Model):
    group = models.ForeignKey(ContactGroup) 
    last_name = models.CharField(max_length = "40", blank=False)
    first_name = models.CharField(max_length = "40", blank=False)
    middle_name = models.CharField(max_length = "40", blank = True)
    title = models.CharField(max_length = "40", blank = True)
    organization = models.CharField(max_length = "50", blank = True)
    url = models.URLField(verify_exists = False, blank = True)    
    
    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Address(models.Model):
    contact = models.ForeignKey(Contact)
    street = models.CharField(max_length = "50")
    city = models.CharField(max_length = "40")
    state = USStateField()
    zip = models.CharField(max_length = "10") 
    type = models.CharField(max_length="5", choices = ADR_TYPES)

    def __unicode__(self):
        return '%s %s: %s %s, %s' % (self.contact.first_name, self.contact.last_name, self.street, self.city, self.state)

class PhoneNumber(models.Model):
    contact = models.ForeignKey(Contact)
    phone = PhoneNumberField()
    type = models.CharField(max_length="4", choices = TEL_TYPES)

    def __unicode__(self):
        return "%s %s: %s" % (self.contact.first_name, self.contact.last_name, self.phone)
   
class Email(models.Model):
    contact = models.ForeignKey(Contact)
    email = models.EmailField() 
    type = models.CharField(max_length="8", choices = EMAIL_TYPES) 
    
    def __unicode__(self):
        return "%s %s: %s" % (self.contact.first_name, self.contact.last_name, self.email)


