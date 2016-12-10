from django.contrib import admin
from .models import Article, Category,About,Comment
from pagedown.widgets import AdminPagedownWidget
from django import forms
class ArticleForm(forms.ModelForm):
      body = forms.CharField(widget=AdminPagedownWidget())
      class Meta:
          model = Article
          fields = '__all__'

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
    list_display = ('title', 'create_time', 'status', 'views', 'likes', 'topped')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time', 'last_modefied_time')
class ComentAdmin(admin.ModelAdmin): 
    list_display = ('name','email','article_id','create_time','message')
    list_filter  = ('name','article_id')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(About)
admin.site.register(Comment, ComentAdmin)
