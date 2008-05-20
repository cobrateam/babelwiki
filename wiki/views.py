from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.api import users
from models import *
from forms import *
from django.shortcuts import render_to_response

def index(request):   
    return render_to_response('index.html', {'pages':pages})
    
def about(request):
    return render_to_response('about.html')
    
def contact(request):

    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send()
    else:
        form = ContactForm()
        
    return render_to_response('contact.html', {'form':form})
    

def pages(request):
    pages = Page.all()    
    return render_to_response('pages.html', {'pages':pages})
    

def add_page(request):
    
    if request.POST:
        form = PageForm(request.POST)
        
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/')
    else:
        form = PageForm()
    
    return render_to_response('add_page.html', {'form':form})

    
def translate_page(request, page_id):
    page = Page.get_by_id(int(page_id))
    return render_to_response('translate_page.html', {'page':page})
    
    
def sugestions(request, paragraph_id, page_id):
    s = []
    
    p = Page.get_by_id(int(page_id))
    
    sugestions = Translation.all()
    sugestions.filter('id = ', int(paragraph_id))
    sugestions.filter('page = ', p)

    for x in sugestions:
        d = {'sugestion':x.suggestion, 'id':x.key().id()}
        s.append(d)
    
    from utils import simplejson
    return HttpResponse(simplejson.dumps(s))
    
    
def aprove_sugestion(request, id):
       
    s = Translation.get_by_id(int(id))
    s.accepted = True
    s.put()
        
    return HttpResponse('ok')



def add_sugestion(request, paragraph_id, page_id):
    
    if request.POST:
        form = TranslatorForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.id = int(paragraph_id)
            t.page = Page.get_by_id(int(page_id))
            t.language = 'pt_br'
            t.accepted = False

            t.put()
    else:
        form = TranslatorForm()
    
    return HttpResponse('ok')

