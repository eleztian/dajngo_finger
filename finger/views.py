from django.http import HttpResponse,HttpResponseRedirect
from finger.models import Student,FingerPrint,Atendance,FingerDevice,FingerDown
from django.views.generic.list import ListView
import time
from finger.finger_email import send_email
from django.template import loader
from finger.finger_config import *
def putFinger(request):
    message = ''


#    fid = str(request.POST.get('Id')).strip()
    stu_name = str(request.POST.get('name' )).strip()
    stu_id   = str(request.POST.get('id'   )).strip()
    stu_email= str(request.POST.get('email')).strip()
    f1       = str(request.POST.get('F1'   )).strip()
    f2       = str(request.POST.get('F2'   )).strip()
    psw      = str(request.POST.get('psw'  )).strip()
    s = FingerPrint.objects.raw('SELECT Fid,MAX(Fid) AS id FROM finger_fingerprint')
    fid = 0
    for i in s:
        fid = str(i.id + 1)
    message += fid.zfill(3)
    if psw == put_psw:
        if stu_id != '' and stu_name != '':
            re = Student.objects.filter(Sid = stu_id)
            if re.count() == 0:
                stu = Student(Sname = stu_name, Sid = stu_id, Semail = stu_email)
                try:
                    stu.save()
                    if True:
                        fingerPrint = FingerPrint(Fid = int(fid), Ftemp1 = f1, Ftemp2 = f2)
                        fingerPrint.save()
                        Student.objects.filter(Sid = stu_id).update(Sfinger = fingerPrint)
                        message += 'OK fingerid %s' % fid
                    else:
                        message += 'ERROR finger temp error'
                        Student.objects.filter(Sid = stu_id).delete()
                except Exception as e:
                    message += 'ERROR'+ e
            else:
                message += 'ERROR this id is exited'
        else:
            message += 'ERROR name or id can\'t be Null'
    else:
        message += 'ERROR psw is wrong'
    return HttpResponse(message)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def getFinger(request):
    message = ''
    address = request.GET.get('addr')
    delmessage=''
    if address == None:
        return HttpResponse(status=404)
    else:
        if address == 'ffffffff':
            addr = hex(FingerDevice.objects.count())[2:].zfill(8)
            device = FingerDevice(FDaddress= addr,FDname=addr)   #新建设备
            device.save()
            return HttpResponse('change%s' % addr)                  #返回新的地址
        else:
            downloed = FingerDown.objects.filter(Ddevice__FDaddress=address).values('Dfinger__Fid')
            all = Student.objects.all().exclude(Sfinger__Fid__in=downloed).filter(Sfinger__Fdel=False)
            if all.count() > 0:
                message += "%s%s%s" % (str(all[0].Sfinger.Fid).zfill(3), all[0].Sfinger.Ftemp1, all[0].Sfinger.Ftemp2)
            delFinger = FingerPrint.objects.filter(Fdel=True)
            delmessage += str(delFinger.count()).zfill(3)
            for j in delFinger:
                delmessage += str(j.Fid).zfill(3)
            NowTime = time.strftime("%a %H:%M",time.localtime(time.time()))
            return HttpResponse('Time'+ NowTime + 'del'+ delmessage+'\n'+ message)

def getFingerBack(request):
    id = request.GET.get('id')
    addr = request.GET.get('addr')
    finger = None
    device = None
    if(id):
        if(addr):
            try:
                finger = FingerPrint.objects.get(Fid=int(id))
            except:
                return HttpResponse(status = 404)
            try:
                device = FingerDevice.objects.get(FDaddress=addr)
            except:
                device = FingerDevice(FDaddress=addr, FDname = addr)
                device.save()
            try:
                FingerDown(Dfinger=finger,Ddevice=device).save()
            except:
                return HttpResponse(status = 404)
            #邮件通知  学生和管理员
            subject, from_email, to_list = "指纹录入","544347795@qq.com",['544347795@qq.com']
            try:
                stu = Student.objects.get(Sfinger__Fid = int(id))
                to_list.append(stu.Semail)
                html_content = loader.render_to_string(
                        'finger_get_email.html',  # 需要渲染的html模板
                        {
                            'student': stu,
                        }
                )
                send_email(subject = subject,to_email_list = to_list,message = html_content)
            except:
                pass
            delFinger = FingerPrint.objects.filter(Fdel=True)
            for i in delFinger:
                i.delete()
    return HttpResponse("")

def student_Search(request,year,month):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        return HttpResponseRedirect('/finger/atendance/%s/%s/%s' % (year,month,student_id))
    return HttpResponseRedirect('./')

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode())
    return m.hexdigest()

