import vobject
import inspect
from addressbook.models import *

class VCard(object):
    """ Helper class for vcard generation. """

    def __init__(self, contact):
        self.contact = contact
        self.card = vobject.vCard()
        self.card.behavior.sortFirst = (
            'version', 'prodid', 'uid', 'n', 'fn',
            'org', 'title', 'photo', 'tel', 'url',
            'adr', 'email',
        )

    def add_name(self):
        contact = self.contact
        card = self.card
        self.card.add('n')
        card.n.value = vobject.vcard.Name(family=contact.last_name, given=contact.first_name, additional=contact.middle_name)
        card.add('fn')
        if contact.middle_name:
            initial = contact.middle_name[0].upper()
            card.fn.value = "%s %s. %s" % (contact.first_name, initial, contact.last_name)
        else:
            card.fn.value = "%s %s" % (contact.first_name, contact.last_name)

    def add_org(self):
        contact = self.contact
        card = self.card
        org = contact.organization
        if org:
            card.add('org')
            card.org.value = [org]

    def add_title(self):
        contact = self.contact
        card = self.card
        title = contact.title
        if title:
            card.add('title')
            card.title.value = title

    def add_addresses(self):
        contact = self.contact
        card = self.card
        addresses = Address.objects.filter(contact=contact)
        for address in addresses:
            a = card.add('adr')
            a.value = vobject.vcard.Address(street=address.street, city=address.city, region= address.state, code = address.zip, country = "United States" )
            a.type_param = address.type

    def add_emails(self):
        contact = self.contact
        card = self.card
        emails = Email.objects.filter(contact=contact)
        for email in emails:
            e = card.add('email')
            e.value = email.email
            e.type_param = email.type

    def add_phones(self):
        contact = self.contact
        card = self.card
        phones = PhoneNumber.objects.filter(contact=contact)
        for phone in phones:
            p = card.add('tel')
            p.value = phone.phone
            p.type_param = phone.type

    def add_websites(self):
        contact = self.contact
        card = self.card
        websites = Website.objects.filter(contact=contact)
        for web in websites:
            w = card.add('url')
            w.value = web.website
            w.type_param = web.type

    def add_socialnetworks(self):
        contact = self.contact
        card = self.card
        social_nets = SocialNetwork.objects.filter(contact=contact)
        for social in social_nets:
            s = card.add('url')
            s.value = social.url
            s.type_param = social.type

    def output_string(self):
        """ Executes all the `add_` methods and serializes the vcard"""
        methods = [ k for k in dict(inspect.getmembers(self)).keys() if k.startswith('add_') ]
        for m in methods:
            getattr(self, m)()
        return self.card.serialize()

    def __str__(self):
        return self.output_string()
