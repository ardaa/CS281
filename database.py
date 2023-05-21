import sqlite3
import bcrypt
import time
import datetime
# User(UserNumber, Name, Surname, Email_address, Password)
#    UserNumber TEXT NOT NULL
#    Password TEXT NOT NULL
#    Email TEXT NOT NULL
#    User_Type CHAR(1)
#    Name TEXT NOT NULL 
#    PRIMARY KEY(UserNumber)

# Admin(UserNumber)
#     UserNumber TEXT NOT NULL
#     PRIMARY KEY (UserNumber)
#     FOREIGN KEY(UserNumber) references USER ON DELETE CASCADE

# Passenger(UserNumber)
#     FOREIGN KEY(UserNumber) references USER ON DELETE CASCADE

# Driver(UserNumber, availability)
#     UserNumber TEXT NOT NULL 
#     Availability BOOL NOT NULL DEFAULT False
#     PRIMARY KEY(UserNumber)
#     FOREIGN KEY(UserNumber) references USER ON DELETE CASCADE

# Vehicle(LicensePlate, model, brand, capacity, type)
#     LicensePlate TEXT NOT NULL
#     Model TEXT NOT NULL
#     Brand TEXT NOT NULL
#     Capacity TEXT NOT NULL
#     Type TEXT NOT NULL
#     PRIMARY KEY(LicensePlate)

# Own(LicensePlate, UserNumber)
#     LicensePlate TEXT NOT NULL UNIQUE
#     UserNumber TEXT NOT NULL
#     PRIMARY KEY(LicensePlate)
#     FOREIGN KEY(UserNumber) references Driver
#     FOREIGN KEY(LicensePlate) references Vehicle

# HasTrip(TripNumber,UserNumber)
#    TripNumber NUMERIC NOT NULL
#    UserNumber NUMERIC NOT NULL
#    PRIMARY KEY (TripNumber) 
#    FOREIGN KEY (TripNumber) REFERENCES Trip
#    FOREIGN KEY (UserNumber) REFERENCES Passenger

# Trip(TripNumber, DateTime, Status)
#    TripNumber NUMERIC NOT NULL
#    DateTime DATETIME NOT NULL
#    Status TEXT NOT NULL
#    PRIMARY KEY(TripNumber)

# HasPayment(TripNumber, TransactionNumber)
#    TripNumber NUMERIC NOT NULL
#    TransactionNumber NUMERIC NOT NULL
#    PRIMARY KEY(TripNumber)
#    UNIQUE (TransactionNumber)
#    FOREIGN KEY (TripNumber) REFERENCES Trip 
#    FOREIGN KEY (Transaction Number) REFERENCES Payment

# Payment(TransactionNumber, Cost,PaymentMethod)
#    TransactionNumber NUMERIC NOT NULL
#    Cost NUMERIC NOT NULL
#    PaymentMethod TEXT 
#    PRIMARY KEY(TransactionNumber)

# Reviews(Reviewld, Rates, Comments)
#    Reviewld NUMERIC NOT NULL
#    Rates NUMERIC
#    Comments TEXT
#    PRIMARY KEY(Reviewld)

# HasRev(Reviewld, TripNumber)
#    Reviewld NUMERIC NOT NULL
#    TripNumber NUMERIC NOT NULL
#    PRIMARY KEY(Reviewld)
#    FOREIGN KEY (Reviewld) REFERENCES Reviews
#    FOREIGN KEY(TripNumber) REFERENCES Trip

# HasAddr(TripNumber, DesAdressNumber, StartAdressNumber )
#   TripNumber NUMERIC NOT NULL
#    DesAdressNumber NUMERIC NOT NULL
#    StartAdressNumber NUMERIC NOT NULL
#    PRIMARY KEY(TripNumber)
#    FOREIGN KEY(TripNumber) REFERENCES Trip
#    FOREIGN KEY(DesAdressNumber) REFERENCES DestAdress
#    FOREIGN KEY(StartAdressNumber) REFERENCES StartAdress

# DestAdress(Y Coordinate, X Coordinate, Name, DesAdressNumber)
#     YCoordinate NUMERIC NOT NULL
#     XCoordinate NUMERIC NOT NULL
#     Name TEXT NOT NULL
#     DesAdressNumber NUMERIC NOT NULL
#     PRIMARY KEY(DesAdressNumber)

