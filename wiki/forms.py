from django import newforms as forms
from models import *
from google.appengine.ext.db import djangoforms
from google.appengine.api import mail

class PageForm(djangoforms.ModelForm):

    title = forms.CharField(required=True) 
    #text = forms.CharField(required=True, widget=forms.widgets.Textarea)

    class Meta:
        model = Page
        exclude = ['data', 'by']
        
        
class TranslatorForm(djangoforms.ModelForm):
    class Meta:
        model = Translation
        exclude = ['data', 'id', 'page', 'accepted', 'by']
        
class ContactForm(forms.Form):
    nome = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    assunto = forms.CharField(required=True)
    mensagem = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'cols':50, 'rows':10}))
    
    def send(self):
        mensagem = u'Enviado por %s \n' % self.cleaned_data['nome']
        mensagem += self.cleaned_data['mensagem']

        email = u'andrewsmedina@gmail.com'
        
        mail.send_mail(email, self.cleaned_data['email'], self.cleaned_data['assunto'], mensagem)
