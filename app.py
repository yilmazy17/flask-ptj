import os
from flask import Flask
from flask import render_template, current_app, request, redirect, url_for, flash, session, g
from flask_mail import Mail, Message
import psycopg2 as dbapi2
import time
import random
from passlib.hash import pbkdf2_sha256 as hasher


ty = time.localtime().tm_year
tm = time.localtime().tm_mon
td = time.localtime().tm_mday
check = 0


app = Flask(__name__)
app.secret_key = 'onlyıknow'
url = "postgres://kvwrgkebshegcf:aa87eb5072319ace108142f5e23255e66768ea1e77e76db8fbd9480de4fcf13a@ec2-34-202-5-87.compute-1.amazonaws.com:5432/d41ek2217p7u99"
con = dbapi2.connect(url)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'info.partjobs@gmail.com'
app.config['MAIL_PASSWORD'] = 'zuhal1977'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'info.partjobs@gmail.com'
mail = Mail(app)

if __name__ == '__main__':
    app.run()






def home_page():
    return render_template("index.html")
    
def age_regis_page():
    if request.method == "GET":
        return render_template("aceregis.html")
    else:
        cur = con.cursor()
        form_compname = request.form['comp_name']
        form_mersis = request.form['mersis']
        if len(form_mersis) != 16:
            return render_template("aceregis.html", message="Mersis Numarası 16 karakterden oluşmaktadır")
        cur.execute("""select * from "agency" """)
        agencies = cur.fetchall()
        for agency in agencies:
            if form_mersis == agency[0]:
                return render_template("aceregis.html", message="Mersis Numarası zaten sistemde kayıtlı")
        form_office = request.form['office']
        form_password = hasher.hash(request.form['Password'])
        if len(form_password) < 8:
            return render_template("aceregis.html", message="Şifre 8 karakterden büyük olmalıdır")
        cur.execute("""insert into "agency" ("mersis_no","name","office_location","password")values(%s,%s,%s,%s)""",(form_mersis,form_compname,form_office,form_password))
        con.commit()
        flash('Kayıt Başarılı')
        return redirect(url_for("age_regis_page"))
        
def job_post_page():
    if request.method == "GET":
        return render_template("jobpost.html")
    else:
        cur = con.cursor()
        form_jobloc = request.form['Job_Loc']
        form_stunum = request.form['StuNum']
        if int(form_stunum) < 1:
            return render_template("jobpost.html", message="İş için gereken öğrenci sayısı 0 olmamalıdır")
        form_JobDate = request.form['date']
        form_JobDate = request.form['date']
        year = form_JobDate[0:4]
        if int(year) < int(ty):
            return render_template("jobpost.html", message="Girilen Tarih Değeri Günümüzden Küçük Olmamalıdır")
        month = form_JobDate[5:7]
        if int(month) < int(tm):
            return render_template("jobpost.html", message="Girilen Tarih Değeri Günümüzden Küçük Olmamalıdır")
        day = form_JobDate[8:10]
        if int(day) < int(td):
            return render_template("jobpost.html", message="Girilen Tarih Değeri Günümüzden Küçük Olmamalıdır")
        time = form_JobDate[11:len(form_JobDate)]
        form_JobDate2 = 'İş Tarihi: ' + year + '-' + month + '-' + day + ' İş Başlangıç Saati: ' + time
        form_lang = request.form['lang']
        form_wage = request.form['wage']
        form_work_time = request.form['work_time']
        form_work_days = request.form['work_days']
        cur.execute("""insert into "job" ("job_location","work_date","number_of_students","nececity_language","mersis_no","wage","work_time","work_days")values(%s,%s,%s,%s,%s,%s,%s,%s)""",(form_jobloc,form_JobDate2,form_stunum,form_lang,g.pk,form_wage,form_work_time,form_work_days))
        con.commit()
        flash('İş Paylaşıldı')
        return redirect(url_for("job_post_page"))

