from django.core.management.base import BaseCommand
from django.template import loader
from finger.models import Student,Atendance
from datetime import datetime as datet
import datetime
from xlwt import *
from finger.finger_email import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.send_email_to_everyOne()

    def getInfo(self):
        atens = []
        date_now = datet.now()
        date_ = date_now - datetime.timedelta(days = 7)
        aten = Atendance.objects.filter(Adate__range = (date_, date_now))
        stus = aten.values('Astudent').distinct()
        for stu in stus:
            atens.append(aten.filter(Astudent__Sid = stu['Astudent']))
        return atens

    def getXls(self):
        w = Workbook(encoding='utf-8')
        self.atens = self.getInfo()
        self.tableNme = 'qrs' + datet.now().strftime("%y-%m-%d") + '.xls' #文件名
        for stu in self.atens:
            if stu.__len__() == 0:
                continue
            sheet = w.add_sheet(stu[0].Astudent.Sname)
            #  表头
            sheet.write(0, 0, '姓名')
            sheet.write(0, 1, '学号')
            sheet.write(0, 2, '日期')
            sheet.write(0, 3, '开始时间')
            sheet.write(0, 4, '结束时间')
            sheet.write(0, 5, '有效时间(Min)')
            # 数据
            row = 1
            for aten in stu:
                sheet.write(row, 0, aten.Astudent.Sname)
                sheet.write(row, 1, aten.Astudent.Sid)
                sheet.write(row, 2, aten.Adate.strftime("%Y-%m-%d"))
                sheet.write(row, 3, aten.Astart.strftime("%H:%m"))
                sheet.write(row, 4, aten.Aend.strftime("%H:%m"))
                if aten.Ais == 'Y':
                    time = (int(aten.Aend.hour) - int(aten.Astart.hour))*60 \
                         + int(aten.Aend.minute) - int(aten.Astart.minute)
                else:
                    time = 0
                sheet.write(row, 5, str(time))
                row += 1
        w.add_sheet("...")      #防止w为空
        w.save(self.tableNme)

    def send_email_to_everyOne(self):
        subject, from_email, to= "B302本周考勤", "544347795@qq.com", ['544347795@qq.com']
        students = Student.objects.all()
        stus_email = students.values('Semail').distinct()
        for emai in stus_email:     #获取所有学生的邮箱
            if emai['Semail'] != None:
                to.append(emai['Semail'])
        self.getXls()
        html_content = loader.render_to_string(
                                'EmailTemp.html',  # 需要渲染的html模板
                                {
                                    'students_list':students ,
                                }
                        )
        if send_email(subject = subject,to_email_list = to,\
                      message = html_content,file_path = self.tableNme):
            print('ok')

