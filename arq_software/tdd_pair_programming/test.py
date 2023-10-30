import pytest
import algorithm


#----------------------------------------------
#       Validate number of students
#----------------------------------------------

def test_incorrect_number_of_tests_input_1():
    
    t = "-6900"
    
    with pytest.raises(algorithm.TestCasesNumberError):
        algorithm.validate_number_of_test_cases(t)


def test_incorrect_number_of_tests_input_2():
    
    t = "6900"
    
    with pytest.raises(algorithm.TestCasesNumberError):
        algorithm.validate_number_of_test_cases(t)


def test_correct_number_of_tests_input():
    
    t = "1"

    #if no exception is raised, the test is passed
    algorithm.validate_number_of_test_cases(t)


#----------------------------------------------
#        Validate number of students
#----------------------------------------------

def test_incorrect_number_of_students_input_1():
    
    n = "-6900"
    k = "1"
    a = "-1 0 1"

    with pytest.raises(algorithm.StudentsNumberError):
        algorithm.test_case_validator(n, k, a)

def test_incorrect_number_of_students_input_2():
    
    n = "6900"
    k = "1"
    a = "-1 0 1"

    with pytest.raises(algorithm.StudentsNumberError):
        algorithm.test_case_validator(n, k, a)

def test_correct_number_of_students_input():
    
    n = "3"
    k = "2"
    a = "-1 0 1"

    #if no exception is raised, the test is passed
    algorithm.test_case_validator(n, k, a)
    

#----------------------------------------------
#          Validate the value of treshold
#----------------------------------------------

def test_incorrect_number_of_treshold_input_1():
    
    n = "3"
    k = "-1"
    a = "-1 0 1"

    with pytest.raises(algorithm.ThresholdError):
        algorithm.test_case_validator(n, k, a)

def test_incorrect_number_of_treshold_input_2():
    
    n = "3"
    k = "4"
    a = "-1 0 1"

    with pytest.raises(algorithm.ThresholdError):
        algorithm.test_case_validator(n, k, a)

def test_correct_number_of_treshold_input():
        
    n = "3"
    k = "1"
    a = "-1 0 1"
    
    #if no exception is raised, the test is passed
    algorithm.test_case_validator(n, k, a)


#----------------------------------------------
#           Validate students times
#----------------------------------------------

def test_incorrect_student_times_input_1():
    
    n = "3"
    k = "1"
    a = "-1000 0 1"

    with pytest.raises(algorithm.ArrivalTimeError):
        algorithm.test_case_validator(n, k, a)

def test_incorrect_student_times_input_2():
    
    n = "3"
    k = "1"
    a = "-1 1000 0"

    with pytest.raises(algorithm.ArrivalTimeError):
        algorithm.test_case_validator(n, k, a)

def test_correct_student_times_input():
    
    n = "3"
    k = "1"
    a = "-1 0 0"

    algorithm.test_case_validator(n, k, a)


#----------------------------------------------
#           Validate students times
#----------------------------------------------

def test_inconsistent_input_1():
        
    n = "3"
    k = "1"
    a = "-1 0"

    with pytest.raises(algorithm.InconsistentInputError):
        algorithm.test_case_validator(n, k, a)

def test_inconsistent_input_2():
            
    n = "3"
    k = "1"
    a = "-1 0 1 2"

    with pytest.raises(algorithm.InconsistentInputError):
        algorithm.test_case_validator(n, k, a)

def test_consistent_input():
    
    n = "3"
    k = "1"
    a = "-1 0 1"

    algorithm.test_case_validator(n, k, a)


#----------------------------------------------
#           Check the algorithm not cancelling
#----------------------------------------------

def test_algorithm_no_cancelled():
        
    n = 3
    k = 1
    a = [-1, 0, 1]
    assert algorithm.angry_professor(n, k, a) == "NO"

def test_algorithm_no_cancelled_2():
    
    n = 5
    k = 3
    a = [-2, -1, 0, 1, 2]
    assert algorithm.angry_professor(n, k, a) == "NO"

def test_algorithm_no_cancelled_3():
    
    n = 4
    k = 2
    a = [0, -1, 2, 1]
    assert algorithm.angry_professor(n, k, a) == "NO"


#----------------------------------------------
#           Check the algorithm cancelling
#----------------------------------------------

def test_algorithm_cancelled():
        
    n = 3
    k = 3
    a = [-1, 0, 1]
    assert algorithm.angry_professor(n, k, a) == "YES"

def test_algorithm_cancelled_2():
        
    t = 2
    n = 4
    k = 3
    a = [-1, -3, 4, 2]
    assert algorithm.angry_professor(n, k, a) == "YES"


# run the test with pytest
if __name__ == "__main__":
    pytest.main()