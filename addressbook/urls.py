from django.conf.urls.defaults import *

urlpatterns = patterns('addressbook.views',
    url(r'^$', 'index', name='addressbook_index'),
    url(r'^group/add$', 'add_group', name='addressbook_add_group'),    
    url(r'^contact/add$', 'add_contact', name='addressbook_add_contact'),    
    url(r'^contact/(?P<pk>\d+)/edit$', 'edit_contact', name='addressbook_edit_contact'),    
    url(r'^contact/(?P<pk>\d+)/view$', 'single_contact', name='addressbook_single_contact'),    
    url(r'^contact/(?P<pk>\d+)/download$', 'download_vcard', name='addressbook_download_vcard'),    
)
