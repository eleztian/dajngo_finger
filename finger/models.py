from django.db import models
import datetime
class FingerPrint(models.Model):
    Fid    = models.AutoField('编号',primary_key=True)
    Ftemp1 = models.CharField('模板1', max_length = 534, null = True)
    Ftemp2 = models.CharField('模板2', max_length = 534,null = True)
    Fdel   = models.BooleanField('删除',default=False)

    def __str__(self):
        return str(self.Fid)
    class Meta:
        ordering = ['Fid']

class Student(models.Model):
    Sname = models.CharField('姓名',max_length = 20)
    Sid   = models.CharField('学号',max_length = 11,primary_key=True)
    Semail= models.EmailField('邮箱',null = True)
    StotalTime = models.IntegerField('总时间', default=0)
    Sfinger = models.ForeignKey(FingerPrint,verbose_name =  '指纹',
                                 null = True,
                                 on_delete = models.SET_NULL,)
    def __str__(self):
        return self.Sname
    class Meta:
        ordering = ['Sid']

class Atendance(models.Model):
    AIS_CHOICES = (
        ('Y','有效'),
        ('N','无效'),
    )
    Astudent = models.ForeignKey(Student, verbose_name='考勤',
                                   null=True)
    Adate  = models.DateField('日期', auto_now_add=True)
    Astart = models.TimeField('开始时间', auto_now_add = True)
    Aend   = models.TimeField('结束时间', auto_now = True)
    Ais    = models.CharField('有效', max_length=1, choices=AIS_CHOICES,default='N')
    def __str__(self):
        return str(self.Adate)
    class Meta:
       ordering = ['Adate']

class FingerDevice(models.Model):
    FDaddress = models.CharField(max_length=8, null=False)
    FDname    = models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.FDaddress
    class Meta:
        ordering = ['FDaddress']

class FingerDown(models.Model):
    Dfinger = models.ForeignKey(FingerPrint,verbose_name="指纹",
                                null=True)
    Ddevice = models.ForeignKey(FingerDevice,verbose_name="设备",
                                null=True)
    def __str__(self):
        return self.Ddevice.FDname

    class Meta:
        unique_together = ("Dfinger", "Ddevice")  # 这是重点

class FingerDelete(models.Model):
    DelFinger = models.ForeignKey(FingerPrint,verbose_name="指纹",
                                null=True)
    def __str__(self):
        return self.DelFinger_Fid