#!/usr/bin/env python


import json
import logging

from django.http import Http404
from django.utils.functional import wraps
from django.utils.translation import ugettext as _

## from desktop.lib.django_util import JsonResponse
## from desktop.lib.exceptions_renderable import PopupException
from desktop.lib.i18n import force_unicode

LOG = logging.getLogger(__name__)



def api_error_handler(func):
  def decorator(*args, **kwargs):
    response = {}
    
    try:
      return func(*args, **kwargs)
    except SessionExpired, e:
      response['status'] = -2    
    except QueryExpired, e:
      response['status'] = -3
    except QueryError, e:
      response['status'] = 1
      response['message'] = force_unicode(str(e))
    except Exception, e:
      response['status'] = -1
      response['message'] = force_unicode(str(e))
    finally:
      if response:
        ##return JsonResponse(response)
        return HttpResponse(json.dumps(response), mimetype="application/json")

  return decorator


def json_error_handler(view_fn):
  def decorator(*args, **kwargs):
    try:
      return view_fn(*args, **kwargs)
    except Http404, e:
      raise e
    except Exception, e:
      response = {
        'error': str(e)
      }
      return HttpResponse(json.dumps(response), mimetype="application/json")
      ##return JsonResponse(response, status=500)
  return decorator
