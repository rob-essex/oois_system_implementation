import unittest
from unittest.mock import patch
from system_implementation import *

# Initialize mock objects for integration tests

mock_healthcare_professional = HealthcareProfessional("healthcare_pro_name", "123")
mock_doctor = Doctor("doctor_name", "456")
mock_nurse = Nurse("nurse_name", "789")
mock_receptionist = Receptionist("receptionist_name", "987")
mock_patient = Patient("patient_name", "123 Main St", "1234567890")
mock_patient_2 = Patient("patient_name2", "456 2nd St", "222-333-4444")
mock_appointment = Appointment("mock_appointment_type", mock_nurse, mock_patient)
mock_appointment_2 = Appointment("mock_appointment_type_2", mock_nurse, mock_patient)
mock_appointment_schedule = AppointmentSchedule()
mock_appointment_schedule_2 = AppointmentSchedule()
mock_prescription = Prescription("mock_rx_type", mock_patient, mock_doctor, "10", "1.500")
mock_prescription2 = Prescription("mock_rx_type2", mock_patient_2, mock_doctor, "20", "2.500")

# Unit and Integration tests for each class

class TestPatient(unittest.TestCase):
    def test_patient_attributes(self):
        patient1 = Patient("Test_Patient_1","123 Main St","123-456-7890")
        self.assertEqual(patient1.name, "Test_Patient_1")
        self.assertEqual(patient1.address, "123 Main St")
        self.assertEqual(patient1.phone, "123-456-7890")

    @patch('builtins.print')
    def test_patient_request_repeat(self,test_repeat_prescription):
        mock_patient.request_repeat(mock_prescription)
        test_repeat_prescription.assert_called_with('Sending repeat prescription request of ', 'mock_rx_type', ' to ', 'doctor_name', '.')
        mock_patient.request_repeat(mock_prescription2)
        test_repeat_prescription.assert_called_with('This prescription does not belong to this patient.')

    @patch('builtins.print')
    def test_request_appointment(self, test_request):
        mock_patient.request_appointment("Annual check-up",mock_nurse)
        test_request.assert_called_with('patient_name','requests a(n) ', 'Annual check-up', 'appointment with ','nurse_name','.')

class TestHealthcareProfessional(unittest.TestCase):
    def test_healthcare_professional_attributes(self):
        healthcare_pro1 = HealthcareProfessional("Healthcare_Pro_1","123")
        self.assertEqual(healthcare_pro1.name, "Healthcare_Pro_1")
        self.assertEqual(healthcare_pro1.employee_number, "123")

    @patch('builtins.print')
    def test_consultation(self, test_consult):
        mock_healthcare_professional.consultation(mock_appointment)
        test_consult.assert_called_with('healthcare_pro_name', ' conducted the consultation for ', 'patient_name', "'s ", 'mock_appointment_type',
              'appointment.')


class TestDoctor(unittest.TestCase):
    def test_doctor_attributes(self):
        doctor1 = Doctor('doctor1_name', '111')
        self.assertEqual(doctor1.name, 'doctor1_name')
        self.assertEqual(doctor1.employee_number, '111')

    def test_issue_prescription(self):
        test_prescription = mock_doctor.issue_prescription(mock_patient,'mock_rx_type_3','300','300mg')
        self.assertEqual(test_prescription.prescription_type, 'mock_rx_type_3')
        self.assertEqual(test_prescription.patient, 'patient_name')
        self.assertEqual(test_prescription.doctor, 'doctor_name')
        self.assertEqual(test_prescription.quantity, '300')
        self.assertEqual(test_prescription.dosage, '300mg')

    def test_register_patient(self):
        mock_doctor.register_patient(mock_patient)
        self.assertIn(mock_patient, mock_doctor.registered_patient_list)

    @patch('builtins.print')
    def test_consultation(self, test_consult):
        mock_doctor.consultation(mock_appointment)
        test_consult.assert_called_with('doctor_name', ' conducted the consultation for ', 'patient_name',
                                        "'s ", 'mock_appointment_type', 'appointment.')


