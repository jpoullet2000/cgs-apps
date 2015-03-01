#!/usr/bin/env python

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('genomicAPI',
  url(r'^$', 'views.index'),
  
  url(r'^init/$', 'views.init'),
  
  url(r'^api/files/search$', 'views.api_search_sample_id'), #Post request
  url(r'^api/variants/get/(?P<variant_id>[a-zA-Z0-9_-]*)/$', 'views.api_get_variants'),
  url(r'^api/general/insert/$', 'views.api_insert_general'), #Related to query_insert/
  url(r'^api/variants/search/$', 'views.api_search_variants'),
  url(r'^api/variants/import/$', 'views.api_import_variants'),
  
  url(r'^query/$', 'views.query'),
  url(r'^query_insert/$', 'views.query_insert'),
  url(r'^job/$', 'views.job'),
  url(r'^history/$', 'views.history'),
  
  url(r'^documentation/$', 'views.documentation'),
)