def FingerAtendance(request):
    pas = str(request.GET.get('pas')).strip()[:32]
    fingerId  = request.GET.get('id')

    if pas == md5("finger"+aten_pass+fingerId+aten_user):       #密码验证正确
        stu = Student.objects.filter(Sfinger__Fid=int(fingerId))
        if stu.__len__() != 0:             #存在这个指纹
            #return HttpResponse(stu[0].Sname+str(stu[0].Sfinger.Fid))
            ates = Atendance.objects.filter(Astudent=stu[0]).filter(Ais='N')
            if ates.__len__() == 0:        #第一次签到
                ate = Atendance(Astudent=stu[0],Ais='N')
                ate.save()
                return HttpResponse ("mesg:0")
            else :                         #第二次签到
                ate = ates[0]
                if str(ate.Adate) == time.strftime("%Y-%m-%d",time.localtime(time.time())):
                    ate.Ais = 'Y'
                    ate.save()
                    time_ = int(ate.Aend.hour)*60 + int(ate.Aend.minute) - int(ate.Astart.hour)*60 - int(ate.Astart.minute)
                    stu[0].StotalTime = int(stu[0].StotalTime) + time_      #变化总时间
                    stu[0].save()
                    return HttpResponse ("mesg:1"+str(time_).zfill(3))
        return HttpResponse(status = 404)

    return HttpResponse(status = 403)

class FingerIndex(ListView):
    template_name = 'finger_index.html'
    context_object_name = 'Student_list'

    def get_queryset(self):
        Student_list = Student.objects.all()
        return Student_list

class ShowOneStudentAtendance(ListView):
    template_name = 'finger_show_onestu_atendance.html'
    context_object_name = 'Atendance_ok_list'
    pk_url_kwarg = 'student_id'
    everydayTime = [{'data': [], 'name': 'Times'}]
    def get_queryset(self):
        self.atendance = Atendance.objects.filter(Astudent__Sid = self.kwargs['student_id'])\
                                          .filter(Adate__year   = self.kwargs['year'])\
                                          .filter(Adate__month  = self.kwargs['month'])
        self.Atendance_ok_list = self.atendance.filter(Ais='Y')

        return self.Atendance_ok_list
    def get_context_data(self, **kwargs):
        kwargs['Atendance_not_list'] = self.atendance.filter(Ais='N')
        data = []
        for i in range(1,32):
            data.append([str(i) + ' day', 0])
        for ate in self.Atendance_ok_list:
            data[int(ate.Adate.day)][1] = int(ate.Aend.hour  ) * 60 + int(ate.Aend.minute) - \
                                          int(ate.Astart.hour) * 60 - int(ate.Astart.minute)
        self.everydayTime[0]['data'] = data
        kwargs['everydayTime'] = self.everydayTime
        kwargs['year'] = self.kwargs['year']
        kwargs['month'] = self.kwargs['month']
        kwargs['student_id'] = self.kwargs['student_id']
        return super(ShowOneStudentAtendance, self).get_context_data(**kwargs)

class ShowAllAtendance(ListView):
    template_name = 'finger_show_atendance.html'
    context_object_name = 'Atendance_ok_list'
    pk_url_kwarg = 'student_id'
    everydayTime = [{'data': [], 'name': 'Times'}]
    def get_queryset(self):
        self.atendance = Atendance.objects.filter(Adate__year = self.kwargs['year'])\
                                          .filter(Adate__month=self.kwargs['month'])
        self.Atendance_ok_list = self.atendance.filter(Ais='Y')
        return self.Atendance_ok_list
    def get_context_data(self, **kwargs):
        kwargs['Atendance_not_list'] = self.atendance.filter(Ais='N')
        data = []
        for i in range(31):
            data.append([str(i)+' day', 0])
        for ate in self.Atendance_ok_list:
           data[int(ate.Adate.day)][1] = int(ate.Aend.hour)*60 + int(ate.Aend.minute) - int(ate.Astart.hour)*60 - int(ate.Astart.minute)
        self.everydayTime[0]['data'] = data
        kwargs['everydayTime'] = self.everydayTime
        kwargs['year'] = self.kwargs['year']
        kwargs['month'] = self.kwargs['month']
        return super(ShowAllAtendance, self).get_context_data(**kwargs)

class atendance_sort(ListView):
    template_name = 'finger_atendance_sort.html'
    context_object_name = 'student_list'
    def get_queryset(self):
        self.student_list = Student.objects.order_by('StotalTime').all()[0:3]
        return self.student_list
    def get_context_data(self, **kwargs):
        for (index,stu) in enumerate(self.student_list):
            kwargs['stu_'+str(index)] = stu.Sname
        return super(atendance_sort, self).get_context_data(**kwargs)


