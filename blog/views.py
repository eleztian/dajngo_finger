from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import Article, Category, Contract,Comment
import markdown2
import datetime
from django.core.mail import EmailMultiAlternatives,send_mail  
def setEmail(request):
    if request.method == "POST":
        send_mail(request.POST['subject'],
                  request.POST['name']+':         Message: '+request.POST['message'],
                  request.POST['email'], 
                  ['544347795@qq.com',], 
fail_silently=False)
        return HttpResponse(u'发送邮件成功')
    return render_to_response('blog_index.html')

def comment(request,article_id):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        article = Article.objects.get(id = article_id)
        comment = Comment(
                         article_id = article,
                         name = name,
                         email = email,
                         message = message,)
        comment.save()
        send_mail(name+' 评论了你的文章（'+article.__str__()+'）', message, email, ['544347795@qq.com',], fail_silently = False)
        return HttpResponse('ok');
    return HttpResponse('error')

class IndexView(ListView):
    template_name = 'blog_index.html'
    context_object_name = 'article_list'
    def get_queryset(self):
        article_list = Article.objects.filter(status = 'p')
        for article in article_list:
             article.body = markdown2.markdown(article.body, )
        return article_list
    def get_context_data(self, **kwargs):
        date_now = datetime.datetime.now()
        date_ = date_now - datetime.timedelta(days = 7)
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['recent_list']   = Article.objects.filter(status = 'p', last_modified_time__range = (date_, date_now)).order_by('last_modified_time')
        return super(IndexView, self).get_context_data(**kwargs)

class IndexViewFull(ListView):
    template_name = 'blog_indexFull.html'
    context_object_name = 'article_list'
 
    def get_queryset(self):
        article_list = Article.objects.filter(status = 'p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, )
        return article_list
    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(IndexViewFull, self).get_context_data(**kwargs)

class ArticleDetailView(DetailView):
    model = Article
    tempalte_name = 'blog_detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'
    
    def get_object(self,**kwargs):
        obj = super(ArticleDetailView, self).get_object()
        obj.views += 1
        obj.save()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'],)
        return obj
    def get_context_data(self, **kwargs):
        kwargs['comment_list'] = Comment.objects.filter(article_id = self.kwargs['article_id']).order_by('create_time')
        return super(ArticleDetailView, self).get_context_data(**kwargs)
class CategoryDetailView(ListView):
      template_name = 'blog_index.html'
      context_object_name = 'article_list'
      def get_queryset(self):
          article_list = Article.objects.filter(cateory_id = self.kwargs['cate_id'],status = 'p')
          for article in article_list:
               article.body = markdown2.markdown(article.body, )
          return article_list
      def get_context_data(self, **kwargs):
          kwargs['category_list'] = Category.objects.all().order_by('name')
          return super(CategoryDetailView, self).get_context_data(**kwargs)

class IndexAdout(ListView):
    template_name = 'blog_about'
    context_object_name = 'aboutme_list'
    
    def get_queryset(self):
        aboutme_list = Article.objects.filter(status = 'p')











