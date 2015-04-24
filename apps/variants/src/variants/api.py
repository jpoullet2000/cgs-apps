#!/usr/bin/env python

import json
import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.http import HttpResponse

from beeswax.design import hql_query
from beeswax.server import dbms
from beeswax.server.dbms import get_query_server_config
from impala.models import Dashboard, Controller

#from desktop.lib.django_util import JsonResponse
from desktop.lib.rest.http_client import RestException
from exception import handle_rest_exception

from variants.decorators import api_error_handler

LOG = logging.getLogger(__name__)

### debugging
# def current_line():
#     """ Return the current line number """
#     return inspect.currentframe().f_back.f_lineno
  
def fprint(txt):
    """ Print some text in a debug file """
    f = open('/home/cloudera/debug.txt', 'a')
    f.write(str(txt)+"\n")
    f.close()
    return True
###

## samples
@api_error_handler
def samples_create(request):
    """ create new samples
    """
    pass

@api_error_handler
def samples_delete(request):
    """ Deletes samples by ID 
    """
    pass

@api_error_handler
def samples_search(request):
    """ Searches for samples. It returns one or multiple representations of samples.
    """
    pass

## datasets
@api_error_handler
def datasets_create(request):
    """ Creates a new dataset 
    """
    pass

@api_error_handler
def datasets_delete(request):
    """ Deletes a dataset by ID
    """
    pass 

@api_error_handler
def datasets_list(request):
    """ Lists all datasets
    """
    pass


## readgroupsets
@api_error_handler
def readgroupsets_get(request):
    """ Gets a read group set by ID
    """
    pass


## variantsets
@api_error_handler
def variantsets_get(request):
    """ Gets a variant set by ID
    """
    pass

@api_error_handler    
def variantsets_importVariants(request):
    """ Creates variant data by asynchronously importing the provided information into HBase.
    HTTP request: POST https://<your.site>/variants/variantsets/variantSetId/importVariants    

    Parameters: 
     - variantSetId: string Required. The variant set to which variant data should be imported.  
    sourceUris: a list of URIs pointing to VCF files in the cluster
    format: "VCF" 

    ## VCF headers are 
    """
    pass 
    
## variants
@api_error_handler
def variants_get(request):
    """ Gets a variant by ID (ID = row key in HBase) 
    """
    result = {'status': -1}
    ## config.yml and reference.yml in CGSCONFIG (see the config file in the root directory of this package) 
    ## reading the config.yml file to define the datastructure (looking for HBase with "variant" in names)
    
    
    ## reading the reference.yml file to define the link between the API resource and HBase/impala fields
    ## impalaFields = 
    ## hbaseFields = 
    
    ## request HBase through Impala with the ID (or row key)
    ##Connexion db
    # query_server = get_query_server_config(name='impala')
    # db = dbms.get(request.user, query_server=query_server)
    # hql = "SELECT ... FROM ..."
    # query = hql_query(hql)
    # handle = db.execute_and_wait(query, timeout_sec=5.0)
    # if handle:
    #     data = db.fetch(handle, rows=1)
    #     result['data'] = list(data.rows())
    #     result['status'] = 1
    #     db.close(handle)  
    
    pass 


@api_error_handler
def variants_search(request):
    """ Gets a variant by ID (ID = row key in HBase)
    
    To test it type in your bash prompt: 
    See the documentation    

    """
    result = {'status': -1}
    # ## check request
    if request.method != 'POST':
        result['status'] = -1
        result['error'] = "The method should be POST."
        return HttpResponse(json.dumps(result), mimetype="application/json")
        ##return JsonResponse(result)

    criteria_json = request.POST['criteria']
    #fprint("============")
    ##fprint(criteria_json)
    #callsetid = json.loads(criteria)['callSetIds']
    criteria = json.loads(criteria_json)
    criteria_keys = [str(s) for s in criteria.keys()]
    #fprint(criteria['callSetIds'])
    if 'callSetIds' not in criteria_keys:
    #if 'callSetIds' not in request.POST.keys():
        result['status'] = -1
        result['keys'] = request.POST.keys()
        #result['criteria'] = callsetid
        result['error'] = "Information about the callsets (sample information should be available)."
        return HttpResponse(json.dumps(result), mimetype="application/json")
        ##return JsonResponse(result)

    callsetids = [str(s) for s in criteria['callSetIds']]
    ##fprint(','.join(callsetids))
    ## getting data from DB
    try:
        query_server = get_query_server_config(name='impala')
        db = dbms.get(request.user, query_server=query_server)
    except Exception:
        result['status'] = 0
        result['error'] = "Sorry, an error occured: Impossible to connect to the db."
        return HttpResponse(json.dumps(result), mimetype="application/json")

    try:
        ## TODO: the variant_table should be defined from the config files 
        variant_table = "jpoullet_1000genomes_1E7rows_bis"
        hql = "SELECT * FROM " + variant_table + " WHERE readGroupSets_readGroups_info_patientId IN ('" + ','.join(callsetids) + "')"
        fprint(hql)
        query = hql_query(hql)
        handle = db.execute_and_wait(query, timeout_sec=5.0)

    except:
        result['status'] = 0
        result['error'] = "The query cannot be performed :%s" % hql
        return HttpResponse(json.dumps(result), mimetype="application/json")

    
    if handle:
        data = db.fetch(handle, rows=1)
        result['data'] = list(data.rows())
        result['status'] = 1
        db.close(handle)  

    return HttpResponse(json.dumps(result), mimetype="application/json")
    

## callsets
@api_error_handler
def callsets_get(request):
    """ Gets a call set by ID 
    """
    pass 
