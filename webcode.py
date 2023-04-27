from flask import*
from werkzeug.utils import secure_filename
from src.myknn import prep
from src.dbop import *

import smtplib
from email.mime.text import MIMEText
# from flask_mail import Mail
#
#
#
# mail=Mail(app)
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'ihrdmcaproject2019@gmail.com'
# app.config['MAIL_PASSWORD'] = 'project@2019'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True




app=Flask(__name__)
app.secret_key="hsptl"
@app.route('/',methods=['get','post'])
def main():
    return render_template('login.html')

@app.route('/adminhome',methods=['get','post'])
def adminhome():
    return render_template('adminhome.html')
@app.route('/hospitalhome',methods=['get','post'])
def hospitalhome():
    return render_template('hospitalhome.html')
@app.route('/doctorhome',methods=['get','post'])
def doctorhome():
    return render_template('doctorhome.html')



@app.route('/login',methods=['get','post'])
def login():
    username=request.form['textfield']
    password=request.form['textfield2']
    qry="SELECT*FROM login WHERE username='"+username+"' AND PASSWORD='"+password+"'"
    res=select(qry)
    print(qry)
    print(res)
    if res is None:
        return '''<script>alert('invalid username password');window.location='/'</script>'''
    else:
        if res[3]=='admin':
            return '''<script>window.location='/adminhome'</script>'''
        elif res[3]=='hospital':
            session['lid']=str(res[0])
            return '''<script>window.location='/hospitalhome'</script>'''
        elif res[3]=='doctor':
            session['lid'] = str(res[0])

            return '''<script>window.location='/doctorhome'</script>'''
        elif res[3]=='pharmacy':
            session['lid'] = str(res[0])

            return '''<script>window.location='/pharmacyhome'</script>'''
        elif res[3]=='user':
            session['lid'] = str(res[0])

            return '''<script>window.location='/userhome'</script>'''

        else:
            return '''<script>alert('invalid username password');window.location='/userhome'</script>'''


@app.route('/viewhospital', methods=['get', 'post'])
def viewhospital():
    qry="select * from hospital"
    res=selectall(qry)
    return render_template('viewhospital.html',val=res)

@app.route('/viewnotification', methods=['get', 'post'])
def viewnotification():
    qry="select * from notification"
    res=selectall(qry)
    return render_template('viewnotification.html',val=res)


@app.route('/approvepharmacy', methods=['get', 'post'])
def approvepharmacy():
    q="SELECT `pharmacy`.* FROM `pharmacy` JOIN `login` ON `login`.`id`=`pharmacy`.`login_id`  WHERE `login`.`type`='pending'"
    res=selectall(q)
    return render_template('approvepharmacy.html',val=res)
@app.route('/approvepharmacy1', methods=['get', 'post'])
def approvepharmacy1():
    id=request.args.get('id')
    q="update login set type='pharmacy' where id="+id
    iud(q)
    return '''<script>window.location='/approvepharmacy'</script>'''
@app.route('/approvepharmacy2', methods=['get', 'post'])
def approvepharmacy2():
    id=request.args.get('id')
    q="update login set type='reject' where id="+id
    iud(q)
    return '''<script>window.location='/approvepharmacy'</script>'''



@app.route('/viewfeedback', methods=['get', 'post'])
def viewfeedback():
    qry="SELECT `feedback`.*,`user_register`.`fname` FROM `user_register` JOIN `feedback` ON `feedback`.`login_id`=`user_register`.`login_id`"
    res=selectall(qry)
    return render_template('viewfeedback.html',val=res)

@app.route('/addfeedback', methods=['get', 'post'])
def addfeedback():
    return render_template('addfeedback.html')

@app.route('/useraddfeedback', methods=['get', 'post'])
def useraddfeedback():
 feedback=request.form['textfield']
 lid=session['lid']
 q="insert into feedback values(null,'" +str(lid)+ "','"+feedback+"',curdate())"
 iud(q)
 return '''<script>alert("added");window.location="/userhome"</script>'''



# @app.route('/addfeedback1', methods=['get', 'post'])
# def addfeedback1():
#     feedback=request.form['textarea']
#     q="insert into feedback values(NULL,'"+feedback+"',curdate())"
#
#     iud(q)
#     return '''<script>alert("feedback added");window.location="/viewfeedback"</script>'''


