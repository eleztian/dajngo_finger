from django.db import models
# Create your models here.

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )
    title = models.CharField('标题', max_length = 70)
    body  = models.TextField('正文')
    create_time = models.DateTimeField('创建时间', auto_now_add = True)
    last_modified_time = models.DateTimeField('修改时间', auto_now = True)
    status = models.CharField('文章状态', max_length = 1, choices = STATUS_CHOICES)
    abstract = models.CharField('摘要', max_length = 154, blank = True, null = True,
                                help_text  = "可选， 如若为空将摘取正文前154个字符")
    views = models.PositiveIntegerField('浏览量', default = 0)
    likes = models.PositiveIntegerField('点赞数', default = 0)
    topped = models.BooleanField('置顶', default = False)
    cateory = models.ForeignKey('Category', verbose_name = '分类',
                                null = True,
                                on_delete = models.SET_NULL)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-last_modified_time']


class Category(models.Model):
    name = models.CharField('类名', max_length = 20)
    created_time = models.DateTimeField('创建时间', auto_now_add = True)
    last_modefied_time = models.DateTimeField('修改时间', auto_now = True)
    def __str__(self):
        return self.name

class About(models.Model):
    SEX_CHOICES = (
           ('Man', 'Man'),
           ('Women', 'Women'),
          )
    name = models.CharField('姓名', max_length = 20)
    sex = models.CharField('性别', max_length = 5, choices = SEX_CHOICES)
    age  = models.DateField('出生')
    email = models.EmailField('邮箱')
    identity = models.CharField('身份', max_length = 20)  
    say = models.TextField('我说')
   
    def __str__(self):
        return self.name

class Contract(models.Model):
    name = models.CharField('姓名',max_length = 20)
    email = models.EmailField('邮箱')
    subject = models.CharField('主题', max_length = 100)
    message = models.TextField('信息')

class Comment(models.Model):
    article_id = models.ForeignKey('Article',verbose_name='文章',
                                   null = True,
                                   on_delete = models.SET_NULL)
    name = models.CharField('姓名',max_length = 20)
    email = models.EmailField('邮箱')
    message = models.TextField('信息')
    create_time = models.DateTimeField('时间', auto_now_add = True)




