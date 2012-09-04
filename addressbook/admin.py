from django.contrib import admin
from addressbook.models import *

class ContactAdmin(admin.ModelAdmin):
    pass

class ContactGroupAdmin(admin.ModelAdmin):
    pass

class AddressAdmin(admin.ModelAdmin):
    pass

class EmailAdmin(admin.ModelAdmin):
    pass

class PhoneNumberAdmin(admin.ModelAdmin):
    pass

class WebsiteAdmin(admin.ModelAdmin):
    pass

class SocialNetworkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactGroup, ContactGroupAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(SocialNetwork, SocialNetworkAdmin)

