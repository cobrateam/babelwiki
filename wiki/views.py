from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.api import users
from models import *
from forms import *
from django.shortcuts import render_to_response


def index(request):   
    user = users.get_current_user()
    lurl = users.create_logout_url("/") if user else users.create_login_url("/")
    
    return render_to_response('index.html', {'user':user, 'lurl': lurl})
    
    
def about(request):
    user = users.get_current_user()
    lurl = users.create_logout_url("/") if user else users.create_login_url("/about")
    
    return render_to_response('about.html', {'user':user, 'lurl': lurl})
    
    
def contact(request):
    user = users.get_current_user()
    lurl = users.create_logout_url("/") if user else users.create_login_url("/contact")

    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send()
    else:
        form = ContactForm()
        
    return render_to_response('contact.html', {'form':form, 'user':user, 'lurl': lurl})
    

def pages(request):
    user = users.get_current_user()
    lurl = users.create_logout_url("/") if user else users.create_login_url("/pages")
    
    pages = Page.all()
    return render_to_response('pages.html', {'pages':pages, 'user':user, 'lurl': lurl})
    

def add_page(request):
    user = users.get_current_user()
    lurl = users.create_logout_url("/") if user else users.create_login_url("/add_page")
    
    if not user:
        return HttpResponseRedirect(users.create_login_url("/add_page"))    

    if request.POST:
        form = PageForm(request.POST)
        
        if form.is_valid():
            p = form.save(commit=False)
            p.by = users.get_current_user()
            p.put()

            return HttpResponseRedirect('/translate_page/%d/' % p.key().id())
    else:
        form = PageForm()
    
    return render_to_response('add_page.html', {'form':form, 'user':user, 'lurl': lurl})

    
def translate_page(request, page_id):
    user = users.get_current_user()
    lurl = users.create_logout_url("/") if user else users.create_login_url("/translate_page/%s" % page_id)

    page = Page.get_by_id(int(page_id))
    return render_to_response('translate_page.html', {'page':page, 'user':user, 'lurl': lurl})
    


def suggestions(request):
    s = []
    
    
    suggestions = Translation.all()
    #suggestions = suggestions.filter('paragraph = ', Page.get_by_id(100)).order('-date')

    for x in suggestions:
        d = {'suggestion':x.suggestion, 'id':x.key().id(), 'p':x.paragraph}
        s.append(d)
    
    from utils import simplejson
    return HttpResponse(simplejson.dumps(s))
    
'''    
def aprove_suggestion(request, id):
       
    s = Translation.get_by_id(int(id))
    s.accepted = True
    s.put()
        
    return HttpResponse('ok')
'''


def add_suggestion(request, paragraph_id, page_id):
    
    if request.POST:
        form = TranslatorForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.suggestion = request['suggestion']
            t.paragraph = Paragraph.get_by_id(int(paragraph_id))
            t.page = Page.get_by_id(int(page_id))
            t.language = 'pt_br'
            t.by = users.get_current_user()
            t.put()

            return HttpResponse('ok')
        else:
            return HttpResponse('erro')
    else:
        form = TranslatorForm()
    
    return HttpResponse('ok')

def changes(request):
    #t= Translation.get_by_id(translation_id)

    t_diff = TranslationDiff.all().order('-modified')
    #t_diff = t_diff.filter('translation = ', t)

    return render_to_response('changes.html', {'changes':t_diff})