def code_page():
    if request.method == "GET":
        return render_template("code.html")
    else:
        cur = con.cursor()
        form_mail = request.args.get('form_mail')
        form_namesurn = request.args.get('form_namesurn')
        form_password = request.args.get('form_password')
        form_age = request.args.get('form_age')
        form_school = request.args.get('form_school')
        langlist = request.args.getlist('langlist')
        stringcode = request.args.get('stringcode')
        code = request.form['code']
        
        if code != stringcode:
            return render_template("register.html", message="Onay Kodunu Yanlış Girdiniz Lütfen Tekrar Deneyiniz")
        else:
            cur.execute("""insert into "Student" ("Student_Mail","Name_Surname","Password","University","Age")values(%s,%s,%s,%s,%s)""",(form_mail,form_namesurn,form_password,form_school,form_age))
            con.commit()
            for lang in langlist:
                cur.execute("""insert into "Lan_Table" ("Student_Mail","Extra_Language")values(%s,%s)""",(form_mail,lang))
                con.commit()
            msg = Message('PTJ Ailesine Hoşgeldin', recipients=[form_mail])
            msg.body = 'Merhaba, PTJ Ailesi olarak seni aramızda görmekten Mutluluk Duyuyoruz, Umarım websitemizdeki deneyimden Memnun kalırsın.'
            mail.send(msg)
            flash('Kaydınız Alınmıştır')
            return redirect(url_for("regis_page"))      

    
def regis_page():
    if request.method == "GET":
        return render_template("register.html")
    else:
        cur = con.cursor()
        form_namesurn = request.form["first_name"] + " " + request.form["last_name"]
        form_mail = request.form["email"]
        cur.execute("""select * from "Student" """)
        students = cur.fetchall()
        for student in students:
            if form_mail == student[0]:
                return render_template("register.html", message="Mail adresi zaten mevcut")
        form_password = hasher.hash(request.form["Password"])
        if len(form_password) < 8:
            return render_template("register.html", message="Şifreniz 8 karakterden küçük olmalıdır")
        form_age = request.form["age"]
        form_school = request.form["school"]
        langlist = []
        form_lang = request.form["en"]
        if form_lang != "Yok":
            langlist.append(form_lang)
        form_lang = request.form["al"]
        if form_lang != "Yok":
            langlist.append(form_lang)
        form_lang = request.form["ru"]
        if form_lang != "Yok":
            langlist.append(form_lang)
        form_lang = request.form["ch"]
        if form_lang != "Yok":
            langlist.append(form_lang)
        form_lang = request.form["es"]
        if form_lang != "Yok":
            langlist.append(form_lang)
        form_lang = request.form["ar"]
        if form_lang != "Yok":
            langlist.append(form_lang)
        form_lang = request.form["ja"]
        if form_lang != "Yok":
            langlist.append(form_lang)
        randomlist = []
        for i in range(0,5):
            n = random.randint(0,9)
            randomlist.append(n)
        string_ints = [str(int) for int in randomlist]
        stringcode = string_ints[0] + string_ints[1] + string_ints[2] + string_ints[3] + string_ints[4]
        msg = Message('Kayıt Kodu', recipients=[form_mail])
        msg.body = 'Kaydolmak için kodunuz "' + stringcode + '" olarak verilmiştir. Kodu çalışanımız dahil kimseyle paylaşmayınız.'
        mail.send(msg)
        return render_template("code.html", form_namesurn=form_namesurn, form_mail=form_mail, form_password=form_password, form_school=form_school, form_age=form_age, stringcode=stringcode, langlist=langlist)
        
def reset_code_page():
    if request.method == "GET":
        return render_template("index.html")
    else:
        form_mail = request.form['form_mail']
        cur = con.cursor()
        cur.execute("""select * from "Student" """)
        students = cur.fetchall()
        x = 0
        for student in students:
            if student[0] == form_mail:
                x = 1
        if x == 0:
            return render_template("resetpass.html", message="Girdiğiniz Mail Adresi Sistemde Kayıtlı Değil")
        else:
            randomlist = []
            for i in range(0,5):
                n = random.randint(0,9)
                randomlist.append(n)
            string_ints = [str(int) for int in randomlist]
            stringcode = string_ints[0] + string_ints[1] + string_ints[2] + string_ints[3] + string_ints[4]
            msg = Message('Şifre Yenileme Kodu', recipients=[form_mail])
            msg.body = 'Şifrenizi yenilemek için kodunuz "' + stringcode + '" olarak verilmiştir. Kodu çalışanımız dahil kimseyle paylaşmayınız.'
            mail.send(msg)
            return render_template("code1.html", form_mail=form_mail, stringcode=stringcode)

