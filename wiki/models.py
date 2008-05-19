#coding: utf-8
from google.appengine.ext import db

class Page(db.Model):

    MARKUP_CHOICES = (
        ('text'),
        ('markdown'),
        ('textile'),
        ('reStructuredText'),
        ('html'),
    )

    title = db.StringProperty('titulo')
    text = db.TextProperty('Texto')
    license = db.StringProperty('Licença')
    link = db.StringProperty('Endereço URL')
    markup = db.StringProperty(choices=MARKUP_CHOICES)
    date = db.DateTimeProperty(auto_now_add=True)
    
    def paragraphs(self):
        p = Paragraph.all()
        p = p.filter('page = ', self).order('id')
        return p
        
    def translations(self):
        t = Translation.all()
        t = t.filter('page = ', self).order('id')

    def __unicode__(self):
        return "%s - %s" % (self.title, self.language)
        
    def put(self):
        super(Page, self).put()

        i = 1
        for t in self.text.split('\n'):
            p = Paragraph(page=self, text=t, id=i)
            p.put()
            i += 1        

class Paragraph(db.Model):
    page = db.ReferenceProperty(Page)
    text = db.StringProperty()
    id = db.IntegerProperty()
    
    def translation(self):
        try:
            t = Translation.all()
            t = t.filter('page = ', self.page)
            t = t.filter('id = ', int(self.id))
            t = t.filter('accepted = ', True)
            return t[0]
        except:
            return ''
        
    def teste(self):
        return 'teste'
    
    def __unicode__(self):
        return self.text
        
        
class Translation(db.Model):
    page = db.ReferenceProperty(Page)
    suggestion = db.TextProperty()
    accepted = db.BooleanProperty()
    language = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    id = db.IntegerProperty()
    
    def __unicode__(self):
        return self.suggestion
