import string
import random
import magic
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.template import loader
from zerofile.models import File
from zerofile.settings import FILEDIR

class ReqEx(Exception):
    pass

def upload(request):
    """ Processes form answer and stores it in db, returns upload page if answer is empty """
    if 'fileselect' in request.FILES and 'timeout' in request.POST:
        try:
            return upload_file(request)
        except ReqEx as e:
            return e.args[0]

    template = loader.get_template('uploader/index.html')
    return HttpResponse(template.render({}, request=request))

def upload_file(request):
    ufile = request.FILES['fileselect']
    validate_size(request, ufile)
    fileid = write_file(ufile)
    mime = get_mime(request, fileid)
    expiry = get_expiry(request.POST['timeout'])

    dbfile = File(_id=fileid, name=ufile.name,
                mime=mime,
                upload_date=timezone.now(),
                user=request.user if request.user.is_authenticated else None,
                expiry=expiry)
    dbfile.save()

    template = loader.get_template('uploader/ajax.html')
    return HttpResponse(template.render({'file_id': fileid, 'file_name': ufile.name},
                                        request=request))

def validate_size(request, file):
    if file.size > 50000000: # 50 Megabyte
        template = loader.get_template('uploader/index.html')
        raise ReqEx(HttpResponse(template.render({'file_toobig': True}, request=request)))

def write_file(file):
    fileid = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(7)])
    with default_storage.open(FILEDIR + fileid, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return fileid

def get_mime(request, fileid):
    mime = magic.from_file(FILEDIR + fileid, mime=True)
    if mime in NOT_ALLOWED_MIMES and not request.user.is_authenticated:
        template = loader.get_template('uploader/not_allowed_mime.html')
        raise ReqEx(HttpResponse(template.render({}, request=request)))
    return mime

def get_expiry(time):
    try:
        delta = TIMEDELTAS[time]
        return timezone.now() + delta
    except:
        template = loader.get_template('uploader/invalid_timeout.html')
        raise ReqEx(HttpResponse(template.render({}, request=request)))

NOT_ALLOWED_MIMES = ["text/html", "text/x-php"]
TIMEDELTAS = {
    "minute": timedelta(minutes = 1),
    "hour": timedelta(hours = 1),
    "day": timedelta(days = 1),
    "week": timedelta(weeks = 1)
}
