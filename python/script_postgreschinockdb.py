from sqlalchemy import create_engine

QUARTERS = {
    1:1,2:1,3:1,
    4:2,5:2,6:2,
    7:3,8:3,9:3,
    10:4,11:5,12:4
}

"""
Rompe la fecha en partes para insertarlas en la nueva tabla
"""
def getDateItems(id, date_hour):
    return {
        'id':'{}{}{}{}'.format(date_hour.year, 
        ('{}'.format(date_hour.month)).zfill(2), 
        ('{}'.format(date_hour.day)).zfill(2), 
        ('{}'.format(id)).zfill(8)),
        'date':date_hour.date(),
        'year':date_hour.year,
        'month':date_hour.month,
        'day':date_hour.day,
        'day_name':date_hour.strftime("%A"),
        'week':date_hour.isocalendar()[1],
        'weekday':date_hour.weekday(),
        'quarter':QUARTERS[date_hour.month]
    }

def removeSpecial(text):
    return text.replace("'","") if text else ""

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/chinockdb')

with engine.connect() as db_conn:
    # TABLA DATEDIM ================
    scripts = [
        "DROP TABLE date_dim",
        "CREATE TABLE date_dim(id varchar(20) primary key, date date, year integer, month integer, day integer, dayname varchar, week integer, week_day integer, quarter integer)",
        "SELECT facturaid, facturadate from factura"
    ]

    result = None
    for script in scripts:
        try:
            if "SELECT" in script:
                result = db_conn.execute(script).fetchall()
            else:
                db_conn.execute(script)
        except:
            pass

    if result:    
        for r in result:
            id, fecha_hora = r[0], r[1]
            data = getDateItems(id, fecha_hora)

            db_conn.execute("INSERT INTO date_dim (id,date,year,month,day,dayname,week,week_day,quarter) VALUES('{}','{}',{},{},{},'{}',{},{},{})".format(
                data['id'],data['date'],data['year'],data['month'],data['day'],data['day_name'],data['week'],data['weekday'],data['quarter']
            ))

        print('<-- {} registro de fecha insertados'.format(len(result)))

    # TABLA CUSTOMER_DIM ================
    scripts2 = [
        "DROP TABLE customer_dim",
        "CREATE TABLE customer_dim(id integer primary key, first_name varchar, last_name varchar, company varchar, address varchar, city varchar, state varchar, country varchar, postal_code varchar, phone varchar, email varchar)",
        "SELECT c.nombrepila, c.apellido, c.compania, c.telefono, c.email, f.pagociudad, f.pagodireccion, f.pagoestadoprovin, f.pagopais, f.pagocodigopostal from factura as f join cliente as c on c.clienteid=f.clienteid"
    ]

    result = None
    for script in scripts2:
        try:
            if "SELECT" in script:
                result = db_conn.execute(script).fetchall()
            else:
                db_conn.execute(script)
            
        except Exception as e:
            print(e)
            pass

    if result:   
        seq = 1
        for r in result:
            nombrepila, apellido, compania, telefono, email, pagociudad, pagodireccion, pagoestadoprovin, pagopais, pagocodigopostal = r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9]

            s = 'INSERT INTO customer_dim (id,first_name,last_name,company,address,city,state,country,postal_code,phone,email) VALUES({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(
                seq, removeSpecial(nombrepila), removeSpecial(apellido), removeSpecial(compania), pagodireccion, pagociudad, pagoestadoprovin, pagopais, pagocodigopostal, telefono, email
            )

            db_conn.execute(s)

            seq += 1
            
        print('<-- {} clientes insertados con exito!'.format(seq))
