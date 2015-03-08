#!/usr/bin/env python

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('GEMAN',
    url(r'^$', 'views.index'),
  
    url(r'^database/initialize/$', 'views.database_initialize'),

    url(r'^sample/insert/interface/$', 'views.sample_insert_interface'),
    url(r'^sample/insert/$', 'views.sample_insert'),


    url(r'^api/files/search$', 'views.sample_search'), #Post request
    url(r'^api/variant/get/(?P<variant_id>[a-zA-Z0-9_-]*)/$', 'views.variant_get'),
    url(r'^api/general/insert/$', 'views.api_insert_general'), #Related to query_insert/
    url(r'^api/variant/search/$', 'views.variant_search'),
    url(r'^api/variant/import/$', 'views.variant_import'),
  
    url(r'^query/$', 'views.query'),
  
    url(r'^documentation/$', 'views.documentation'),
)
