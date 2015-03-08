#!/usr/bin/env python

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('GEMAN',
    url(r'^$', 'views.index'),
  
    url(r'^database/initialize/$', 'views.database_initialize'),

    """
        Some rules:
         <PART>/<OPERATION>/ -> <PART>_<OPERATION> -> For API
         <PART>/<OPERATION>/interface/ -> <PART>_<OPERATION>_interface -> For the interface
        The <PART> is always singular.
    """

    url(r'^sample/insert/interface/$', 'views.sample_insert_interface'),
    url(r'^sample/insert/$', 'views.sample_insert'),
    url(r'^sample/index/interface/$', 'views.sample_index_interface'),

    url(r'^query/index/interface/$', 'views.query_index_interface'),

    url(r'^files/search/$', 'views.sample_search'), #Post request
    url(r'^variant/get/(?P<variant_id>[a-zA-Z0-9_-]*)/$', 'views.variant_get'),
    url(r'^general/insert/$', 'views.api_insert_general'), #Related to query_insert/
    url(r'^variant/search/$', 'views.variant_search'),
    url(r'^variant/import/$', 'views.variant_import'),

  
    url(r'^documentation/$', 'views.documentation'),
)
