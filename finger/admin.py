from django.contrib import admin
from .models import FingerPrint,Student,Atendance,FingerDevice,FingerDown,FingerDelete

class FingerPrintAdmin(admin.ModelAdmin):
    list_display = ('Fid','Fdel')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('Sname', 'Sid', 'StotalTime', 'Sfinger')
    list_filter = ('Sid','Sfinger')
    actions = ['delete']
    def delete(self,request,obj):
        for i in obj:
            i.Sfinger.Fdel = True
            i.Sfinger.save()
        obj.delete()




class AtendenceAdmin(admin.ModelAdmin):
    list_display = ('Astudent','Adate', 'Astart', 'Aend')
    list_filter = ('Adate',)

class FingerDeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'FDaddress', 'FDname')
    list_filter = ('id', 'FDaddress', 'FDname')
    actions = ['Delete']

    def Delete(self, request, obj):     #删除设备的同时删除该设备的下载记录
        for i in obj:
            FingerDown.objects.filter(Ddevice=i)
        obj.delete()

class FingerDownAdmin(admin.ModelAdmin):
    list_display = ('Ddevice','Dfinger')
    list_filter  = ('Ddevice','Dfinger')

admin.site.register(FingerPrint, FingerPrintAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Atendance, AtendenceAdmin)
admin.site.register(FingerDevice,FingerDeviceAdmin)
admin.site.register(FingerDown,FingerDownAdmin)
