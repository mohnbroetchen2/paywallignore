import os
import wget
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import string
import sys

from .forms import FnewUrl
from .models import Url
from django.utils.crypto import get_random_string

@login_required
def home_view(request):
    return render(request,'home.html',{'form':FnewUrl(),})

def download_view(request):
    try:
        if request.method == 'POST':  # If the form has been submitted...
            form = FnewUrl(request.POST)  # A form bound to the POST data
            if form.is_valid():
                data = form.cleaned_data
                nurl = Url.objects.filter(url=data['url'])
                if not nurl:
                    nurl = form.save()
                    nurl.ofile =  get_random_string(8,string.ascii_lowercase + string.digits) + '.html'
                    nurl.pfile =  'p_'+ nurl.ofile 
                    nurl.save()
                    file_path = os.path.join(settings.MEDIA_ROOT, '{}'.format(nurl.ofile))
                    req = requests.get(nurl.url, stream=True)
                    if req.status_code == 200:
                        chunk=2048
                        with open(file_path, 'wb') as f:
                            for chunk in req.iter_content(chunk):
                                f.write(chunk)
                            f.close()
                        f = open(file_path, "r") 
                        soup = BeautifulSoup(f, 'html.parser')
                        #head_tag = soup.head
                        #link_tag = soup.link.extract() 
                        for link in soup.find_all("link"): 
                            link.decompose()
                        for script in soup.find_all("script"): 
                            script.decompose()
                        nav = soup.nav
                        #messages.add_message(request, messages.INFO, 'newurl')
                        for navhref in nav.find_all("a"):
                            href = navhref['href']
                            newhref= href.replace("/","_")
                            #messages.add_message(request, messages.INFO, 'newurl {}'.format(newhref))
                            #newtext = BeautifulSoup("+", "html")
                            #navhrefs.find(":").replace_with(newtext)
                            #messages.add_message(request, messages.INFO, 'newurl {}'.format(navhrefs))
                            #text = navhrefs.replace_with("/","_")
                            ##text = navhrefs.replace_with(":","+")
                            #text = navhrefs.replace("https://otz","+")
                            #messages.add_message(request, messages.INFO, 'newurl {}'.format(text ))
                        new_file_path =  os.path.join(settings.MEDIA_ROOT, nurl.pfile)
                        new_file = open(new_file_path, "x")   
                        new_file.write(soup.prettify())  
                        new_file.close()
                        file_path = new_file_path
                else:
                    file_path = os.path.join(settings.MEDIA_ROOT, nurl[0].pfile)
                if os.path.exists(file_path):       
                    #messages.add_message(request, messages.INFO, 'URL {}'.format(file_path))
                    #return HttpResponseRedirect('/{}'.format(file_path))
                    full_file_path = os.path.join(settings.DOMAIN,file_path)
                    #return render(request,'show.html',{'url':full_file_path,})
                    return HttpResponseRedirect(full_file_path)
        return HttpResponseRedirect('/{}'.format(file_path))
    except BaseException as e:
        messages.error(request, 'Fehler {} in Zeile {}'.format(e,sys.exc_info()[2].tb_lineno)) 
        return HttpResponseRedirect('/')