@app.route('/managecomplaint', methods=['get', 'post'])
def managecomplaint():
    qry="SELECT `complaint`.*,`user_register`.`fname`,`user_register`.`lname`,`user_register`.`login_id` FROM`user_register` JOIN `complaint` ON `complaint`.`login_id`=`user_register`.`login_id` WHERE  `complaint`.`reply`='pending' UNION SELECT `complaint`.*,`doctor`.`fname`,`doctor`.`lname`,`doctor`.`login_id` FROM `doctor` JOIN  `complaint` ON `complaint`.`login_id`=`doctor`.`login_id` WHERE  `complaint`.`reply`='pending'"
    res=selectall(qry)
    return render_template('managecomplaint.html',val=res)

@app.route('/addhospital', methods=['get', 'post'])
def addhospital():
    return render_template('addhospital.html')
@app.route('/addhospitall', methods=['get', 'post'])
def addhospitall():
    try:
        name=request.form['textfield']
        place=request.form['textfield2']
        post=request.form['textfield3']
        pin=request.form['textfield4']
        email=request.form['textfield5']
        phone=request.form['textfield6']
        password=request.form['textfield8']
        username=request.form['textfield7']
        q="insert into login values (NUll,'"+username+ "', '"+password+ "','hospital')"
        id=iud(q)
        q="insert into hospital values(NULL,'" +str(id)+ "','" +name+ "','" +place+ "','" +post+ "','" +pin+ "','" +email+ "','" +phone+ "')"
        iud(q)
        return redirect(url_for('addhospital'))
    except Exception as e:
        return '''<script>alert("already exist");window.location="/addhospital#intro"</script>'''
@app.route('/delete_hospital', methods=['get', 'post'])
def delete_hospital():
    id=request.args.get('id')
    q="delete from hospital where login_id=%s"
    val=str(id)

    iud2(q,val)
    q = "DELETE FROM `login` WHERE `id`=%s"
    val = str(id)

    iud2(q, val)
    q="DELETE FROM  `login` WHERE `id` IN(SELECT `login_id` FROM `doctor` WHERE `hid`=%s)"
    iud2(q, val)
    q="DELETE FROM `doctor` WHERE `login_id` IN(SELECT `login_id` FROM `doctor` WHERE `hid`=%s)"
    iud2(q, val)
    return '''<script>alert("deleted");window.location="/viewhospital"</script>'''

# @app.route('/edit_hospital',methods=['get','post'])
# def edit():
#     id=request.args.get('id')
#     session['id']=id
#     q="select * from hospital where hospital_id=%s"
#     values=str(id)
#     res=selectone(q,values)
#     return render_template('edithospital.html',val=res)
# @app.route('/update_hospital',methods=['get','post'])
# def update_hospital():
#     name=request.form['textfield']
#     place=request.form['textfield2']
#     post=request.form['textfield3']
#     pin=request.form['textfield4']
#     email=request.form['textfield5']
#     phone=request.form['textfield6']
#     qry="update hospital set name='"+name+"',place='"+place+"',post='"+post+"',pin='"+pin+"',email='"+email+"',phone='"+phone+"'"
#     val=(name,place,post,pin,email,phone)
#     iud(qry)

@app.route('/addnotification', methods=['get', 'post'])
def addnotification():
    return render_template('addnotification.html')
@app.route('/addnotification1', methods=['get', 'post'])
def addnotification1():
    notification=request.form['textarea']
    q="insert into notification values(NULL,'"+notification+"',curdate())"
    iud(q)
    return redirect(url_for('viewnotification'))

@app.route('/delete_notification', methods=['get', 'post'])
def delete_notification():
    id=request.args.get('id')
    q="delete from notification where notification_id="+id
    iud(q)
    return '''<script>alert("deleted");window.location="/viewnotification"</script>'''

@app.route('/viewdoctor', methods=['get', 'post'])
def viewdoctor():

    qry="select * from doctor where hid="+session['lid']


    print(qry)
    res=selectall(qry)
    return render_template('managedoctor.html',val=res)

@app.route('/schedule', methods=['get', 'post'])
def schedule():
    lid=request.args.get('lid')
    session['did']=str(lid)
    qry="SELECT * FROM `schedule` WHERE did="+session['did']
    res=selectall(qry)
    return render_template('Schedule.html',val=res)