def bridge():
    return render_template("resetpass.html")

def reset_pass_page():
    if request.method == "GET":
        return render_template("index.html")
    else:
        form_mail = request.args.get('form_mail')
        stringcode = request.args.get('stringcode')
        form_mail =  request.args.get('form_mail')
        stringcode = request.args.get('stringcode')
        code = request.form['code']
        if code != stringcode:
            return render_template("resetpass.html", message = "Kodu Yanlış Girdiniz Lütfen Tekrar Deneyiniz")
        else:
            return render_template("resetpass1.html", form_mail=form_mail, code=code, stringcode=stringcode)

def reset_pass1_page():
    if request.method == "GET":
        return render_template("index.html")
    else:
        form_mail = request.args.get('form_mail')
        stringcode = request.args.get('stringcode')
        code = request.args.get('code')
        if code == stringcode:
            pass1 = request.form['password']
            pass2 = request.form['password1']
            if pass1 != pass2:
                return render_template("resetpass1.html", form_mail=form_mail, stringcode=stringcode, code=code, message="Girilen Şifreler Uyuşmuyor")
            else:
                cur = con.cursor()
                hashed = hasher.hash(pass1)
                cur.execute("""update "Student" set "Password"=%s where "Student_Mail"=%s""",(hashed,form_mail))
                con.commit()
                flash('Şifre Değiştirildi')
                return redirect(url_for("stu_login_page"))




def logout():
    session['is_active'] = 'nonactive'
    return redirect(url_for("home_page"))

@app.before_request
def before_request():
   
    global check
    g.user = None
    g.types = None
    g.is_admin = None
    if check == 0:
        session['is_active'] = 'nonactive'
        check = 1
    if session['is_active'] == 'active':
        user = session['user_name']
        g.user = user
        types = session['type']
        is_admin = session['admin']
        pk = session['user_pk']
        g.pk = pk
        g.types = types
        g.is_admin = is_admin
    g.is_active = session['is_active']
    

def agency_page():
    cur = con.cursor()
    cur.execute("""select * from "agency" """)
    agencies = cur.fetchall()
    return render_template("agencies.html", agencies=agencies)

    

def age_login_page():
    if request.method == "GET":
        return render_template("acelogin.html")
    else:
        i = 0
        form_mersis = request.form['mersis']
        form_password = request.form['password']
        cur = con.cursor()
        cur.execute("""select * from "agency" """)
        agencies = cur.fetchall()
        for agency in agencies:
            if agency[0] == form_mersis and hasher.verify(form_password, agency[3]):
                i = 1
                session['is_active'] = 'active'
                session['user_name'] = agency[1]
                session['user_pk'] = agency[0]
                session['type'] = 'Agency'
                session['admin'] = 'nonadmin'
                flash('Giriş Başarılı')
                return redirect(url_for("age_login_page"))
        if i == 0:
            session['is_active'] = 'nonactive'
            message = "Mersis Numarası İle Şifre Uyuşmuyor"
            return render_template("acelogin.html", message = message)       
            
def stu_login_page():
    if request.method == "GET":
        return render_template("stulogin.html")
    else:
        i = 0
        form_mail = request.form["mail"]
        form_password = request.form["password"]
        cur = con.cursor()
        cur.execute("""select * from "Student" """)
        students = cur.fetchall()
        for student in students:
            if student[0] == form_mail and hasher.verify(form_password, student[2]):
                i = 1
                session['is_active'] = 'active'
                session['user_name'] = student[1]
                session['type'] = 'Student'
                session['user_pk'] = student[0]
                if student[0] == 'yilmazy17@itu.edu.tr':
                    session['admin'] = 'admin'
                else:
                    session['admin'] = 'nonadmin'
                flash('Giriş Başarılı')
                return redirect(url_for("stu_login_page"))
                
        if i == 0:  
            session['is_active'] = 'nonactive'
            message = "Mail İle Şifre Uyuşmuyor"
            return render_template("stulogin.html", message = message)   

def request_job():
    reqjob_ıd = request.args.get('reqjob_ıd')
    reqjob_mer = request.args.get('reqjob_mer')
    cur = con.cursor()
    cur.execute("""insert into "job_request" ("Student_Mail","mersis_no","job_ıd","checks")values(%s,%s,%s,%s)""",(g.pk,reqjob_mer,reqjob_ıd,'Onay Bekliyor'))
    con.commit()
    flash('İstek Gönderildi')
    return redirect(url_for("jobs_page"))

