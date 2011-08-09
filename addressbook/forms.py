from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USZipCodeField
from django.forms.formsets import BaseFormSet, formset_factory
from django.forms.models import inlineformset_factory, BaseInlineFormSet 
from django.forms import ValidationError

from addressbook.models import *

class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

class ContactGroupForm(ModelForm):
    class Meta:
        model = ContactGroup
        fields = ('name',)

class ContactForm(ModelForm):
    def __init__(self, *pa, **ka):
        user = ka.pop('user')
        super(ContactForm, self).__init__(*pa, **ka)
        self.fields['group'].queryset = ContactGroup.objects.filter(user=user)

    class Meta:
        model = Contact

class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ('email', 'type')

class PhoneForm(ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ('phone', 'type')

class AddressForm(ModelForm):
    zip = USZipCodeField()
    
    class Meta:
        model = Address
        fields = ('street','city','state','zip', 'type')


class MandatoryInlineFormSet(BaseInlineFormSet):
    def is_valid(self):
        return super(MandatoryInlineFormSet, self).is_valid() and \
                    not any([bool(e) for e in self.errors])  

    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise ValidationError('You must have at least one of these.')

PhoneFormSet = formset_factory(PhoneForm, max_num=3, formset=RequiredFormSet)
AddressFormSet = formset_factory(AddressForm, max_num=3, formset=RequiredFormSet)
EmailFormSet = formset_factory(EmailForm, max_num=3, formset=RequiredFormSet)

ContactFormSet = inlineformset_factory(ContactGroup, Contact, max_num=4, extra=1, can_delete = False)
EmailEditFormSet = inlineformset_factory(Contact, Email, max_num=3, extra=0, formset=MandatoryInlineFormSet)
PhoneEditFormSet = inlineformset_factory(Contact, PhoneNumber, max_num=3, extra=0, formset=MandatoryInlineFormSet)
AddressEditFormSet = inlineformset_factory(Contact, Address, max_num=3, extra=0, formset=MandatoryInlineFormSet)

