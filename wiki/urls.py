from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    #url(r'^$', index, name="view_pages"),
    (r'^$', index),
    (r'^pages/$', pages),
    (r'^about/$', about),
    (r'^contact/$', contact),    
    (r'^add_page/$', add_page),
    (r'^translate_page/(?P<page_id>\d+)/$', translate_page),
    (r'^add_sugestion/(?P<paragraph_id>\d+)/(?P<page_id>\d+)/$', add_sugestion),
    (r'^aprove_sugestion/(?P<id>\d+)/$', aprove_sugestion),    
    (r'^sugestions/(?P<paragraph_id>\d+)/(?P<page_id>\d+)/$', sugestions),        
    #url(r'^add_page/$', add_page, name="add_page"),

)
