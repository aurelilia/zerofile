import datetime, threading, time
from django.core.files.storage import default_storage
from django.utils import timezone
from django_extensions.management.jobs import BaseJob
from zerofile.models import File
from zerofile.settings import DEBUG, FILEDIR

def timer():
    next_call = time.time()
    while True:
        next_call = next_call + 60
        execute()
        time.sleep(next_call - time.time())

def execute():
    files = File.objects.filter(deleted=False).exclude(expiry__gte=timezone.now())
    for file in files:
        delete_file(file._id)
        file.deleted = True
        file.save()

def delete_file(fileid):
    default_storage.delete(FILEDIR + fileid)

if not DEBUG:
    print("Running without DEBUG, enabling file autodelete...")
    timerThread = threading.Thread(target=timer)
    timerThread.start()
