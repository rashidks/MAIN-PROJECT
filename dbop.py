import pymysql



def iud(q):
    con = pymysql.connect(host='localhost', user='root', password='', port=3306, db='virtualmedico')
    cmd = con.cursor()
    cmd.execute(q)
    id = con.insert_id()
    con.commit()
    cmd.close()
    con.close()
    return id
def iud2(q,values):
    con = pymysql.connect(host='localhost', user='root', password='', port=3306, db='virtualmedico')
    cmd = con.cursor()
    cmd.execute(q,values)
    id = con.insert_id()
    con.commit()
    cmd.close()
    con.close()
    return id
def select(q):
    con = pymysql.connect(host='localhost', user='root', password='', port=3306, db='virtualmedico')
    cmd = con.cursor()
    cmd.execute(q)
    res=cmd.fetchone()
    con.commit()
    cmd.close()
    con.close()
    return res

def selectall(q):
    con = pymysql.connect(host='localhost', user='root', password='', port=3306, db='virtualmedico')
    cmd = con.cursor()
    cmd.execute(q)
    res=cmd.fetchall()
    con.commit()
    cmd.close()
    con.close()
    return res

def selectone(q,values):
    con = pymysql.connect(host='localhost', user='root', password='', port=3306, db='virtualmedico')
    cmd = con.cursor()
    cmd.execute(q,values)
    res=cmd.fetchone()
    con.commit()
    cmd.close()
    con.close()
    return res