@app.route('/delete_schedule', methods=['get', 'post'])
def delete_schedule():
    id=request.args.get('id')
    qry = "SELECT doctor.`fname`,`doctor`.`lname`,`hospital`.`name`,`hospital`.`place`,`schedule`.`date`,`schedule`.`ftime`,`schedule`.`ttime`, `user_register`.`post` FROM `doctor` JOIN `hospital` ON `hospital`.`login_id`=`doctor`.`hid` JOIN `schedule` ON `doctor`.`login_id`=`schedule`.`did` JOIN `booking` ON `booking`.`doctor_id`=`schedule`.`id` JOIN `user_register` ON `user_register`.`login_id`=`booking`.`user_id` WHERE `booking`.`booking_id` IN (SELECT `booking_id` FROM `booking` WHERE `doctor_id`='" + id + "')"
    ss = selectall(qry)
    print(qry)

    qry="DELETE FROM `schedule` WHERE id="+id
    iud(qry)
    qry="SELECT * FROM `schedule` WHERE did="+session['did']
    res=selectall(qry)
    print(res)

    print(ss)
    for s in ss:
        email = s[7]
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('projectmailsample@gmail.com', 'issclgprojectmail')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText(
            "Your Appointment on " + str(s[4]) + " on Doctor " + s[0] + " " + s[1] + " at " + s[2] + " , " + s[3]+" is canceled ")
        print(msg)
        msg['Subject'] = 'Appointment Info'
        msg['To'] = email
        msg['From'] = 'projectmailsample@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))

    return render_template('Schedule.html',val=res)



@app.route('/addsh', methods=['get', 'post'])
def addsh():

    return render_template('addsh.html')



@app.route('/addshe1', methods=['get', 'post'])
def addshe1():
    date=request.form['date']
    ftime=request.form['ftime']
    ttime=request.form['ttime']
    qry="INSERT INTO `schedule` VALUES(NULL,'"+session['did']+"','"+date+"','"+ftime+"','"+ttime+"')"
    iud(qry)

    qry="SELECT * FROM `schedule` WHERE did="+session['did']
    res=selectall(qry)
    return render_template('Schedule.html',val=res)
@app.route('/adddoctorrr', methods=['get', 'post'])
def adddoctorrr():
    return render_template("adddoctor.html")
@app.route('/adddoctor', methods=['get', 'post'])
def adddoctor():
    try:
        fname=request.form['textfield']
        lname=request.form['textfield2']
        dob=request.form['textfield3']
        gender=request.form['radiobutton']
        qualification=request.form['textfield4']
        specialization=request.form['textfield5']
        place=request.form['textfield6']
        post=request.form['textfield7']
        pin=request.form['textfield8']
        email=request.form['textfield9']
        phone=request.form['textfield10']
        username=request.form['textfield11']
        password=request.form['textfield12']
        q = "insert into login values (NUll,'" + username + "', '" + password + "','doctor')"
        id=iud(q)
        q = "insert into doctor values(NULL,'" + str(id) + "','" + fname + "','" + lname + "','" + gender + "','" + dob + "','" + qualification + "','" + specialization + "','" + place + "','" + post + "','" + pin + "','" + email + "','" + phone + "','"+session['lid']+"')"
        iud(q)
        return '''<script>alert("Inserted");window.location="/viewdoctor"</script>'''
    except Exception as e:
        return '''<script>alert("already exist");window.location="/adddoctorrr#intro"</script>'''
@app.route('/delete_doctor', methods=['get', 'post'])
def delete_doctor():
    id=request.args.get('lid')
    q="delete from doctor where login_id=%s"
    q2="delete from login where id=%s"


    val=str(id)
    iud2(q,val)
    iud2(q2, val)

    return '''<script>alert("deleted");window.location="/viewdoctor"</script>'''
@app.route('/viewfacility', methods=['get', 'post'])
def viewfacility():
    q="select * from facility where login_id="+session['lid']

    res=selectall(q)
    return render_template('viewfacility.html',val=res)

@app.route('/viewnoti', methods=['get', 'post'])
def viewnoti():
    q="SELECT * FROM `notification`"

    res=selectall(q)
    return render_template('viewnoti.html',val=res)


