from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from zerofile.models import File
from zerofile.settings import FILEDIR

def download(request, file_id):
    """ Serve file corresponding to the id """
    dbfile = get_object_or_404(File, _id=file_id)
    with open(FILEDIR + dbfile._id, "rb") as i:
        response = HttpResponse(i.read(), content_type=dbfile.mime)
        response['Content-Disposition'] = 'inline; filename=%s' % dbfile.name
        return response