def my_jobs_rq_page():
    reqjob1 = request.args.get('reqjob')
    reqjob = int(reqjob1)
    cur = con.cursor()
    cur.execute("""select * from "job_request" """)
    myrequests = cur.fetchall()
    cur.execute("""select * from "Student" """)
    students = cur.fetchall()
    cur.execute("""select * from "Lan_Table" """)
    languages = cur.fetchall()
    return render_template("myjobrequest.html", myrequests=myrequests, reqjob=reqjob, students=students, languages=languages)

def aprove_req():
    apreq = request.args.get('apreq')
    cur = con.cursor()
    cur.execute("""update "job_request" set "checks"='Onaylandı' where "request_ıd"=%s""",[apreq])
    con.commit()
    cur.execute("""select "job_ıd" from "job_request" where "request_ıd"=%s""",[apreq])
    reqjob = cur.fetchall()
    cur.execute("""select "number_of_students" from "job" where "job_ıd"=%s""",[reqjob[0][0]])
    number1 = cur.fetchall()
    number = number1[0][0]
    number = number-1
    number1 = str(number)
    cur.execute("""update "job" set "number_of_students"=%s where "job_ıd"=%s""",(number1,reqjob[0][0]))
    con.commit()
    flash('İstek Onaylandı')
    return redirect(url_for('my_jobs_rq_page',reqjob=reqjob[0][0]))

def deny_req():
    denreq = request.args.get('apreq')
    cur = con.cursor()
    cur.execute("""select "checks" from "job_request" where "request_ıd"=%s""",[denreq])
    checks = cur.fetchall()
    if checks[0][0] == 'Onay Bekliyor':
        cur.execute("""update "job_request" set "checks"='Reddedildi' where "request_ıd"=%s""",[denreq])
        con.commit()
        cur.execute("""select "job_ıd" from "job_request" where "request_ıd"=%s""",[denreq])
        reqjob = cur.fetchall()
        flash('İstek Reddedildi')
        return redirect(url_for('my_jobs_rq_page',reqjob=reqjob[0][0]))
    elif checks[0][0] == 'Onaylandı':
        cur.execute("""update "job_request" set "checks"='Reddedildi' where "request_ıd"=%s""",[denreq])
        con.commit()
        cur.execute("""select "job_ıd" from "job_request" where "request_ıd"=%s""",[denreq])
        reqjob = cur.fetchall()
        cur.execute("""select "number_of_students" from "job" where "job_ıd"=%s""",[reqjob[0][0]])
        number1 = cur.fetchall()
        number = number1[0][0]
        number = number+1
        number1 = str(number)
        cur.execute("""update "job" set "number_of_students"=%s where "job_ıd"=%s""",(number1,reqjob[0][0]))
        con.commit()
        flash('İstek Reddedildi')
        return redirect(url_for('my_jobs_rq_page',reqjob=reqjob[0][0]))


def my_request_page():
    cur = con.cursor()
    cur.execute("""select * from "job_request" """)
    myrequests = cur.fetchall()
    cur.execute("""select * from "job" """)
    jobs = cur.fetchall()
    cur.execute("""select * from "agency" """)
    agencies = cur.fetchall()
    return render_template("myrequest.html", myrequests=myrequests, jobs=jobs, agencies=agencies)



def my_jobs_page():
    cur = con.cursor()
    cur.execute("""select * from "job" """)
    myjobs = cur.fetchall()
    return render_template("myjobs.html", myjobs=myjobs)