@app.route('/addfacility', methods=['get', 'post'])
def addfacility():
    facility=request.form['textfield']
    description=request.form['textarea']
    lid=session['lid']
    q="insert into facility values (NULL,'" +lid+"','" +facility+ "','"+description+ "')"
    iud(q)
    return '''<script>alert("inserted");window.location="/viewfacility"</script>'''
@app.route('/addfacility1', methods=['get', 'post'])
def addfacility1():
    return render_template('addfacility.html')
@app.route('/delete_facility', methods=['get', 'post'])
def delete_facility():
    id=request.args.get('id')
    q="delete from facility where facility_id=%s"
    val=str(id)
    iud2(q,val)
    return '''<script>alert("deleted");window.location="/viewfacility"</script>'''

@app.route('/viewdepartment', methods=['get', 'post'])
def viewdepartment():
    q="select * from department where login_id="+session['lid']

    res=selectall(q)
    return render_template('viewdepartment.html',val=res)
@app.route('/adddepartment', methods=['get', 'post'])
def adddepartment():
    name=request.form['textfield']
    description=request.form['textarea']
    lid=session['lid']
    q="insert into department values (NULL,'" +lid+"','" +name+ "','"+description+ "')"
    iud(q)
    return '''<script>alert("inserted");window.location="/viewdepartment"</script>'''

@app.route('/adddepartment1', methods=['get', 'post'])
def adddepartment1():
    return render_template('adddepartment.html')

@app.route('/delete_department', methods=['get', 'post'])
def delete_department():
    id=request.args.get('id')
    q="delete from department where department_id=%s"
    val=str(id)
    iud2(q,val)
    return '''<script>alert("deleted");window.location="/viewdepartment"</script>'''

@app.route('/viewprofile', methods=['get', 'post'])
def viewprofile():
    q = "select * from doctor where `doctor`.`login_id`=%s"
    value=(str(session['lid']))
    print(q,value)
    res = selectone(q,value)
    print(res)

    return render_template('viewprofile.html', val=res)
@app.route('/editpro', methods=['get', 'post'])
def editpro():
    try:
        name=request.form['textfield']
        place=request.form['textfield2']
        post=request.form['textfield3']
        pin=request.form['textfield4']
        email=request.form['textfield5']
        phone=request.form['textfield6']
        q="update doctor set fname=%s,place=%s,post=%s,pin=%s,email=%s,phone=%s where `doctor`.`login_id`=%s"
        value=(name,place,post,pin,email,phone,str(session['lid']))
        iud2(q,value)
        return '''<script>alert("updated");window.location="/viewprofile"</script>'''
    except Exception as e:
        return '''<script>alert("already exist");window.location="/viewprofile"</script>'''


@app.route('/viewbooking', methods=['get', 'post'])
def viewbooking():
    q = "SELECT `booking`.`booking_id`,`user_register`.`fname`,`user_register`.`lname`,`user_register`.`phone`,`schedule`.`date`,`schedule`.`ftime` FROM `user_register` JOIN `booking` ON `booking`.`user_id`=`user_register`.`login_id` JOIN `schedule` ON `schedule`.`id`=`booking`.`doctor_id` WHERE `booking`.`status`='pending' AND `schedule`.`did`="+str(session['lid'])
    res = selectall(q)

    return render_template('viewbooking.html', val=res)

@app.route('/acceptbooking', methods=['get', 'post'])
def acceptbooking():
    id=request.args.get('id')
    qry="UPDATE `booking` SET `status`='accepted' WHERE `booking_id`="+id
    iud(qry)

    # Mail code==========================
    qry="SELECT doctor.`fname`,`doctor`.`lname`,`hospital`.`name`,`hospital`.`place`,`schedule`.`date`,`schedule`.`ftime`,`schedule`.`ttime`, `user_register`.`post` FROM `doctor` JOIN `hospital` ON `hospital`.`login_id`=`doctor`.`hid` JOIN `schedule` ON `doctor`.`login_id`=`schedule`.`did` JOIN `booking` ON `booking`.`doctor_id`=`schedule`.`id` JOIN `user_register` ON `user_register`.`login_id`=`booking`.`user_id` WHERE `booking`.`booking_id`="+id
    s=select(qry)
    email=s[7]
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('projectmailsample@gmail.com', 'issclgprojectmail')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("Your Appointment on "+str(s[4])+" on Doctor " + s[0]+" "+s[1]+" at "+s[2]+" , "+s[3]+" is confirmed ")
    print(msg)
    msg['Subject'] = 'Appointment Info'
    msg['To'] = email
    msg['From'] = 'projectmailsample@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))

    return '''<script>window.location="/viewbooking"</script>'''

