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
    template = loader.get_template('uploader/index.html')
    if "fileselect" in request.FILES:
        template = loader.get_template('uploader/ajax.html')        
        ufile = request.FILES['fileselect']

        if ufile.size < 50000000: # 50 Megabyte
            fileid = ''.join([random.choice(string.ascii_letters
                                            + string.digits) for n in range(7)])

            with default_storage.open(FILEDIR + fileid, 'wb+') as destination:
                for chunk in ufile.chunks():
                    destination.write(chunk)

            dbfile = File(_id=fileid, name=ufile.name,
                          mime=magic.from_file(FILEDIR + fileid, mime=True),
                          upload_date=timezone.now(),
                          user=request.user if request.user.is_authenticated else None)
            dbfile.save()
            return HttpResponse(template.render({'file_id': fileid, "file_name": ufile.name},
                                                request=request))
        return HttpResponse(template.render({"file_toobig": True}, request=request))
    template = loader.get_template('uploader/index.html')
    return HttpResponse(template.render({}, request=request))

def handle404(request):
    """ Renders 404 template """
    template = loader.get_template('uploader/index.html')
    return HttpResponse(template.render({"file_notfound": True}, request))
