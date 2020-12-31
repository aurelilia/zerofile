from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from zerofile.models import File


def viewfiles(request):
    """ List a user's uploaded files """
    if request.user.is_authenticated:
        files = []
        for ufile in File.objects.filter(user=request.user):
            files.append({
                'name': ufile.name, 
                'date': ufile.upload_date, 
                'fid': ufile._id, 
                'deleted': ufile.deleted, 
                'expiry': ufile.expiry
            })
        template = loader.get_template('manager/files.html')
        return HttpResponse(template.render({'files': files}, request))
    return HttpResponseRedirect('/')
