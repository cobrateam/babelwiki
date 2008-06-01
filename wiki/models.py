#coding: utf-8
from __future__ import division
from google.appengine.ext import db
from utils.diff_match_patch import diff_match_patch
#import logging

def diff(t1, t2):
    dmp = diff_match_patch()
    patch = dmp.patch_make(t1, t2)
    return dmp.patch_toText(patch)
    
class Page(db.Model):

    MARKUP_CHOICES = (
        ('text'),
        ('markdown'),
        ('textile'),
        ('reStructuredText'),
        ('html'),
    )

    title = db.StringProperty('Titulo')
    text = db.TextProperty('Texto')
    license = db.StringProperty('Licença')
    link = db.StringProperty('Endereço URL')
    markup = db.StringProperty(choices=MARKUP_CHOICES)
    date = db.DateTimeProperty(auto_now_add=True)
    by = db.UserProperty()
    
    def paragraphs(self):
        p = Paragraph.all()
        p = p.filter('page = ', self).order('id')
        return p
        
    def translations(self):
        t = Translation.all()
        t = t.filter('page = ', self).order('paragraph')
        return t

    def translateds(self):
        p = Paragraph.all()
        p = p.filter('translated = ', True)
        p = p.filter('page = ', self).order('id')
        return p
    def percentage(self):
        try:
            p = (self.translateds().count() / self.paragraphs().count()) * 100
        except ZeroDivisionError: # there is something strange going on, no paragraphs?
            p = 100 # no paragraphs, so everything is translated, right?
        return p

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
    translated = db.BooleanProperty()
    
    
    def translation(self):
        try:
            t = Translation.all()
            #t = t.filter('page = ', self.page)
            t = t.filter('paragraph = ', self).order('-date')

            return t[0].suggestion
        except:
            return ''
    
    def __unicode__(self):
        return self.text

    def put(self):
        if self.text == '':
            self.translated = True
        super(Paragraph, self).put()
        
        
class Translation(db.Model):
    suggestion = db.TextProperty()
    language = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    paragraph = db.ReferenceProperty(Paragraph)
    page = db.ReferenceProperty(Page)
    by = db.UserProperty()
    
    def new_change(self):
        t = TranslationDiff()
        t.translation = self

        try:

            old = TranslationDiff.all()
            old = old.filter('paragraph = ', self.paragraph).order('-modified')

            s = old.diff
        except:
            s = ''

        t.diff = diff(self.suggestion, s)
        t.by = self.by
        t.comment = ''
        t.put()

    def put(self):
        super(Translation, self).put()
        self.paragraph.translated = True
        self.paragraph.put()
        self.new_change()
    
    def __unicode__(self):
        return self.suggestion

class TranslationDiff(db.Model):
    translation = db.ReferenceProperty(Translation)
    diff = db.TextProperty()
    comment = db.StringProperty()
    modified = db.DateTimeProperty(auto_now_add=True)
    revision = db.IntegerProperty()
    by = db.UserProperty()

    def revert(self):
        dmp = diff_match_patch()
        patch = dmp.patch_fromText(self.diff)
        self.translation.suggestion = dmp.patch_apply(patch, self.translation.suggest)[0]
        self.translation.put()

    def put(self):
        try:
            self.revision = TranslationDiff.all().filter('translation =', self.translation).order('-revision')[0].revision + 1
        except:
            self.revision = 1
        super(TranslationDiff, self).put()

    def show_diff(self):
        dmp = diff_match_patch()
        return dmp.diff_prettyHtml(self.diff)

    def __unicode__(self):
        return self.suggestion
