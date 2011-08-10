from urllib import urlencode
import hashlib
import vobject

from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout 
from django.http import Http404, HttpResponse, HttpResponseRedirect

import settings
from addressbook.models import *
from addressbook.forms import *

@login_required
def add_group(request):
    if request.method == "GET":
        form = ContactGroupForm()
    else:
        group = ContactGroup(user=request.user)
        form = ContactGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message = 'Successfully saved group.')
            return HttpResponseRedirect(reverse('addressbook_index'))
    return direct_to_template(request, 'addressbook/add_group.html', {'form':form})

 
@login_required
def add_contact(request):
    if request.method == 'POST': # If the form has been submitted...
        contact_form = ContactForm(request.POST, user=request.user) # A form bound to the POST data
        # Create a formset from the submitted data
        email_formset = EmailFormSet(request.POST, prefix="email")
        phone_formset = PhoneFormSet(request.POST, prefix="phone")
        address_formset = AddressFormSet(request.POST, prefix="address")
        if contact_form.is_valid() and email_formset.is_valid() and phone_formset.is_valid() and address_formset.is_valid():
            contact = contact_form.save()
            for form in email_formset.forms:
                email = form.save(commit=False)
                email.contact = contact
                email.save()
            for form in phone_formset.forms:
                phone = form.save(commit=False)
                phone.contact = contact
                phone.save()
            for form in address_formset.forms:
                address = form.save(commit=False)
                address.contact = contact
                address.save()
            request.user.message_set.create(message = 'Successfully saved contact.')    
            return HttpResponseRedirect(reverse('addressbook_index')) # Redirect to a 'success' page
    else:
        groups = ContactGroup.objects.filter(user=request.user)
        if not groups:
            return HttpResponseRedirect(reverse('addressbook_add_group'))
        contact_form = ContactForm(user=request.user)
        email_formset = EmailFormSet(prefix="email")
        phone_formset = PhoneFormSet(prefix="phone")
        address_formset = AddressFormSet(prefix="address")
    return direct_to_template(request, 'addressbook/add_contact.html', {
        'phone_formset':phone_formset, 'contact_form':contact_form,
        'email_formset':email_formset, 'address_formset':address_formset})

@login_required
def edit_contact(request, pk):
    contact = Contact.objects.get(pk=pk)
    if contact.group.user != request.user:
        return HttpResponse(contact.group.user.username + request.user.username)
        #raise Http404
    if request.method == "POST":
        contact_form = ContactForm(request.POST, instance = contact, user = request.user)
        phone_formset = PhoneEditFormSet(request.POST, instance = contact, prefix="phone")
        address_formset = AddressEditFormSet(request.POST, instance = contact, prefix="address")
        email_formset = EmailEditFormSet(request.POST, instance = contact, prefix="email")
        if (contact_form.is_valid() and email_formset.is_valid() and
            address_formset.is_valid() and email_formset.is_valid()):
            contact_form.save()
            email_formset.save()
            address_formset.save()     
            phone_formset.save()     
            return HttpResponseRedirect(reverse('addressbook_index'))
    else:
        contact_form = ContactForm(instance=contact, user=request.user)
        phone_formset = PhoneEditFormSet(instance = contact, prefix="phone") 
        address_formset = AddressEditFormSet(instance = contact, prefix="address") 
        email_formset = EmailEditFormSet(instance = contact, prefix="email") 
    return direct_to_template(request, 'addressbook/edit_contact.html', {
        'email_formset':email_formset, 'phone_formset':phone_formset,
        'address_formset':address_formset, 'contact_form':contact_form,
        'contact':contact
        })

@login_required
def index(request):
    groups = ContactGroup.objects.filter(user=request.user)
    contacts = Contact.objects.filter(group__user=request.user)
    tup = [(group.name, Contact.objects.filter(group = group).order_by('last_name','first_name')) for group in groups]
    return direct_to_template(request, 'addressbook/index.html', {'tup':tup, 'contacts':contacts})

def get_hash(str):
    str = str.lower().strip()
    md5 = hashlib.md5()
    md5.update(str)
    return md5.hexdigest()
    
@login_required
def single_contact(request, pk):
    contact = Contact.objects.get(pk = pk)
    if contact.group.user != request.user:
        raise Http404
    if request.method=="GET":
        emails = Email.objects.filter(contact = contact)
        hash = ''
        if emails:
            email = emails[0]
            hash = get_hash(email.email)
        # XXX is email required?
        addresses = Address.objects.filter(contact = contact)
        if addresses:
            address = addresses[0]
        phones = PhoneNumber.objects.filter(contact=contact)
        return direct_to_template(request, 'addressbook/single_contact.html', {
            'contact':contact, 'emails':emails, 'hash':hash, 'addresses':addresses,
            'phones':phones, 'vcard_str': _vcard_string(contact),
        })
    elif request.method=="POST":
        contact.delete()
        return HttpResponseRedirect(reverse('addressbook_index'))    
    else:
        raise Http404

def _vcard_string(contact):
    """
    Helper function for vcard views. Accepts a 'contact' object 
    with certain attributes (firstname, lastname, email, phone, id)
    and returns a string containing serialized vCard data.
    """
    v = vobject.vCard()
    v.behavior.sortFirst = ('version', 'prodid' ,'uid', 'n', 'fn', 'org', 'title', 'photo', 'tel', 'adr', 'email')
    v.add('n')
    v.n.value = vobject.vcard.Name(family=contact.last_name, given=contact.first_name, additional=contact.middle_name)
    v.add('fn')
    if contact.middle_name:
        initial = contact.middle_name[0].upper()
        v.fn.value = "%s %s. %s" % (contact.first_name, initial, contact.last_name)
    else:
        v.fn.value = "%s %s" % (contact.first_name, contact.last_name)
    org = contact.organization
    if org:
        v.add('org')
        v.org.value = [org]
    addresses = Address.objects.filter(contact=contact)
    title = contact.title
    if title:
        v.add('title')
        v.title.value = title
    for address in addresses:
        a = v.add('adr')
        a.value = vobject.vcard.Address(street=address.street, city=address.city, region= address.state, code = address.zip, country = "United States" )
        a.type_param = address.type
    emails = Email.objects.filter(contact=contact)
    for email in emails:
        e = v.add('email')
        e.value = email.email
        e.type_param = email.type
    phones = PhoneNumber.objects.filter(contact=contact)
    for phone in phones:
        p = v.add('tel')
        p.value = phone.phone
        p.type_param = phone.type
    url = contact.url
    if url:
        v.add('url')
        v.url.value = contact.url
    output = v.serialize()
    return output

def _vcard_string2(contact):
    pass 

@login_required
def download_vcard(request, pk):
    """
    View function for returning single vcard
    """
    contact = Contact.objects.get(pk=pk)
    output = _vcard_string(contact)
    filename = "%s%s.vcf" % (contact.first_name, contact.last_name)
    response = HttpResponse(output, mimetype="text/x-vCard")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

