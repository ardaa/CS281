import sqlite3
import bcrypt
import time
import asyncio

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

    def check_admin(self):
        sql = "SELECT UserNumber FROM USER WHERE UserNumber = ?"
        params = (self.__usernumber,)
        rows = self.fetch(sql, params)
        if rows[0][0] == 'A':
            return True
        else:
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
            hashed_password = bcrypt.hashpw(rows[0][1].encode('utf8'), bcrypt.gensalt())
            #bcrypt hashed password
            if bcrypt.checkpw(password.encode('utf8'), hashed_password ):
                self.__usernumber = rows[0][0]
                print(self.__usernumber)
                return self.get_account_type(rows[0][0])
            else:
                return False
            
    def get_user_type(self, username):
        sql = "SELECT User_Type FROM USER WHERE UserNumber = ?"
        params = (username,)
        rows = self.fetch(sql, params)
        return rows[0][0]
    
    def get_user_info(self, username):
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
    
    def get_account_type(self, username):
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
    
    def get_driver_info(self, username):
        sql = "SELECT * FROM USER NATURAL JOIN Driver WHERE UserNumber = ?"
        params = (username,)
        rows = self.fetch(sql, params)
        return rows[0]
    
    def set_driver_avail(self, username, avail):
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
    
    def get_cars(self, username, car_type = "All"):
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
        sql = "SELECT * FROM HasTrip WHERE LicensePlate = ?"
        params = (license_plate,)
        rows = self.fetch(sql, params)
        return rows
    
    def create_trip(self, username, selected_driver, selected_car, selected_payment, selected_start_address, selected_destination_address):
            date = time.time()
            max_value = self.fetch("SELECT COALESCE(MAX(TripNumber), 0) + 1 FROM Trip",params=())[0][0]
            maxPayment = self.fetch("SELECT COALESCE(MAX(TransactionNumber), 0) + 1 FROM Payment",params=())[0][0]
            print(max_value)
            sql = "INSERT INTO Trip (TripNumber,  DateTime,  Status)  VALUES (?, ?, ?)"
            params = (max_value, date, 'Waiting for approval')
            self.execute(sql, params)
            sql = "INSERT INTO HasTrip (TripNumber,  UserNumber,  LicensePlate)  VALUES (?, ?, ?)"
            params = (max_value, username, selected_car[0])
            self.execute(sql, params)
            sql = "INSERT INTO HasAddr (TripNumber,  StartAddrNum,  DestAddrNum)  VALUES (?, ?, ?)"
            params = (max_value, selected_start_address[0], selected_destination_address[0])
            self.execute(sql, params)
            self.conn.commit()

    def get_addresses(self):
        sql = "SELECT AddrNum, Name FROM Addr"
        params = ()
        rows = self.fetch(sql, params)
        return rows
    
    def assign_password(self, password, email):
        if self.check_admin():
            sql = "UPDATE USER SET Password = ? WHERE Email = ?"
            password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
            params = (password, email)
            self.execute(sql, params)
            return True
        else:
            return False
    
if __name__ == '__main__':
    db = Database('project.sqlite')
    print(db.assign_password('123456', 'mittromney4@yahoo.com'))