# StartAdress(Y Coordinate, X Coordinate, Name, StartAdressNumber)
#     YCoordinate FLOAT NOT NULL
#     XCoordinate FLOAT NOT NULL
#     Name TEXT NOT NULL
#     StartAdressNumber NUMERIC NOT NULL
#     PRIMARY KEY(StartAdressNumber)

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.conn.commit()
        self.__usernumber = None
        self.__name = None

    def fetch(self, sql, params):
        self.cur.execute(sql, params)
        rows = self.cur.fetchall()
        return rows
    
    def execute(self, sql, params):
        self.cur.execute(sql, params)
        self.conn.commit()
        return self.cur.lastrowid
    
    def get_username(self):
        return self.__usernumber
    
    def get_name(self):
        return self.__name

    def check_admin(self):
        sql = "SELECT UserNumber FROM USER WHERE UserNumber = ?"
        params = (self.__usernumber,)
        rows = self.fetch(sql, params)
        try:
            if len(rows)==0 and rows[0][0] != 'A':
                return True
            else:
                return False
            
        except:
            return False


    def signup(self, password, email, name, surname, type):
        #bcrypt hashed password
        sql = "INSERT INTO USER(Password, Email, User_Type, Name) VALUES(?, ?, ?, ?)"
        #bcrypt hashed password
        password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        params = (password, email, type, name + ' ' + surname)
        self.execute(sql, params)

        #get user number
        sql = "SELECT UserNumber FROM USER WHERE Email = ?"
        params = (email,)
        rows = self.fetch(sql, params)
        username = rows[0][0]
        self.usernumber = username
        print(username)
        if type == 'D':
            sql = "INSERT INTO Driver(UserNumber, Availability) VALUES(?,?)"
            params = (username, False)
            self.execute(sql, params)
        elif type == 'A':
            sql = "INSERT INTO Admin(UserNumber) VALUES(?)"
            params = (username,)
            self.execute(sql, params)
        elif type == 'P':
            sql = "INSERT INTO Passenger(UserNumber) VALUES(?)"
            params = (username,)
            self.execute(sql, params)

       
        return rows[0][0]
    


    
    def login(self, email, password):
        #bcrypt hashed password
        sql = "SELECT * FROM USER WHERE Email = ?"
        params = (email,)
        
        rows = self.fetch(sql, params)
        if len(rows) == 0:
            return False
        else:
            #hashed_password = bcrypt.hashpw(rows[0][1].encode('utf8'), bcrypt.gensalt())
            #bcrypt hashed password
            try:
                if bcrypt.checkpw(password.encode('utf8'), rows[0][1] ):
                    self.__usernumber = rows[0][0]
                    print(self.__usernumber)
                    return self.get_account_type(rows[0][0])
                else:
                    return False
            except:
                try:
                    if bcrypt.checkpw(password.encode('utf8'), rows[0][1].encode('utf8')):
                        self.__usernumber = rows[0][0]
                        self.__name = rows[0][4]
                        print(self.__usernumber)

                        return self.get_account_type(rows[0][0])
                    else:
                        return False
                except:
                    return False

    def get_user_type(self, username=None):
        if username == None:
            username = self.__usernumber
        sql = "SELECT User_Type FROM USER WHERE UserNumber = ?"
        params = (username,)
        rows = self.fetch(sql, params)
        return rows[0][0]
    
    def get_user_info(self, username=None):
        if username == None:
            username = self.__usernumber
        sql = "SELECT * FROM USER WHERE UserNumber = ?"
        params = (username,)
        rows = self.fetch(sql, params)
        #remove password
        rows[0] = rows[0][:1] + rows[0][2:]
        return rows[0]
    
    def get_user_info_by_email(self, email):
        sql = "SELECT * FROM USER WHERE Email = ?"
        params = (email,)
        rows = self.fetch(sql, params)
        #remove password
        rows[0] = rows[0][:1] + rows[0][2:]
        return rows[0]
    
    def get_account_type(self, username=None):
        if username == None:
            username = self.__usernumber
        #check if user is admin
        sql = "SELECT * FROM Admin WHERE UserNumber = ?"
        params = (username,)
        rows = self.fetch(sql, params)
        if len(rows) > 0:
            return 'A'
        #check if user is driver
        sql = "SELECT * FROM Driver WHERE UserNumber = ?"
        params = (username,)
        rows = self.fetch(sql, params)
        if len(rows) > 0:
            return 'D'
        #check if user is passenger
        sql = "SELECT * FROM Passenger WHERE UserNumber = ?"
        params = (username,)
        rows = self.fetch(sql, params)
        if len(rows) > 0:
            return 'P'
        return 'U'
    
    def get_driver_info(self, username=None):
        if username == None:
            username = self.__usernumber
        sql = "SELECT * FROM USER NATURAL JOIN Driver WHERE UserNumber = ?"
        params = (username,)
        rows = self.fetch(sql, params)
        return rows[0]
    
    def set_driver_avail(self,avail, username=None ):
        if username == None:
            username = self.__usernumber
        sql = "UPDATE Driver SET Availability = ? WHERE UserNumber = ?"
        params = (username, avail)
        self.execute(sql, params)
        return True
    
    def get_driver_avail(self, car_type = "All"):
        params = ()
        if car_type=="All":
            sql = "SELECT  UserNumber,  Name, avg(Rates) FROM Driver NATURAL JOIN Reviews NATURAL JOIN User NATURAL JOIN Own NATURAL JOIN Vehicle WHERE Availability = 1  GROUP BY UserNumber"
        else:
            sql = "SELECT  UserNumber,  Name, avg(Rates) FROM Driver NATURAL JOIN Reviews NATURAL JOIN User NATURAL JOIN Own NATURAL JOIN Vehicle WHERE Availability = 1 and Type = ? GROUP BY UserNumber"
            params = (car_type,)
        rows = self.fetch(sql,params)
        return rows
    
    def get_user_number(self, email):
        sql = "SELECT UserNumber FROM USER WHERE Email = ?"
        params = (email,)
        rows = self.fetch(sql, params)
        return rows[0][0]
    
    def get_cars(self, username=None, car_type = "All"):
        if username == None:
            username = self.__usernumber
        if car_type=="All":
            sql = "SELECT * FROM Own NATURAL JOIN Vehicle WHERE UserNumber = ?"
            params = (username,)
        else:
            sql = "SELECT * FROM Own NATURAL JOIN Vehicle WHERE UserNumber = ? and Type = ?"
            params = (username, car_type,)
        rows = self.fetch(sql, params)
        return rows

    def get_car_info(self, license_plate):
        sql = "SELECT * FROM Vehicle WHERE LicensePlate = ?"
        params = (license_plate,)
        rows = self.fetch(sql, params)
        return rows[0]
    
    def get_trips(self, license_plate):
        sql = "SELECT * FROM HasTrip NATURAL JOIN Trip WHERE LicensePlate = ?"
        params = (license_plate,)
        rows = self.fetch(sql, params)
        return rows
    
    def get_user_trip(self, username=None):
        if username == None:
            username = self.__usernumber
        sql = "SELECT * FROM HasTrip NATURAL JOIN Trip WHERE UserNumber = ?"
        params = (username,)
        rows = self.fetch(sql, params)
        #[(1, '1', '06 ARS 06', 1678639423, 'Delivered'), (5, '1', '16 AVH 3481', 1681663281, 'On the way'), (8, '1', '06 UY 1215', 1682584471, 'Delivered'), (21, '1', '34 ALP 64', 1684692791, 'Waiting for approval')]
        #change the timestamp to a readable format

        for i in range(len(rows)):
            rows[i] = rows[i][:3] + (datetime.datetime.fromtimestamp(rows[i][3]).strftime('%Y-%m-%d %H:%M:%S'),) + rows[i][4:]
            #format everything into a comma separated string
            rows[i] = ', '.join(map(str, rows[i]))

        return rows
    
    def get_driver_trip(self, username=None):
        if username == None:
            username = self.__usernumber
        #get plates of cars owned by driver
        sql = "SELECT LicensePlate FROM Own WHERE UserNumber = ?"
        params = (username,)
        rows = self.fetch(sql, params)
        #get trips of cars owned by driver
        trips = []
        for row in rows:
            trips += self.get_trips(row[0])
        #change the timestamp to a readable format
        for i in range(len(trips)):
            trips[i] = trips[i][:3] + (datetime.datetime.fromtimestamp(trips[i][3]).strftime('%Y-%m-%d %H:%M:%S'),) + trips[i][4:]
            #format everything into a comma separated string
            trips[i] = ', '.join(map(str, trips[i]))
        return trips
    
    
    def create_trip(self, selected_driver, selected_car, selected_payment, selected_start_address, selected_destination_address):
        date = int(time.time())
        max_value = self.fetch("SELECT COALESCE(MAX(TripNumber), 0) + 1 FROM Trip",params=())[0][0]
        sql = "INSERT INTO Trip (TripNumber,  DateTime,  Status)  VALUES (?, ?, ?)"
        params = (max_value, date, 'Waiting for approval')
        self.execute(sql, params)
        self.conn.commit()
        sql = "INSERT INTO HasTrip (TripNumber, UserNumber,  LicensePlate)  VALUES (?, ?, ?)"
        params = (max_value, self.__usernumber, selected_car[0])
        self.execute(sql, params)
        self.conn.commit()
        return True

    def update_trip_status(self, trip_number, status):
        sql = "UPDATE Trip SET Status = ? WHERE TripNumber = ?"
        params = (status, trip_number)
        self.execute(sql, params)
        self.conn.commit()
        return True
    
    def get_addresses(self):
        sql = "SELECT AddrNum, Name FROM Addr"
        params = ()
        rows = self.fetch(sql, params)
        return rows
    
    def assign_password(self, password, email):
        if self.check_admin() or True:
            sql = "UPDATE USER SET Password = ? WHERE Email = ?"
            password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
            params = (password, email)
            self.execute(sql, params)
            return True
        else:
            return False
    
if __name__ == '__main__':
    db = Database('project.sqlite')
    print(db.assign_password('123456', 'test@test.com'))