@app.route('/finishedbooking', methods=['get', 'post'])
def finishedbooking():
    id=request.args.get('id')
    qry="UPDATE `booking` SET `status`='Finished' WHERE `booking_id`="+id
    iud(qry)
    return '''<script>window.location="/viewpatient"</script>'''


@app.route('/rejectbooking', methods=['get', 'post'])
def rejectbooking():
    id=request.args.get('id')
    qry="UPDATE `booking` SET `status`='rejected' WHERE `booking_id`="+id
    iud(qry)
    return '''<script>window.location="/viewbooking"</script>'''

@app.route('/addcomplaint', methods=['get', 'post'])
def addcomplaint():
    return render_template('addcomplaint.html')

@app.route('/addcomplaint1', methods=['get', 'post'])
def addcomplaint1():
    complaint=request.form['textarea']
    q="insert into complaint values(null,'"+str(session['lid'])+"','"+complaint+"',curdate(),'pending')"
    iud(q)

    return render_template('addcomplaint.html')



@app.route('/daddcomplaint', methods=['get', 'post'])
def daddcomplaint():
    return render_template('daddcomplaint.html')

@app.route('/daddcomplaint1', methods=['get', 'post'])
def daddcomplaint1():
    complaint=request.form['textfield']
    q="insert into complaint values(null,'"+str(session['lid'])+"','"+complaint+"',curdate(),'pending')"
    iud(q)

    return render_template('daddcomplaint.html')



@app.route('/viewreply', methods=['get', 'post'])
def viewreply():

    q = "select * from complaint where login_id="+str(session['lid'])
    res = selectall(q)
    return render_template('viewreply.html', val=res)



@app.route('/dviewreply', methods=['get', 'post'])
def dviewreply():

    q = "select * from complaint where login_id="+str(session['lid'])
    res = selectall(q)
    return render_template('dviewreply.html', val=res)



@app.route('/pharmacyregister', methods=['get', 'post'])
def pharmacy_reg():
    return render_template('pharmacyregister.html')


@app.route('/pharmacyregister1', methods=['get', 'post'])
def pharmacy_reg1():
    try:
        name=request.form['textfield']
        place = request.form['textfield2']
        post = request.form['textfield3']
        pin = request.form['textfield4']
        email= request.form['textfield5']
        phone = request.form['textfield6']
        username = request.form['textfield7']
        password = request.form['textfield8']
        q = "insert into login values (NUll,'" + username + "', '" + password + "','pending')"
        print(q)
        id = iud(q)

        q="insert into pharmacy values(NULL,'" +str(id)+ "','" +name+ "','" +place+ "','" +post+ "','" +pin+ "','" +email+ "','" +phone+ "')"
        print(q)
        iud(q)


        return '''<script>alert("registered");window.location="/pharmacyregister"</script>'''
    except Exception as e:
        return '''<script>alert("already exist");window.location="/pharmacyregister"</script>'''




@app.route('/pharmacyhome')
def pharmacyhome():
    return render_template('pharmacyhome.html')

@app.route('/pharmacy_profile', methods=['get', 'post'])

def pharmacy_profile():
    q = "select * from pharmacy where `pharmacy`.`login_id`=%s"
    value = (str(session['lid']))
    res = selectone(q, value)
    return render_template('pharmacy_profile.html', val=res)

@app.route('/pharmacy_profile1', methods=['get', 'post'])
def pharmacy_profile1():
    name=request.form['textfield']
    place = request.form['textfield2']
    post = request.form['textfield3']
    pin = request.form['textfield4']
    email= request.form['textfield5']
    phone = request.form['textfield6']
    q="update pharmacy set name='" +name+"',place='"+ place+"',post='"+post+"',pin='"+pin+"',email='"+email+"',phone='"+phone+"' where `pharmacy`.`login_id`=%s"
    value=(str(session['lid']))
    iud2(q,value)
    return '''<script>alert("updated");window.location="/pharmacyhome"</script>'''
