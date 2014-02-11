import hashlib

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.context import RequestContext

from addressbook.forms import *
from addressbook.models import *
from helper import VCard



@login_required
def add_group(request):
    if request.method == "GET":
        form = ContactGroupForm()
    else:
        group = ContactGroup(user=request.user)
        form = ContactGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
#            request.user.message_set.create(message = 'Successfully saved group.')
            return HttpResponseRedirect(reverse('addressbook_index'))
    return render(request, 'addressbook/add_group.html',
            RequestContext(request, {'form':form}))

 
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
#            request.user.message_set.create(message = 'Successfully saved contact.')
            return HttpResponseRedirect(reverse('addressbook_index')) # Redirect to a 'success' page
    else:
        groups = ContactGroup.objects.filter(user=request.user)
        if not groups:
            return HttpResponseRedirect(reverse('addressbook_add_group'))
        contact_form = ContactForm(user=request.user)
        email_formset = EmailFormSet(prefix="email")
        phone_formset = PhoneFormSet(prefix="phone")
        address_formset = AddressFormSet(prefix="address")
    return render(request, 'addressbook/add_contact.html',
            RequestContext(request, {
                'phone_formset':phone_formset, 'contact_form':contact_form,
                'email_formset':email_formset, 'address_formset':address_formset
            }))

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
    return render(request, 'addressbook/edit_contact.html',
            RequestContext(request, {
                'email_formset':email_formset, 'phone_formset':phone_formset,
                'address_formset':address_formset, 'contact_form':contact_form,
                'contact':contact
            }))

@login_required
def index(request):
    groups = ContactGroup.objects.filter(user=request.user)
    contacts = Contact.objects.filter(group__user=request.user)
    tup = [(group.name, Contact.objects.filter(group = group).order_by('last_name','first_name')) for group in groups]
    return render(request, 'addressbook/index.html',
            RequestContext(request, {'tup':tup, 'contacts':contacts}))

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
        return render(request, 'addressbook/single_contact.html',
                RequestContext(request, {
                    'contact':contact, 'emails':emails, 'hash':hash,
                    'addresses':addresses, 'phones':phones,
                    'vcard_str': str(VCard(contact)),
                }))
    elif request.method=="POST":
        contact.delete()
        return HttpResponseRedirect(reverse('addressbook_index'))    
    else:
        raise Http404

@login_required
def download_vcard(request, vcard=VCard):
    """
    View function for returning single vcard
    """
    pk = request.GET.get('id');
    contact = Contact.objects.get(pk=pk)
    output = vcard(contact).output_string()
    filename = "contact_%s%s.vcf" % (contact.first_name, contact.last_name)
    response = HttpResponse(output, mimetype="text/x-vCard")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
