from django.db import models

class FingerPrint(models.Model):
    Fid = models.CharField('编号', max_length = 4)
    Ftemp = models.CharField('模板', max_length = 534)    
    def __str__(self):
        return self.Fid
    class Meta:
        ordering = ['Fid']

class Student(models.Model):
    Sname = models.CharField('姓名',max_length = 20)
    Sid   = models.CharField('学号',max_length = 11)
    Sfinger = models.ForeignKey('FingerPrint',verbose_name =  '指纹',
                                 null = True,
                                 on_delete = models.SET_NULL)
    def __str__(self):
        return self.Sname
    class Meta:
        ordering = ['Sid']

class Atendance(models.Model):
    Sid = models.ForeignKey('Student', verbose_name = '学生',
                            null = True,
                            on_delete = models.SET_NULL )
    Sstart = models.DateTimeField('开始时间', auto_now_add = True)
    Send   = models.DateTimeField('结束时间', auto_now = True)
   
