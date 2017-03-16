
#1-st task
def like(numbers: str, a_set: str, b_set: str):
    ''' The function takes three positional arguments as string type. All arguments represent
        a set of space-separated digits.
        Function returns int variable according such algorithm: 
        - variable is increased by one if the number from the first
        sequence is contained only in the second (argument a_set)
        - variable is reduced by one if the number from the first
        sequence is contained only in the third (argument b_set)
        - if the number is missing or present in both sequences -
        the variable does not change its meaning
    '''
    likes = 0
    numbersList = numbers.split(' ')
    a_set = a_set.split(' ')
    b_set = b_set.split(' ')
    for x in numbersList:
        if x in a_set and x in b_set:
            continue;
        elif x in a_set:
            likes += 1;
        elif x in b_set:
            likes -= 1;
    return likes;
            
    



#2-nd task
def fine_print(n: int):
    ''' Takes one argument as int. 
        Prints all integers from 1 to n inclusive in four representations - decimal,
        octal, hexadecimal and binary. '''
    for x in range(1, n+1):
        line = '{0:< 10d} {0:< 10o} {0:< 10x} {0:< 10b}'.format(x)
        print(line)        


#3-rd task
def decorator(func):
    '''
    A decorator for function func.
    If exception occurs it print explanation of exception.
    Otherthise it returns the result of function func.
    '''
    def wrapped_func(*args, **kwargs):        
        try:
            return args[0] / args[1]
        except Exception as e:
            print('Exception occurred in func: ' + str(e))
            lineOfArgs = ' '.join(str(x) for x in args)
            print('Input args: {}'.format(lineOfArgs))
            print('Input kwargs: ' + str(kwargs))
            return None
    return wrapped_func


    
@decorator
def func(x, y, **kwargs):
    ''' Function takes 3 arguments. 
        It returns the result of dividing the first by the second argument. '''
    return x / y

 



#4-th task
def filter_func(emails):
    ''' Function takes one argument - the list of email addresses.
        It returns a sorted list of valid email addresses. '''
    def validate_email(email):
        atPosition = email.find('@')
        if atPosition < 0:
            return False

        emailFirstPart = email[:atPosition].lower()
        allValidSymbols = 'qwertyuiopasdfghjklzxcvbnm1234567890_'
        for x in emailFirstPart:
            if not x in allValidSymbols:
                return False

        dotPosition = email.find('.')
        if dotPosition < 0:
            return False

        if dotPosition - atPosition <= 2:
            return False

        return True    

    return sorted( filter(validate_email, emails) )
    



if __name__ == "__main__":
    #1-st task
    numbers = '3 2 10 7 5 5 2 1 2'
    a = '2 3 7'
    b = '5 10 7'
    print(like(numbers, a, b))

    numbers = '1 4 10 20 1 11 12'
    a = '1 4 1 12'
    b = '1 12 10 20'
    print(like(numbers, a, b))

    #2-nd task
    fine_print(13)

    #3-rd task
    print(func(10, 0, op='division', base=10))
    print(func(10, 2, op='division', base=10))

    #4-th task
    emails = ['abc@gmail.com.ua', '*@ank.com', '_ny@us.gov.us', 'z@b.kk']
    print(filter_func(emails))
    


