from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from addressbook.helper import VCard
from addressbook.models import *
from addressbook.views import get_hash



class TestModelsTestCase(TestCase):
    def setUp(self):
        """
        Create a User 1, a 'Family' contact group, a 1st contact in the 'Family' group
        a 1st address, email and phone no. for the 1st contact. Create a second address,
        email, and phone no. for the 1st contact.
        """
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'abc')
        self.group1 = ContactGroup.objects.create(user = self.user, name = 'Family')
        self.contact1 = Contact.objects.create(first_name = 'Sven', last_name='Smith',
                                               group = self.group1,
                                               organization = 'FDA',
                                               url='http://fda.gov')
        self.address1 = Address.objects.create(street = '2000 Hunt Ave',
                                               city = 'Arlington', state = 'VA',
                                               zip = '22313', type = 'Work', contact = self.contact1)
        self.email1 = Email.objects.create(email = 'Sven@gmail.com', type="Work", contact = self.contact1)
        self.phone1 = PhoneNumber.objects.create(contact = self.contact1, type="Work", phone = '212-123-1234')
        self.address2 = Address.objects.create(street = '543 Cameron Run Terrace',
                                               city = 'Arlington', state = 'VA', zip = '22313',
                                               contact = self.contact1, type="Home")
        self.email2 = Email.objects.create(email = 'blah@gmail.com', type="Home", contact = self.contact1)
        self.phone2 = PhoneNumber.objects.create(contact = self.contact1, phone = '410-123-3455', type="Home")

        """
        Create a 2nd Contact for the 'Family' contact group with Email, Phone, Address
        """
        self.contact2 = Contact.objects.create(first_name = 'Bogus', last_name='Lee',
                                               group = self.group1, middle_name='Nacho',
                                               organization='Doritos Inc.', url='http://doritos.com')
        self.c2_address = Address.objects.create(street = '11 Park Pl', city = 'Django', state = 'NJ',
                                               zip = '07463-2308', type="Home", contact = self.contact2)

        self.c2_email = Email.objects.create(email = 'Mark@gmail.com', type="Home", contact = self.contact2)
        self.c2_phone = PhoneNumber.objects.create(contact=self.contact2, phone='201-123-1234', type="Home")

        """
        Create a 2nd Group: Friends. Create a 3rd contact in this group with Email, Address
        Phone.
        """
        self.group2 = ContactGroup.objects.create(user = self.user, name = 'Friends')
        self.contact3 = Contact.objects.create(first_name = 'Donald', last_name='Duck',
                                               group = self.group2,
                                               organization = 'Ducks & Friends',
                                               url='http://ducks.com')
        self.c3_email1 = Email.objects.create(email = 'Donald@gmail.com', type="Home", contact = self.contact3)
        self.c3_phone1 = PhoneNumber.objects.create(contact = self.contact3, phone = '321-123-3455', type="Home")
        self.c3_address1 = Address.objects.create(street = '123 Dagger Ave', city = 'Danger', state = 'NY',
                                               zip = '07222-2308', type="Home", contact = self.contact3)

        self.login_req_uris=['/addressbook/','/addressbook/group/add','/addressbook/contact/add',
              '/addressbook/contact/%s/edit', '/addressbook/contact/%s/view',
              '/addressbook/contact/%s/download']
        self.no_login_req_uris = [ ] # there are no URLs available for not logged in visitors now
        self.client = Client()
        self.logged_client = Client()
        self.logged_client.login(username='john', password='abc')
        self.work_group = None
        self.contact_4 = None

    def testUser(self):
        """ Test that Users was created ok"""
        self.assertEqual(self.user.username, 'john')

    def testGroup(self):
        """ Test that Categories was created ok"""
        self.assertEqual(self.group1.name, 'Family')
        self.assertEqual(self.group1.user, self.user)

    def testContact1(self):
        """ Test that contact 1 was created ok """
        self.assertEqual(self.contact1.first_name, 'Sven')
        self.assertEqual(self.contact1.group,self.group1)
        self.assertEqual(self.contact1.organization, 'FDA')

    def testEmail1(self):
        """ Test that contact1's 1st email was created ok """
        self.assertEqual(self.email1.email, 'Sven@gmail.com')
        self.assertEqual(self.email1.contact, self.contact1)

    def testPhone1(self):
        """ Test that contact1's 1st phone # was created ok """
        self.assertEqual(self.phone1.phone, '212-123-1234')

    def testAddress2(self):
        self.assertEqual(self.address2.street, '543 Cameron Run Terrace')
        self.assertEqual(self.address2.state, 'VA')

    def testEmail2(self):
        """ Test that contact1's 2nd email was created ok """
        self.assertEqual(self.email2.email, 'blah@gmail.com')
        self.assertEqual(self.email2.contact, self.contact1)

    def testPhone2(self):
        """ Test that contact1's 2nd phone # was created ok """
        self.assertEqual(self.phone2.phone, '410-123-3455')

    def testContactOneNumEmail(self):
        """ test that contact1 has 2 emails """
        self.assertEqual(Email.objects.filter(contact=self.contact1).count(), 2)

    def testContactTwo(self):
        """
        Make sure contact2's details are correct
        """
        self.assertEqual(self.contact2.first_name, 'Bogus')
        self.assertEqual(Email.objects.get(contact = self.contact2).email, 'Mark@gmail.com')
        self.assertEqual(PhoneNumber.objects.get(contact = self.contact2).phone, '201-123-1234')
        self.assertEqual(Address.objects.get(contact = self.contact2).street, '11 Park Pl')

    def testContactThree(self):
        """ Test that contact 3 was created and his email, phone, and address are ok """
        self.assertEqual(self.contact3.first_name, 'Donald')
        self.assertEqual(Email.objects.get(contact = self.contact3).email, 'Donald@gmail.com')
        self.assertEqual(PhoneNumber.objects.get(contact = self.contact3).phone, '321-123-3455')
        self.assertEqual(Address.objects.get(contact = self.contact3).street, '123 Dagger Ave')

    def testNumberOfContacts(self):
        self.assertEqual(Contact.objects.filter(group__user = self.user).count(), 3)

    def test_no_login_req_URLS(self):
        for uri in self.no_login_req_uris:
            response = self.client.get(uri)
            self.failUnlessEqual(response.status_code, 200)

    def test_login_required_URLs(self):
        for uri in self.login_req_uris:
            if '%s' in uri:
                uri = uri % 1
            response = self.client.get(uri)
            self.failUnlessEqual(response.status_code, 302)

    def test_login_required_URLs_authenticated(self):
        pk = Contact.objects.all()[0].pk
        for uri in self.login_req_uris:
            if '%s' in uri:
                uri = uri % pk
            response = self.logged_client.get(uri)
            self.failUnlessEqual(response.status_code, 200)

    def test_add_group(self):
        response = self.logged_client.post('/addressbook/group/add', {'name':'Work'})
        self.failUnlessEqual(response.status_code, 302)
        #self.work_group = ContactGroup.objects.get(name = 'Work')

    def test_add_contact(self):
        """ POST data: ContactForm, EmailFormset w/ prefix, PhoneFormSet w/ prefix, AddressFormSet w/ prefix"""
        response = self.logged_client.post('/addressbook/contact/add', {
                'group': self.group1.pk,
                'last_name':'Manno', 'first_name':'David', 'order': 1,
                'email-TOTAL_FORMS':'1', 'email-INITIAL_FORMS':'0',
                'email-MAX_NUM_FORMS':'0', 'email-0-email':'Sven@gmail.com',
                'email-0-type':'Work',
                'phone-TOTAL_FORMS':'1', 'phone-INITIAL_FORMS':'0',
                'phone-MAX_NUM_FORMS':'3', 'phone-0-phone':'201-123-1234',
                'phone-0-type':'Work',
                'address-TOTAL_FORMS':'1', 'address-INITIAL_FORMS':'0',
                'address-MAX_NUM_FORMS':'3', 'address-0-street':'11 Steven Pl',
                'address-0-city':'Waldwick', 'address-0-state':'NJ',
                'address-0-zip':'07463', 'address-0-type':'Work',
                'website-TOTAL_FORMS':'1', 'website-INITIAL_FORMS':'0',
                'website-MAX_NUM_FORMS':'3',
                'website-0-website':'http://www.github.com',
                'website-0-type':'Work', 'website-0-name':'GitHub'
            })
        self.assertRedirects(response, '/addressbook/')
        self.failUnlessEqual(response.status_code, 302)
        count = Contact.objects.all().count()
        self.failUnlessEqual(count, 4)
        #self.failUnlessEqual(c.first_name, 'David')

    def test_edit_contact(self):
        response = self.logged_client.post('/addressbook/contact/%s/edit' % self.contact1.pk, {
                'group': self.group1.pk,
                'last_name':'Smith', 'first_name':'Sven',
                'middle_name':'Steven', 'order': 1,
                'email-TOTAL_FORMS':'1', 'email-INITIAL_FORMS':'0',
                'email-MAX_NUM_FORMS':'0', 'email-0-email':'manno@gmail.com',
                'email-0-type':'Work',
                'phone-TOTAL_FORMS':'1', 'phone-INITIAL_FORMS':'0',
                'phone-MAX_NUM_FORMS':'3', 'phone-0-phone':'201-123-1234',
                'phone-0-type':'Work',
                'address-TOTAL_FORMS':'1', 'address-INITIAL_FORMS':'0',
                'address-MAX_NUM_FORMS':'3', 'address-0-street':'15 Howard Pl',
                'address-0-city':'Waldwick', 'address-0-state':'NJ',
                'address-0-zip':'07463', 'address-0-type':'Work',
                'website-TOTAL_FORMS':'1', 'website-INITIAL_FORMS':'0',
                'website-MAX_NUM_FORMS':'3',
                'website-0-website':'http://www.github.com',
                'website-0-type':'Work', 'website-0-name':'GitHub'
            })
        self.failUnlessEqual(response.status_code, 302)
        c = Contact.objects.get(last_name='Smith', first_name='Sven')
        self.failUnlessEqual(c.middle_name, 'Steven')

    def test_delete_contact(self):
        old_count = Contact.objects.all().count()
        response = self.logged_client.post('/addressbook/contact/%s/view' % self.contact1.pk, {})
        self.failUnlessEqual(response.status_code, 302)
        new_count = Contact.objects.all().count()
        self.failUnlessEqual(new_count + 1, old_count)

    def test_gravatar_hash(self):
        hash = get_hash(' MyEmailAddress@example.com ')
        self.failUnlessEqual(hash,'0bc83cb571cd1c50ba6f3e8a78ef1346')

    def test_vcard_algo(self):
        output = str(VCard(self.contact1)).splitlines()
        expected = 'BEGIN:VCARD\r\nVERSION:3.0\r\nN:Smith;Sven;;;\r\nFN:Sven Smith\r\nORG:FDA\r\nTEL;TYPE=Work:212-123-1234\r\nTEL;TYPE=Home:410-123-3455\r\nADR;TYPE=Home:;;543 Cameron Run Terrace;Arlington;VA;22313;United States\r\nADR;TYPE=Work:;;2000 Hunt Ave;Arlington;VA;22313;United States\r\nEMAIL;TYPE=Work:Sven@gmail.com\r\nEMAIL;TYPE=Home:blah@gmail.com\r\nURL:http://fda.gov\r\nEND:VCARD\r\n'
        expected = expected.splitlines()
        good = True
        for i in range(0, len(output)):
            if output[i] not in expected:
                good = False
        self.failUnlessEqual(good, True)

    def tearDown(self):
        self.user.delete()
        self.group1.delete()
        self.address1.delete()
        self.address2.delete()
        self.phone1.delete()
        self.phone2.delete()
        self.email1.delete()
        self.email2.delete()
        self.contact1.delete()
        self.c2_address.delete()
        self.c2_email.delete()
        self.c2_phone.delete()
        self.contact2.delete()