def delete_req():
    delreq = request.args.get('delreq')
    cur = con.cursor()
    cur.execute("""select "checks" from "job_request" where request_ıd=%s """,[delreq])
    checks = cur.fetchall()
    cur.execute("""select "job_ıd" from "job_request" where "request_ıd"=%s """,[delreq])
    job_ıd = cur.fetchall()
    if checks[0][0] == 'Onaylandı':
        cur.execute("""delete from "job_request" where "request_ıd"=%s """,[delreq])
        con.commit()
        cur.execute("""select "number_of_students" from "job" where "job_ıd"=%s""",[job_ıd[0][0]])
        number1 = cur.fetchall()
        number = number1[0][0]
        number = number+1
        number1 = str(number)
        cur.execute("""update "job" set "number_of_students"=%s where "job_ıd"=%s""",(number1,job_ıd[0][0]))
        con.commit()
        flash('İstek Silindi')
        return redirect(url_for('my_request_page'))
    else:
        cur.execute("""delete from "job_request" where "request_ıd"=%s """,[delreq])
        con.commit()
        flash('İstek silindi')
        return redirect(url_for('my_request_page'))

    
    
def delete_job():
    deljob = request.args.get('deljob')
    cur = con.cursor()
    cur.execute("""delete from "job_request" where "job_ıd"=%s""",[deljob])
    con.commit()
    cur.execute("""delete from "job" where "job_ıd"=%s """,[deljob])
    con.commit()
    flash('İş Başarıyla silindi')
    return redirect(url_for("my_jobs_page"))

def jobs_page():
    cur = con.cursor()
    cur.execute("""select * from "job" """)
    jobs = cur.fetchall()
    cur = con.cursor()
    cur.execute("""select * from "agency" """)
    agencies = cur.fetchall()
    cur.execute("""select * from "job_request" """)
    requests = cur.fetchall()
    return render_template("jobs.html", jobs = jobs, agencies=agencies, requests=requests)

def delete_stu():
    stumail = request.args.get('stumail')
    cur = con.cursor()
    cur.execute("""delete from "Lan_Table" where "Student_Mail"=%s """,[stumail])
    con.commit()
    cur.execute("""delete from "job_request" where "Student_Mail"=%s""",[stumail])
    con.commit()
    cur.execute("""delete from "Student" where "Student_Mail"=%s """,[stumail])
    con.commit()
    return redirect(url_for("students_page"))

def delete_age():
    mersis = request.args.get('mersis')
    cur = con.cursor()
    cur.execute("""delete from "job_request" where "mersis_no"=%s""",[mersis])
    con.commit()
    cur.execute("""delete from "job" where "mersis_no"=%s""",[mersis])
    con.commit()
    cur.execute("""delete from "agency" where "mersis_no"=%s""",[mersis])
    con.commit()
    return redirect(url_for("agency_page"))

def students_page():
    cur = con.cursor()
    cur.execute("""select * from "Student" """)
    students = cur.fetchall()
    cur.execute("""select * from "Lan_Table" """)
    languages = cur.fetchall()
    return render_template("students.html", students = students, languages=languages)


app.add_url_rule("/", view_func=home_page)
app.add_url_rule("/agencies", view_func=agency_page)
app.add_url_rule("/bridge", view_func=bridge)
app.add_url_rule("/resetcode", view_func=reset_code_page, methods=["GET","POST"])
app.add_url_rule("/resetpass", view_func=reset_pass_page, methods=["GET","POST"])
app.add_url_rule("/resetpass1", view_func=reset_pass1_page, methods=["GET","POST"])
app.add_url_rule("/deletestu", view_func=delete_stu)
app.add_url_rule("/deleteage", view_func=delete_age)
app.add_url_rule("/reqjob", view_func=request_job)
app.add_url_rule("/delreq", view_func=delete_req)
app.add_url_rule("/apreq", view_func=aprove_req)
app.add_url_rule("/denreq", view_func=deny_req)
app.add_url_rule("/myjobsreq", view_func=my_jobs_rq_page)
app.add_url_rule("/myrequest", view_func=my_request_page)
app.add_url_rule("/myjobs", view_func=my_jobs_page)
app.add_url_rule("/alljobs", view_func=jobs_page)
app.add_url_rule("/jobdelete", view_func=delete_job)
app.add_url_rule("/jobpost", view_func=job_post_page, methods=["GET","POST"])
app.add_url_rule("/new_agency", view_func=age_regis_page, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/stulogin", view_func=stu_login_page, methods=["GET", "POST"])
app.add_url_rule("/agelogin", view_func=age_login_page, methods=["GET", "POST"])
app.add_url_rule("/students", view_func=students_page)
app.add_url_rule("/new_student", view_func=regis_page, methods=["GET", "POST"])
app.add_url_rule("/code", view_func=code_page, methods=["GET", "POST"])