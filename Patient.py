# Author: Guillermo Tremols Suarez
# Created: 2022-10-29

# This function will parse the values found in the csv cancer column (they can either be 0 or 1)
# into either true or false, defaulting to false
def parse_cancer(cancer):
    if cancer.lower() in ['true', '1']:
        return True
    else:
        return False


# This function will parse the values found in the csv atrophy column (they can either be 0 or 1)
# into either true or false, defaulting to false
def parse_atrophy(atrophy):
    if atrophy.lower() in ['1', 'true']:
        return True
    else:
        return False


# Class that defines the patient object and its functions
class Patient:
    # Constructor
    def __init__(self, patient_id, glucose_at1, glucose_at2, glucose_at3, cancer, atrophy):
        self.patient_id = patient_id
        self.glucose_at1 = glucose_at1
        self.glucose_at2 = glucose_at2
        self.glucose_at3 = glucose_at3
        self.cancer = parse_cancer(cancer)
        self.atrophy = parse_atrophy(atrophy)
        # Calculates the average of the glucose tests and stores it
        self.avg = self.get_avg()
        # Converts the average glucose from a number value to a sentence/verdict of the patient's health and stores it
        self.indicator = self.parse_indicator()

    # Converts the average glucose from a number value to a sentence/verdict of the patient's health
    def parse_indicator(self):
        # Given that the patient's three tests are either invalid or not done yet, we wouldn't have enough information
        if self.avg <= 0:
            return "Not enough information or test to give a conclusion"
        elif self.avg <= 140:
            return "Normal glucose levels"
        elif self.avg <= 199:
            return "Prediabetes glucose levels"
        elif self.avg >= 200:
            return "Diabetes glucose levels"
        else:
            # Default condition in case something unexpected happens
            return "Invalid Range"

    # This function calculates the average based on how many tests the patient has. The assumption made here is that
    # a patient can have less than 3 tests and the doctors should still be able to draw a conclusion and the function
    # adapts. So, this would work for some patients who might be unable to do all tests and increases scalability since
    # it doesn't limit us to a certain number of tests

    def get_avg(self):
        total = 0.0
        glucose_counter = 0
        if self.glucose_at1 != 0:
            total += self.glucose_at1
            glucose_counter += 1
        if self.glucose_at2 != 0:
            total += self.glucose_at2
            glucose_counter += 1
        if self.glucose_at3 != 0:
            total += self.glucose_at3
            glucose_counter += 1

        # Since division by 0 is not defined this condition is necessary
        if glucose_counter != 0:
            return total/glucose_counter
        else:
            return 0

