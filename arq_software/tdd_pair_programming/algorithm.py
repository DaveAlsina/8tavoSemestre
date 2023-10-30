#----------------------------------------------
#               Custom Exceptions
#----------------------------------------------
class TestCasesNumberError(Exception):
    """
        Exception raised for errors in the input number of test cases.
    """
    pass

class StudentsNumberError(Exception):
    """
        Exception raised for errors in the input number of students.
    """
    pass

class ThresholdError(Exception):
    """
        Exception raised for errors in the input threshold.
    """
    pass

class ArrivalTimeError(Exception):
    """
        Exception raised for errors in the input arrival time.
    """
    pass

class InconsistentInputError(Exception):
    """
        Exception raised for situations in which the number of students is different from the number of arrival times.
    """
    pass

#----------------------------------------------
#              Algorithm Implementation
#----------------------------------------------

def take_number_of_test_cases_input():
    t = input("Enter the number of test cases: ").strip()
    return t

def take_test_case_input():

    nk = input("Enter the number of students and the threshold (separated by spaces): ").strip()
    a  = input("Enter the arrival times of the students (separated by spaces): ").strip()

    n, k = nk.split(" ")
    return n, k, a


def test_case_validator(n: str, k: str, a: str):
    
    n = int(n)
    k = int(k)
    a = [int(x) for x in a.split(" ")]

    # n between 1 and 1000
    if n < 1 or n > 1000:
        raise StudentsNumberError
        
    # k between 1 and n
    if k < 1 or k > n:
        raise ThresholdError
    
    # a between -100 and 100
    if any([True for ai in a if (ai < -100) or (ai > 100)]):
        raise ArrivalTimeError

    # the number of students must be equal to the number of arrival times
    if len(a) != n:
        raise InconsistentInputError

    return n, k, a

def validate_number_of_test_cases(t: str) -> int:
    t = int(t)
    
    # t between 1 and 10 
    if t < 1 or t > 10:
        raise TestCasesNumberError

    return t


def angry_professor(n: int, k: int, a: list[int]):
    

    """
        The main function of the algorithm.
        This is the professor's algorithm.

        Input:
        ---------

        - n: the number of students
        - k: the threshold
        - a: the arrival times of the students

        Output:
        ---------
        - "YES" if the class is cancelled
        - "NO" otherwise
    """

    # the class is cancelled if the number of students who arrived on time is less than the threshold
    if len([x for x in a if x <= 0]) < k:
        return "YES"
    
    return "NO"


def main():

    t = take_number_of_test_cases_input()
    t = validate_number_of_test_cases(t)
    print("-"*50)

    for _ in range(t):
        n, k, a = take_test_case_input()
        n, k, a = test_case_validator(n, k, a)
        result = angry_professor(n, k, a)
    
        print(f"The class should be cancelled? {result}")
        print("-"*50 + "\n")


if __name__ == "__main__":
    main()