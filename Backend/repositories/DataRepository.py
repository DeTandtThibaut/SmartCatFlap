from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_status_lampen():
        sql = "SELECT * from lampen"
        return Database.get_rows(sql)

    @staticmethod
    def read_status_lamp_by_id(id):
        sql = "SELECT * from lampen WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_status_lamp(id, status):
        sql = "UPDATE lampen SET status = %s WHERE id = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_status_alle_lampen(status):
        sql = "UPDATE lampen SET status = %s"
        params = [status]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_dht11():
        sql = "SELECT * from SensorData LIMIT 100"
        return Database.get_rows(sql)

    @staticmethod
    def read_SensorData(MeetEenheid):
        sql = "SELECT * FROM SensorData WHERE MeetEenheid = %s ORDER BY Tijd DESC LIMIT 100"
        params = [MeetEenheid]
        return Database.get_rows(sql, params)

    @staticmethod
    def get_latest_SensorData(MeetEenheid):
        sql = "SELECT * FROM SensorData WHERE MeetEenheid = %s ORDER BY Tijd DESC LIMIT 1"
        params = [MeetEenheid]
        return Database.get_rows(sql, params)

    

    @staticmethod
    def insert_sensorData(MeetEenheid, Meting):
        print("Data to insert")
        print(MeetEenheid)
        print(Meting)
       
        print("-----")
        sql = "Insert INTO SensorData(MeetEenheid, Meting, Tijd) values (%s,%s, NOW())"
        params = [MeetEenheid, Meting]
        return Database.execute_sql(sql, params)

    @staticmethod
    def insert_rfid(TagUID, PoesNaam):
        print("Data to insert")
        print(TagUID)
        print(PoesNaam)
        
        print("-----")
        sql = "Insert INTO RfidData(TagUID, PoesNaam, Tijd) values (%s,%s, NOW())"
        params = [TagUID, PoesNaam]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def update_rfid(knop):
        sql = "UPDATE RfidData SET knop = %s ORDER BY Tijd DESC LIMIT 1"
        params = [knop]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_luna():
        sql = "SELECT * FROM RfidData WHERE PoesNaam = %s LIMIT 30"
        params = ["Luna"]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_mona():
        sql = "SELECT * FROM RfidData WHERE PoesNaam = %s LIMIT 30"
        params = ["Mona"]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_recent_mona():
        sql = "SELECT * FROM RfidData WHERE PoesNaam = %s ORDER BY Tijd DESC LIMIT 1"
        params = ["Mona"]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_recent_luna():
        sql = "SELECT * FROM RfidData WHERE PoesNaam = %s ORDER BY Tijd DESC LIMIT 1"
        params = ["Luna"]
        return Database.get_rows(sql, params)

    @staticmethod
    def insert_actuator(Naam, Toestand):
        print("Data to insert")
        print(Naam)
        print(Toestand)
        
        print("-----")
        sql = "Insert INTO ActuatorData(Naam, Toestand, Tijd) values (%s,%s, NOW())"
        params = [Naam, Toestand]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_toestand_motor(toestand,naam):
        print(f'Toestand: {toestand}')
        print(f'Naam: {naam}')
        sql = "UPDATE ActuatorData SET Toestand = %s, Tijd = NOW() WHERE Naam = %s"
        params = [toestand, naam]
        return Database.execute_sql(sql, params)


    

    @staticmethod
    def read_toestand_motor(naam):
        sql = "SELECT Toestand from ActuatorData WHERE Naam = %s"
        params = [naam]
        return Database.get_one_row(sql, params)