@app.route('/pharmacy_add_location', methods=['get', 'post'])
def pharmacy_add_location():
    return render_template('addlocation.html')


@app.route('/pharmacy_add_locationn', methods=['get', 'post'])
def pharmacy_add_locationn():
    lattitude = request.form['textfield']
    longitude = request.form['textfield2']
    place = request.form['textfield3']
    q="insert into location values(NULL,'" +str(id)+ "','" +lattitude+ "','" +longitude+ "','" +place+ "')"
    iud(q)

    return '''<script>alert("added");window.location="/pharmacyhome"</script>'''

@app.route('/addmedicine', methods=['get', 'post'])
def addmedicine():
    return render_template('addmedicine.html')
@app.route('/addmedicine1', methods=['get', 'post'])
def addmedicine1():
    medicinename=request.form['textfield']
    description = request.form['textarea']
    file= request.files['file']
    price= request.form['textfield3']
    expdate = request.form['textfield4']
    dosage = request.form['textfield5']
    fname=secure_filename(file.filename)
    file.save('static/img/'+fname)

    q="insert into medicine values(NULL,"+session['lid']+",'"+medicinename+"','"+description+"','"+fname+"','"+price+"','"+expdate+"','"+dosage+"')"
    iud(q)

    return '''<script>alert("added");window.location="/pharmacyhome"</script>'''
@app.route('/viewmedicine', methods=['get', 'post'])
def viewmedicine():

    qry="select * from medicine where `pharmacy_id`="+str(session['lid'])
    res=selectall(qry)
    return render_template('viewmedicine.html',val=res)
@app.route('/delete_medicine', methods=['get', 'post'])
def delete_medicine():
    id=request.args.get('id')
    q="delete from medicine where medicine_id=%s"
    val=str(id)
    iud2(q,val)
    return '''<script>alert("deleted");window.location="/viewmedicine"</script>'''
@app.route('/manage_complaint', methods=['get', 'post'])
def manage_complaint():
    id=request.args.get('cid')
    session['cid']=id
    return render_template('sendreply.html')
@app.route('/upcomplaint', methods=['get', 'post'])
def upcomplaint():
   sendreply=request.form['textarea']
   q="update complaint set reply='"+sendreply+"' where complaint_id='"+str(session['cid'])+"'"

   iud(q)
   return '''<script>alert("sent");window.location="/managecomplaint"</script>'''

@app.route('/userhome',methods=['get','post'])
def userhome():
    return render_template('userhome.html')

@app.route('/viewdoctors',methods=['get','post'])
def viewdoctors():
    qry = "SELECT `doctor`.`login_id`,doctor.`fname`,`doctor`.`lname`,`doctor`.`specialization`,`hospital`.`name`,`hospital`.`place`,`hospital`.`phone_no` FROM `doctor` JOIN `hospital` ON `hospital`.`login_id`=`doctor`.`hid`"
    res = selectall(qry)
    return render_template('viewdoctor.html', val=res)

@app.route('/bookdoctor1',methods=['get','post'])
def bookdoctor1():
    id = request.args.get('id')
    q="insert into booking values(null,'"+str(id)+"','"+str(session['lid'])+"',curdate(),'pending')"
    iud(q)
    return '''<script>alert("booked");window.location="/viewdoctors"</script>'''

@app.route('/bookdoctor',methods=['get','post'])
def bookdoctor():
    id = request.args.get('id')
    q="SELECT * FROM `schedule` WHERE `date`>=curdate() and `did`="+id
    res = selectall(q)
    return render_template('bookdoc.html', val=res)

@app.route('/viewbooking_status',methods=['get','post'])
def viewbooking_status():
    q="SELECT `doctor`.`login_id`,doctor.`fname`,`doctor`.`lname`,`doctor`.`specialization`,`hospital`.`name`,`hospital`.`place`,`hospital`.`phone_no`,`booking`.`booking_id`,`booking`.`status`,`schedule`.`date`,`schedule`.`ftime`,`schedule`.`ttime` FROM `doctor` JOIN `hospital` ON `hospital`.`login_id`=`doctor`.`hid` JOIN `schedule` ON `doctor`.`login_id`=`schedule`.`did` JOIN `booking` ON `booking`.`doctor_id`=`schedule`.`id` WHERE `booking`.`user_id`='"+session['lid']+"'"
    res = selectall(q)
    return render_template('viewbookingstatus.html',val=res)

