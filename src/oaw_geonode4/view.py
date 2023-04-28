from django.http.response import Http404
from geonode.layers.views import _resolve_dataset, _PERMISSION_MSG_VIEW
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _

def dataset_redirect(request, layername):
    try:
        layer = _resolve_dataset(
            request,
            layername,
            'base.view_resourcebase',
            _PERMISSION_MSG_VIEW)
    except PermissionDenied:
        return HttpResponse(_("Not allowed"), status=403)
    except Exception:
        raise Http404(_("Not found"))
    if not layer:
        raise Http404(_("Not found"))

    return HttpResponseRedirect(layer.detail_url)