class TestNurse(unittest.TestCase):
    def test_nurse_attributes(self):
        nurse1 = Nurse('nurse1_name', '222')
        self.assertEqual(nurse1.name, 'nurse1_name')
        self.assertEqual(nurse1.employee_number, '222')

    @patch('builtins.print')
    def test_consultation(self, test_consult):
        mock_nurse.consultation(mock_appointment)
        test_consult.assert_called_with('nurse_name', ' conducted the consultation for ', 'patient_name',
                                        "'s ", 'mock_appointment_type', 'appointment.')


class TestPrescription(unittest.TestCase):
    def test_prescription_attributes(self):
        prescription1 = Prescription('ibuprofen',mock_patient,mock_doctor,'200','200mg')
        self.assertEqual(prescription1.prescription_type, 'ibuprofen')
        self.assertEqual(prescription1.patient, 'patient_name')
        self.assertEqual(prescription1.doctor, 'doctor_name')
        self.assertEqual(prescription1.quantity, '200')
        self.assertEqual(prescription1.dosage, '200mg')


class TestAppointment(unittest.TestCase):
    def test_appointment_attributes(self):
        appointment1 = Appointment('consultation', mock_nurse, mock_patient)
        self.assertEqual(appointment1.appointment_type, 'consultation')
        self.assertEqual(appointment1.staff, 'nurse_name')
        self.assertEqual(appointment1.patient, 'patient_name')


class TestAppointmentSchedule(unittest.TestCase):
    def test_schedule_attributes(self):
        test_schedule_1 = AppointmentSchedule()
        self.assertDictEqual(test_schedule_1.schedule, mock_appointment_schedule_2.schedule)

    @patch('builtins.print')
    def test_add_appointment(self, test_unavailable):
        mock_appointment_schedule.add_appointment(mock_appointment, '0900')
        self.assertIs(mock_appointment_schedule.schedule['0900'], mock_appointment)
        mock_appointment_schedule.add_appointment(mock_appointment_2, '0900')
        test_unavailable.assert_called_with('This appointment time is unavailable.')
        mock_appointment_schedule.add_appointment(mock_appointment_2, '0930')
        test_unavailable.assert_called_with('This is not a valid appointment time.')

    def test_cancel_appointment(self):
        mock_appointment_schedule.cancel_appointment(mock_appointment)
        self.assertEqual(mock_appointment_schedule.schedule['0900'],'Available')

    @patch('builtins.print')
    def test_find_next_available(self, test_next_appointment):
        # instantiate mock appointment placeholders
        mock_appointment_schedule.add_appointment(mock_appointment,'0800')
        mock_appointment_schedule.add_appointment(mock_appointment_2, '0900')

        mock_appointment_schedule.find_next_available()
        test_next_appointment.assert_called_with('Next available appointment: ', '1000')


class TestReceptionist(unittest.TestCase):
    def test_receptionist_attributes(self):
        receptionist1 = Receptionist('receptionist_1_name','555')
        self.assertEqual(receptionist1.name, 'receptionist_1_name')
        self.assertEqual(receptionist1.employee_number, '555')

    def test_make_appointment(self):
        test_appointment = mock_receptionist.make_appointment('consultation',mock_doctor,mock_patient)
        self.assertEqual(test_appointment.appointment_type, 'consultation')
        self.assertEqual(test_appointment.staff, 'doctor_name')
        self.assertEqual(test_appointment.patient, 'patient_name')

    def test_cancel_appointment(self):
        # instantiate mock appointment placeholders
        mock_appointment_schedule_3 = AppointmentSchedule()
        mock_appointment_schedule_3.add_appointment(mock_appointment, '0800')
        mock_appointment_schedule_3.add_appointment(mock_appointment_2, '0900')

        mock_receptionist.cancel_appointment(mock_appointment, mock_appointment_schedule_3)
        self.assertIsNot(mock_appointment_schedule_3.schedule['0800'], mock_appointment)
        self.assertIs(mock_appointment_schedule_3.schedule['0900'], mock_appointment_2)

if __name__ == '__main__':
    unittest.main()
