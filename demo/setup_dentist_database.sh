docker run --name dentist_database -d -e POSTGRES_USER=valentin -e POSTGRES_PASSWORD=password -p 5433:5432 postgres
sleep 2
docker exec -it dentist_database psql -U valentin -c "CREATE TABLE Patients (ID INT PRIMARY KEY, Name VARCHAR(50), Email VARCHAR(50), Phone VARCHAR(15));"
docker exec -it dentist_database psql -U valentin -c "CREATE TABLE Dentists (ID INT PRIMARY KEY, Name VARCHAR(50), Specialty VARCHAR(50), Clinic VARCHAR(50));"
docker exec -it dentist_database psql -U valentin -c "CREATE TABLE Appointments (ID INT PRIMARY KEY,PatientID INT,DentistID INT,AppointmentDate DATE,AppointmentTime TIME,FOREIGN KEY (PatientID) REFERENCES Patients(ID),FOREIGN KEY (DentistID) REFERENCES Dentists(ID));"

docker exec -it dentist_database psql -U valentin -c "INSERT INTO Patients (ID, Name, Email, Phone) VALUES  (1, 'John Smith', 'john.smith@example.com', '123-456-7890'),  (2, 'Emma Johnson', 'emma.johnson@example.com', '987-654-3210'),  (3, 'Michael Brown', 'michael.brown@example.com', '456-123-7890');"
docker exec -it dentist_database psql -U valentin -c "INSERT INTO Dentists (ID, Name, Specialty, Clinic) VALUES  (1, 'Dr. Roberts', 'Orthodontics', 'ABC Dental'),  (2, 'Dr. Anderson', 'Endodontics', 'XYZ Dental'),  (3, 'Dr. Lee', 'Periodontics', 'PQR Dental');"
docker exec -it dentist_database psql -U valentin -c "INSERT INTO Appointments (ID, PatientID, DentistID, AppointmentDate, AppointmentTime) VALUES  (1, 1, 2, '2023-06-25', '10:00:00'),  (2, 2, 1, '2023-06-26', '11:30:00'),  (3, 3, 3, '2023-06-27', '14:15:00');"

docker exec -it dentist_database psql -U valentin -c "SHOW TABLES;"