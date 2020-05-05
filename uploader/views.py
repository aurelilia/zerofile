import string
import random
import magic
from django.utils import timezone
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.template import loader
from zerofile.models import File
from zerofile.settings import FILEDIR


def upload(request):
    """ Processes form answer and stores it in db, returns upload page if answer is empty """
    if 'fileselect' in request.FILES:
        ufile = request.FILES['fileselect']

        if ufile.size > 50000000: # 50 Megabyte
            template = loader.get_template('uploader/index.html')
            return HttpResponse(template.render({'file_toobig': True}, request=request))

        fileid = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(7)])
        with default_storage.open(FILEDIR + fileid, 'wb+') as destination:
            for chunk in ufile.chunks():
                destination.write(chunk)

        mime = magic.from_file(FILEDIR + fileid, mime=True)
        not_allowed_mimes = ["text/html", "text/x-php"]
        if mime in not_allowed_mimes and not request.user.is_authenticated:
            template = loader.get_template('uploader/not_allowed_mime.html')
            return HttpResponse(template.render({}, request=request))

        dbfile = File(_id=fileid, name=ufile.name,
                    mime=mime,
                    upload_date=timezone.now(),
                    user=request.user if request.user.is_authenticated else None)
        dbfile.save()

        template = loader.get_template('uploader/ajax.html')
        return HttpResponse(template.render({'file_id': fileid, 'file_name': ufile.name},
                                            request=request))

    template = loader.get_template('uploader/index.html')
    return HttpResponse(template.render({}, request=request))
