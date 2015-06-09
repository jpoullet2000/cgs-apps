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

from ranking.decorators import api_error_handler

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
     - sourceUris: a list of URIs pointing to VCF files in the cluster
     - format: "VCF" 

    ## 
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
def ranking_test(request):
    """ Search a variant by some criteria (see doc for more details and if not https://cloud.google.com/genomics/v1beta2/reference/variants/search)
    
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
    fprint("============")
    fprint(criteria_json)
    #callsetid = json.loads(criteria)['callSetIds']
    try: 
        criteria = json.loads(criteria_json)
    except Exception:
        result['status'] = -1
        result['error'] = "Sorry, an error occured: Impossible to load the criteria. Please check that they are in a JSON format."
        return HttpResponse(json.dumps(result), mimetype="application/json")

    criteria_keys = [str(s) for s in criteria.keys()]
    fprint(criteria['callSetIds'])
    if 'callSetIds' not in criteria_keys:
    #if 'callSetIds' not in request.POST.keys():
        result['status'] = -1
        #result['keys'] = request.POST.keys()
        #result['criteria'] = callsetid
        result['error'] = "Information about the callSetsIds (sample information should be available)."
        return HttpResponse(json.dumps(result), mimetype="application/json")
        ##return JsonResponse(result)

    callsetids = [str(s) for s in criteria['callSetIds']]
    
    fprint(','.join(callsetids))
    ## getting data from DB
    try:
        query_server = get_query_server_config(name='impala')
        db = dbms.get(request.user, query_server=query_server)
    except Exception:
        result['status'] = 0
        result['error'] = "Sorry, an error occured: Impossible to connect to the db."
        return HttpResponse(json.dumps(result), mimetype="application/json")

    try:
        ## TODO: 
        ## - the variant_table should be defined from the config files not as a string as here  
        ## - the callsetids should map to a specific field (here readGroupSets_readGroups_info_patientId) in the variant table, this info should be read from the config files, not as a string as here.
        ## the listVars should be read from the config files as well
        variants_table = "jpoullet_1000genomes_1E7rows_bis"
        listVars = ["id","readGroupSets_readGroups_info_patientId"]
        fprint(variants_table)
        #fprint(str(criteria.keys()[0]))
        searchCriteriaList = list()
        for k in criteria.keys():
            fprint(criteria[str(k)])
            if str(k) == 'callSetIds': 
                refvar = "readGroupSets_readGroups_info_patientId" ## TODO: this must be read from the config files 
            elif str(k) == 'referenceName':
                refvar = 'variants_referenceName' ## TODO: this must be read from the config files
            else:
                pass # TODO: there should be an error when the user chooses some inexisting variable 
            fprint(refvar + " in ('" + "','".join([str(s) for s in criteria[str(k)]]) + "')")
            searchCriteriaList.append(refvar + " in ('" + "','".join([str(s) for s in criteria[str(k)]]) + "')")

        searchCriteriaTxt = " AND ".join(searchCriteriaList)
        fprint(searchCriteriaTxt)
        
        hql = "SELECT " + ",".join(listVars) + " FROM " + variants_table + " WHERE " + searchCriteriaTxt
        #hql = "SELECT " + ",".join(listVars) + " FROM " + variant_table + " WHERE readGroupSets_readGroups_info_patientId IN ('" + "','".join(callsetids) + "')"
        fprint(hql)

    except Exception: 
        result['status'] = 0
        result['error'] = "Sorry, an error occured: a syntax error appears in the definition of the criteria. The query could not be built."
        return HttpResponse(json.dumps(result), mimetype="application/json")        

    try:
        query = hql_query(hql)
        handle = db.execute_and_wait(query, timeout_sec=5.0)

    except Exception:
        result['status'] = 0
        result['error'] = "The query cannot be performed: %s" % hql
        return HttpResponse(json.dumps(result), mimetype="application/json")
    
    if handle:
        data = db.fetch(handle)
        ## TODO: rebuild the variant resource such as defined in the API
        ## field parser that would take the config files as input to retrieve the generate back the structured json
        ## results['variants'] = getStructuredJson(list(data.rows))
        result['variants'] = list(data.rows())
        result['status'] = 1
        db.close(handle)  

    else: 
        result['error'] = 'No result found.'
    return HttpResponse(json.dumps(result), mimetype="application/json")
    

## callsets
@api_error_handler
def callsets_get(request):
    """ Gets a call set by ID 
    """
    
    pass 
