import string
import random
import magic
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.template import loader
from zerofile.settings import FILEDIR

def stream(request):
    template = loader.get_template('streamer/index.html')
    return HttpResponse(template.render({ 'host': True }, request=request))

def receive(request, stream_id):
    template = loader.get_template('streamer/index.html')
    return HttpResponse(template.render({ 'host': False, 'stream_id': stream_id }, request=request))