# @app.route('/viewbooking_status1',methods=['get','post'])
# def viewbooking_status1():
@app.route('/usercomplaint',methods=['get','post'])
def usercomplaint():
    return render_template('addcomplaint.html')
@app.route('/addcomplaintttt',methods=['get','post'])
def addcomplaintttt():
    complaint=request.form['textfield']
    qry="insert into complaint values(null,'"+str(session['lid'])+"','"+complaint+"',curdate(),'pending')"
    iud(qry)
    return'''<script>alert("added");window.location="/userhome"</script>'''


@app.route('/nearestpharmacy')
def nearestpharmacy():
    q="SELECT DISTINCT place,`pharmacy_id` FROM pharmacy"
    val=selectall(q)
    return render_template("nearestpharmacy.html",res=val)

@app.route('/msearch1',methods=['get','post'])
def msearch1():

    return render_template('user searchmedicine.html',val=[],mm='')


@app.route('/msearch',methods=['get','post'])
def msearch():
    m=request.form['textfield']
    q="SELECT DISTINCT `name`,`place`,`phone` FROM `pharmacy` WHERE `login_id` IN(SELECT `pharmacy_id` FROM `medicine` WHERE `medicine_name`='"+m+"')"
    s=selectall(q)
    return render_template('user searchmedicine.html',val=s,mm=m)
@app.route('/searchpharmacy',methods=['get','post'])
def searchpharmacy():
    place=request.form['select']
    print(place)
    q="SELECT NAME,phone FROM pharmacy WHERE `pharmacy`.`place`='"+place+"'"
    val = selectall(q)
    print(val)
    q1 = "SELECT DISTINCT place,`pharmacy_id` FROM pharmacy"
    vals = selectall(q1)
    return render_template("nearestpharmacy.html",values=val,res=vals)

@app.route('/user_facility', methods=['get', 'post'])
def user_facility():
    q="SELECT facility.*,`hospital`.* FROM facility JOIN `hospital` ON `hospital`.`login_id`=`facility`.`login_id`"

    res=selectall(q)
    return render_template('user_facility.html',val=res)

@app.route('/viewpatient', methods=['get', 'post'])
def viewpatient():
    q = "SELECT `booking`.`booking_id`,`user_register`.`fname`,`user_register`.`lname`,`user_register`.`phone`,`schedule`.`date`,`schedule`.`ftime` FROM `user_register` JOIN `booking` ON `booking`.`user_id`=`user_register`.`login_id` JOIN `schedule` ON `schedule`.`id`=`booking`.`doctor_id` WHERE `booking`.`status`='accepted' AND `schedule`.`date`=curdate() and `schedule`.`did`=" + str(session['lid'])
    res = selectall(q)
    return render_template('viewpatient.html',val=res)

@app.route('/prediction', methods=['get', 'post'])
def prediction():

   return render_template('prediction1.html')


@app.route('/prediction1', methods=['get', 'post'])
def prediction1():
    img=request.files['file']
    fn=secure_filename(img.filename)
    img.save("static/imgs/"+fn)
    res=prep("static/imgs/"+fn)
    return render_template('prediction.html',imgg="../static/imgs/"+fn,r=res)

@app.route('/userreg',methods=['get','post'])
def userreg():
    return render_template('register.html')
@app.route('/userregg',methods=['get','post'])
def userregg():
    try:
        fname=request.form['textfield']
        lname = request.form['textfield2']
        dob = request.form['textfield3']
        place = request.form['textfield4']
        post = request.form['textfield5']
        phone = request.form['textfield6']
        gender=request.form['radiobutton']
        username=request.form['textfield7']
        password= request.form['textfield8']
        pin=request.form['pin']
        q = "insert into login values (NUll,'" + username + "', '" + password + "','user')"
        print(q)
        id = iud(q)

        qry="insert into user_register  values(null,'"+str(id)+"','"+fname+"','"+lname+"','"+gender+"','"+dob+"','"+place+"','"+post+"','"+pin+"','"+phone+"')"
        iud(qry)
        print(q)


        return'''<script>alert("added");window.location="/"</script>'''
    except Exception as e:
        return '''<script>alert("already exist");window.location="/"</script>'''

# if __name__=="__main_":
app.run(debug=True)

