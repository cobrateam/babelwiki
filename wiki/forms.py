from django import newforms as forms
from models import *
from google.appengine.ext.db import djangoforms

class PageForm(djangoforms.ModelForm):
    class Meta:
        model = Page
        exclude = ['data', 'owner']
        
        
class TranslatorForm(djangoforms.ModelForm):
    class Meta:
        model = Translation
        exclude = ['data', 'id', 'page', 'accepted']
        
class ContatoForm(forms.Form):
    nome = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    assunto = forms.CharField(required=True)
    mensagem = forms.CharField(required=True, widget=forms.widgets.Textarea())
    
    def send(self):
        mensagem = u'Enviado por %s \n' % self.cleaned_data['nome']
        mensagem += self.cleaned_data['mensagem']
        try:
            parametro = Parametro.objects.get(parametro=u'email')
            email = paramentro.valor
        except:
            email = u'andrewsmedina@gmail.com'
        send_mail(self.cleaned_data['assunto'], mensagem, self.cleaned_data['email'], [email], fail_silently=False)
