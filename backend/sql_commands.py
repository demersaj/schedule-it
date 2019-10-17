#Make sure foreign keys are turned on.
useForeignKeys = "PRAGMA foreign_keys=ON;"

#Create the student table.
createStudentTable = "CREATE TABLE IF NOT EXISTS Student(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ONID      TEXT UNIQUE NOT NULL,
    FName     TEXT        NOT NULL,
    LName     TEXT        NOT NULL,
    Phone     TEXT        NOT NULL
);"

#Create the slot table.
createSlotTable = "CREATE TABLE IF NOT EXISTS Slot(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time  TEXT NOT NULL,
    end_time    TEXT NOT NULL,
    location    TEXT NOT NULL,
    numPeople   INTEGER NOT NULL,
    limitPeople INTEGER NOT NULL
);"

#Create the file table.
createFileTable = "CREATE TABLE IF NOT EXISTS File(
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    studentID       INTEGER,
    reservationID   INTEGER,
    filename        TEXT    NOT NULL,
    dateUploaded    INTEGER NOT NULL,
    filepath        TEXT    NOT NULL,
    FOREIGN KEY(studentID) REFERENCES Student(id) ON DELETE CASCADE,
    FOREIGN KEY(reservationID) REFERENCES Reservation(id) ON DELETE CASCADE
);"

#Create the reservation table.
createReservationTable = "CREATE TABLE IF NOT EXISTS Reservation(
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    studentID     INTEGER,
    slotID        INTEGER,
    UNIQUE(studentID,slotID),
    FOREIGN KEY(studentID) REFERENCES Student(id) ON DELETE CASCADE,
    FOREIGN KEY(slotID)    REFERENCES Slot(id)    ON DELETE CASCADE
);"

#Insert a row in the student table.
insertStudent = "INSERT INTO Student(ONID,FName,LName,Phone) Values(?,?,?);"

#Insert a row in the slot table.
insertSlot    = "INSERT INTO Slot(start_time, end_time, location, numPeople, limitPeople) Values(?,?,?,?,?);"

#Insert a row in the file table.
insertFile    = "INSERT INTO File(studentID,reservationID,filename,filepath,dateUploaded) Values(?,?,?,?,?);"

#Insert a row in the reservation table.
insertReservation = "INSERT INTO Reservation(studentID,slotID) VALUES(?,?);"

#Delete a row in the student table by id.
deleteStudent = "DELETE FROM Student WHERE id = ?;"

#Delete a row in the student table by ONID.
deleteStudent = "DELETE FROM Student WHERE ONID = ?;"

#Delete a row in the slot table.
deleteSlot    = "DELETE FROM Slot WHERE id = ?;"

#Delete a row in the file table by id.
deleteFileByID    = "DELETE FROM File WHERE id = ?;"

#Delete a row in the reservation table by id.
deleteReservation = "DELETE FROM Reservation WHERE id = ?;"

#create a trigger to stop a reservation being inserted when there aren't enough spots.
beforeInsertReservationTrigger = "CREATE TRIGGER IF NOT EXISTS beforeInsertReservationT
                                    BEFORE INSERT
                                    ON Reservation
                                    BEGIN
                                        SELECT CASE WHEN limitPeople <= numPeople THEN RAISE(ABORT,"The slot is not open.") END FROM Slot WHERE id = NEW.SlotID;
                                    END;"

#create a trigger to increment numPeople in Slot any time a reservation row is added for that slot.
afterInsertReservationTrigger = "CREATE TRIGGER IF NOT EXISTS afterInsertReservation
                                    AFTER INSERT
                                    ON Reservation
                                    BEGIN
                                        UPDATE Slot Set numPeople = numPeople + 1 WHERE id = NEW.slotID;
                                    END;"

#create a trigger to decrement numPeople in Slot any time a reservation row is removed.
afterDeleteReservationTrigger = "CREATE TRIGGER IF NOT EXISTS deleteReservation
                                    AFTER DELETE
                                    ON Reservation
                                    BEGIN
                                        UPDATE Slot Set numPeople = numPeople - 1 WHERE id = OLD.slotID;
                                    END;"

#Get all reservations by a student.
reservationsByStudentID = "SELECT * FROM Reservations WHERE StudentID = ?;"

#Get all reservations by a slot.
reservationsBySlotID = "SELECT * FROM Reservations WHERE SlotID = ?;"
