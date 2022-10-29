# Author: Guillermo Tremols Suarez
# Created: 2022-10-29

import csv

from Patient import Patient


# Checks if a string value can be stored as integers. Used on the IDs
def is_integer(n):
    try:
        int(n)
    except ValueError:
        return False
    else:
        return True


# Checks if the value for the glucose test is a valid decimal number or if it's
# in a logical range. Here I assume that a glucose test should be between 100 and 250
# (I'm not a doctor). This can still be changed if needed. For now if it is either a non-numerical
# string or an invalid number they are stored as 0. This can be changed if needed (scalable).
def validate_glu(n):
    try:
        float(n)
    except ValueError:
        return 0
    else:
        temp_value = float(n)
        if temp_value < 100 or temp_value > 250:
            return 0
        else:
            return temp_value


if __name__ == "__main__":
    patientList = []

    # List to keep track of IDs
    idList = []

    # Takes input from the user to determine where the file is
    # This makes this more scalable instead of limiting the code to a static path
    path = input("Enter the path of the file that you wish to analyze: ")
    newPath = input("Enter the path of the new file you wish to create (Please end the path with .csv. Ex: "
                    "Desktop\\report.csv): ")

    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        for row in reader:

            # If a record with an existing ID is found, the record is simply ignored and user is notified
            # This behavior can be changed to update the record if needed. But the assumption is that if
            # the same patient is in the same csv file this is most likely an error
            if row['patient_id'] in idList:
                print("Patient ", row['patient_id'], " record already exists")
                continue

            if not is_integer(row['patient_id']):
                continue

            glut1 = validate_glu(row['glucose_mg/dl_t1'])
            glut2 = validate_glu(row['glucose_mg/dl_t2'])
            glut3 = validate_glu(row['glucose_mg/dl_t3'])

            idList.append(row['patient_id'])

            # It is assumed that name, email and address are PHI but cancer and atrophy are not
            # on top of that I imagine these would help in a doctor diagnosis
            temp = Patient(row['patient_id'], glut1, glut2, glut3, row['cancerPresent'], row['atrophy_present'])

            # Here we store things in a List of patient objects. This makes the code more versatile
            # as we can do what we want with the records later
            patientList.append(temp)

        # For the sake of faster testing and to avoid random database errors
        # I decided to write the report in a csv file
        with open(newPath, 'w', newline='') as writefile:
            writer = csv.writer(writefile)
            writer.writerow(
                ['patient_id', 'glucose_mg/dl_t1', 'glucose_mg/dl_t2', 'glucose_mg/dl_t3', 'glucose_mg/dl_avg',
                 'diabetes_indicator', 'cancerPresent', 'atrophy_present'])
            for data in patientList:
                # All data from Patient object is printed since I don't believe any of it is PHI
                writer.writerow(
                    [data.patient_id, data.glucose_at1, data.glucose_at2, data.glucose_at3, data.avg, data.indicator,
                     data.cancer, data.atrophy])
