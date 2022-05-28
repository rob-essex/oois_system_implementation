
class Patient:
    """Creates a Patient object with a patient's name, address, phone number."""
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def request_repeat(self, prescription):
        """Accepts a Prescription object as an argument, verifies it belongs to Patient, and sends for repeat."""
        if prescription.patient == self.name:
            # Print operation serves as a placeholder since surgery request business process is unknown.
            print("Sending repeat prescription request of ", prescription.prescription_type, " to ",
                  prescription.doctor, ".")
        else:
            print("This prescription does not belong to this patient.")

    def request_appointment(self, appointment_type, appointment_staff):
        """Generates a request message from the Patient with specified appointment type and staff."""
        # Print operation serves as a placeholder since surgery request business process is unknown.
        print(self.name, "requests a(n) ", appointment_type, "appointment with ", appointment_staff.name, ".")


class HealthcareProfessional:
    """Creates a Healthcare Professional object with a name and employee number."""
    def __init__(self, name, employee_number):
        self.name = name
        self.employee_number = employee_number

    def consultation(self, appointment):
        """Confirms that a Healthcare Professional class conducted a specified Appointment object."""
        # Print operation serves as a placeholder since consultation business process is unknown.
        print(self.name, " conducted the consultation for ", appointment.patient, "'s ", appointment.appointment_type,
              "appointment.")


class Doctor(HealthcareProfessional):
    """Creates a Doctor object, inherits from Healthcare Professional class."""
    def __init__(self, name, employee_number):
        super().__init__(name, employee_number)  # Required to add another init attribute to Doctor subclass
        self.registered_patient_list = []

    def issue_prescription(self, patient, prescription_type, quantity, dosage):
        """Returns a new Prescription object."""
        new_prescription_type = prescription_type
        new_patient = patient
        new_doctor = self
        new_quantity = quantity
        new_dosage = dosage
        return Prescription(new_prescription_type, new_patient, new_doctor, new_quantity, new_dosage)

    def register_patient(self, patient): # Included to address the multiplicity requirement (0..500).
        """Registers a Patient object to a Doctor; maximum of 500 Patients for each Doctor object."""
        maximum_patients = 500
        if len(self.registered_patient_list) < maximum_patients:
            self.registered_patient_list.append(patient)
        else:
            print('Maximum number of registered patients exceeded.')


class Nurse(HealthcareProfessional):
    """Creates a Nurse object, inherits from the Healthcare Professional class."""
    pass


class Prescription:
    """Creates a Prescription object, aggregating from Patient and Doctor objects."""
    def __init__(self, prescription_type, patient, doctor, quantity, dosage):
        self.prescription_type = prescription_type
        self.patient = patient.name  # Refers to Patient objects
        self.doctor = doctor.name  # Refers to Doctor objects
        self.quantity = quantity
        self.dosage = dosage


class Appointment:
    """Creates an Appointment object, aggregating from Patient and Healthcare Professional objects."""
    def __init__(self, appointment_type, staff, patient):
        self.appointment_type = appointment_type
        self.staff = staff.name  # Refers to HealthcareProfessional objects
        self.patient = patient.name  # Refers to Patient objects


class AppointmentSchedule:
    """Creates an Appointment Schedule object, composed of Appointment objects."""
    def __init__(self):
        # Instantiated sample appointment times and availability since surgery schedule is unknown.
        # Dictionary data structure allows simple mechanism to assign objects and determine availability.
        self.schedule = dict.fromkeys(['0800', '0900', '1000', '1100', '1200', '1300', '1400', '1500', '1600'],
                                      'Available')

    def add_appointment(self, appointment, time):
        """Adds an Appointment object to the Appointment Schedule at the specified time."""
        # Tests if requested appointment time is valid and available
        if time in self.schedule:
            if self.schedule[time] == 'Available':
                self.schedule[time] = appointment
            else:
                print('This appointment time is unavailable.')
        else:
            print('This is not a valid appointment time.')

    def cancel_appointment(self, appointment):
        """Removes all instances of an Appointment object from the Appointment Schedule."""
        for time, appointment_scheduled in self.schedule.items():
            if appointment_scheduled == appointment:
                self.schedule[time] = 'Available'

    def find_next_available(self):
        """Returns the next available appointment time."""
        if 'Available' in self.schedule.values():
            for time, appointment_scheduled in sorted(self.schedule.items()):
                if appointment_scheduled == 'Available':
                    print('Next available appointment: ', time)
                    break
        else:
            print('No appointments available.')


class Receptionist:
    """Creates a Receptionist object with a name and employee number."""
    def __init__(self, name, employee_number):
        self.name = name
        self.employee_number = employee_number

    def make_appointment(self, appointment_type, staff, patient):
        """Returns a new Appointment object."""
        new_appointment_type = appointment_type
        new_appointment_staff = staff
        new_appointment_patient = patient
        return Appointment(new_appointment_type, new_appointment_staff, new_appointment_patient)

    def cancel_appointment(self, appointment, schedule):
        """Removes all instances of an Appointment object from a specified Appointment Schedule object."""
        schedule.cancel_appointment(appointment)
        return schedule
