# Python Basics

## Variables and Data Types:

Python has several basic data types like integers, floats, strings, and booleans. You can assign values to variables without declaring their type.

```py
# Integer
num = 10
# Float
pi = 3.14
# String
greeting = "Hello, World!"
# Boolean
is_true = True
```

## Operators:

Python supports a variety of operators such as arithmetic operators (+, -, \*, /, %, \*\*, //), comparison operators (==, !=, >, <, >=, <=), logical operators (and, or, not), and more.

```py
# Arithmetic operators
add = 5 + 3  # 8
sub = 5 - 3  # 2
mul = 5 * 3  # 15
div = 5 / 3  # 1.6666666666666667

# Comparison operators
eq = 5 == 3  # False
ne = 5 != 3  # True
gt = 5 > 3   # True
lt = 5 < 3   # False

# Logical operators
and_op = True and False  # False
or_op = True or False    # True
not_op = not True        # False
```

## Control Flow:

Python uses if, elif, and else statements for conditional execution of code. It also has while and for loops for repeated execution of code.

```py
# If, elif, else statements
x = 10
if x > 0:
    print("Positive")
elif x < 0:
    print("Negative")
else:
    print("Zero")

# While loop
i = 0
while i < 5:
    print(i)
    i += 1

# For loop
for i in range(5):
    print(i)
```

## Functions:

You can define reusable pieces of code with def keyword. Python also supports anonymous functions (lambda functions).

```py
# Defining a function
def greet(name):
    return f"Hello, {name}!"

# Calling a function
print(greet("Alice"))

# Lambda function
square = lambda x: x * x
print(square(5))
```

## Data Structures:

Python has several built-in data structures like lists, tuples, sets, and dictionaries.

```py
# List
fruits = ["apple", "banana", "cherry"]
# Tuple
coordinates = (10.0, 20.0)
# Set
unique_numbers = {1, 2, 2, 3, 4, 4, 4, 5}
# Dictionary
person = {"name": "Alice", "age": 25}
```

## Classes and Objects:

Python supports object-oriented programming with classes and objects.

```py
# Defining a class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."

# Creating an object
alice = Person("Alice", 25)
print(alice.greet())
```

## Modules and Packages:

You can organize your code into modules and packages, which can be imported using the import statement.

```py

# Importing a module
import math
print(math.pi)

# Importing a function from a module
from math import sqrt
print(sqrt(16))

# Importing a module and aliasing it
import numpy as np
print(np.array([1, 2, 3]))

```

## Exception Handling:

Python uses try, except, finally, and raise statements to handle exceptions.

```py
try:
    x = 1 / 0
except ZeroDivisionError:
    print("You can't divide by zero!")
finally:
    print("This gets executed no matter what.")
```

## File I/O:

Python has built-in functions for reading from and writing to files.

```py
# Writing to a file
with open("test.txt", "w") as f:
    f.write("Hello, World!")

# Reading from a file
with open("test.txt", "r") as f:
    print(f.read())
```

## Standard Library:

Python comes with a rich standard library that includes modules for working with the operating system, regular expressions, threading, networking, and more.

```py
# Using the os module to get the current working directory
import os
print(os.getcwd())

# Using the re module for regular expressions
import re
print(re.match(r"\d+", "1234abc"))

# Using the threading module to create a new thread
import threading
def print_nums():
    for i in range(5):
        print(i)

thread = threading.Thread(target=print_nums)
thread.start()
thread.join()
```

## Group Work

8 minutes in group #correct or #incorrect (if possible - why?)
4 minutes check against answers (one page without answers | 4 with answers)

```py

# Integer
num = 6 # correct
num1 = "10"  # Incorrect - This is a string, not an integer
2num = 10 # Incorrect - variable cannot start with number
num3 = 3.14  # This is a float, not an integer
num4 = -5 # correct
num6 = True  # This is a boolean, not an integer

# Float
float1 = "10.0"  # Incorrect - This is a string, not a float
float2 = 8.0 # Correct float
float3 = 8 # Incorrect - This is an integer, not a float
float4 = 3  # Incorrect - This is an integer, not a float
float5 = -5.5 # Correct float
float6 = 0.0 # Correct float
float7 = False  # Incorrect - This is a boolean, not a float
    float8 = 2.0 # # incorrect - variable indentation is incorrect (4 spaces or tab)
pi = 3.14 # correct

# String
str1 = "Hello, World!" # Correct string
str2 = 123  # Incorrect - This is an integer, not a string
str3 = 3.14  # Incorrect - This is a float, not a string
str4 = 'Python is fun.' # Correct string
str5 = """This is a
multi-line string.""" # Correct string
7str = "I am 7th!" # Incorrect string -  variable cannot start with number
Str8 = True  # Incorrect - This is a boolean, not a string

# Boolean
Bool1 = "True"  # Incorrect - # This is a string, not a boolean
Bool2 = True  # Correct – typical way
Bool3 = 1  # Incorrect - This is an integer, not a boolean
Bool4 = False  # Correct – typical way
Bool5 = 0.0  # Incorrect - This is a float, not a boolean
Bool6 = bool(1)  # Correct returns True
Bool7 = bool(-1)  # Correct returns True
Bool8 = bool(5)  # Correct returns True
Bool9 = bool(0)  # Correct returns False
Bool10 = 3 == 2 # Correct returns False

```

## Group Work

8 minutes in group #correct or #incorrect (if possible - why?)
4 minutes check against answers (one page without answers | 4 with answers)

### Arithmetic Operators

```py


# Addition
add = 5 + 3  # Correct
add1 = "5" + 3  # Incorrect - can't add string and integer
add2 = 5 + "3"  # Incorrect - can't add integer and string
add3 = "5" + "3"  # Correct - concatenates strings # "53"
3add = "5" + "3"  # Correct - concatenates strings # "53"
add4 = 5.0 + 3  # Correct - adds float and integer
add5 = True + 3  # Incorrect - can't add boolean and integer

# Subtraction
sub = 5 - 3  # Correct
sub1 = "5" - 3  # Incorrect - can't subtract integer from string
sub2 = 5 - "3"  # Incorrect - can't subtract string from integer
sub3 = "5" - "3"  # Incorrect - can't subtract strings
sub4 = 5.0 - 3  # Correct - subtracts integer from float
sub5 = True - 3  # Incorrect - can't subtract integer from boolean

# Modulus
mod = 10 % 3  # Correct - returns the remainder of the division, 3 goes 3 times in 10 and 1 is left = result 1
mod1 = "10" % 3  # Incorrect - can't use modulus with string and integer
mod2 = 10 % "3"  # Incorrect - can't use modulus with integer and string
mod3 = "10" % "3"  # Incorrect - can't use modulus with strings
mod4 = 10.0 % 3  # Correct - returns the remainder of the division,3 goes 3 times in 10 and 1 is left = result 1
mod5 = True % 3  # Incorrect - can't use modulus with boolean and integer

# Division
div = 10 / 3  # Correct - performs floating point division - 3.3333
div1 = "10" / 3  # Incorrect - can't divide string by integer
div2 = 10 / "3"  # Incorrect - can't divide integer by string
div3 = "10" / "3"  # Incorrect - can't divide string by string
div4 = 10.0 / 3  # Correct - performs floating point division - 3.3333
div5 = True / 3  # Incorrect - can't divide boolean by integer
    div6 = 10 / 3 # # incorrect - variable indentation is incorrect (4 spaces or tab)

# Multiplication
mul = 5 * 3  # Correct - multiplies two numbers
mul1 = "5" * 3  # Correct - repeats the string 3 times - "555"
mul2 = 5 * "3"  # Correct - repeats the string 5 times  - "33333"
mul3 = "5" * "3"  # Incorrect - can't multiply strings
mul4 = 5.0 * 3  # Correct - multiplies float and integer
mul5 = True * 3  # Incorrect - can't multiply boolean and integer

# Exponentiation
exp = 2 ** 3  # Correct - raises the first number to the power of the second number
exp1 = "2" ** 3  # Incorrect - can't raise string to the power of integer
exp2 = 2 ** "3"  # Incorrect - can't raise integer to the power of string
exp3 = "2" ** "3"  # Incorrect - can't raise string to the power of string
exp4 = 2.0 ** 3  # Correct - raises float to the power of integer
exp5 = True ** 3  # Incorrect - can't raise boolean to the power of integer

# Floor Division
floor_div = 9 // 3  # Correct - performs integer division, rounding down - 3
floor_div1 = "10" // 3  # Incorrect - can't perform floor division with string and integer
floor_div2 = 10 // "3"  # Incorrect - can't perform floor division with integer and string
floor_div3 = "10" // "3"  # Incorrect - can't perform floor division with strings
floor_div4 = 9.0 // 2  # Correct - performs floor division, rounding down - 3
floor_div5 = True // 3  # Incorrect - can't perform floor division with boolean and integer
```

## Group Work

8 minutes in group #correct or #incorrect (if possible - why?)
4 minutes check against answers (one page without answers | 4 with answers)

### Comparison Operators

```py
# Equality
eq = 5 == 3  # Correct - compares integers
eq1 = "5" == 3  # Correct - compares string and integer, returns False
eq2 = 5 == "3"  # Correct - compares integer and string, returns False
eq3 = "5" == "3"  # Correct - compares strings, returns False
eq4 = 5.0 == 3  # Correct - compares float and integer, returns False
eq5 = True == 3  # Correct - compares boolean and integer, returns False (True is equivalent to 1 in Python)

# Not Equal
neq = 5 != 3  # Correct - compares integers
neq1 = "5" != 3  # Correct - compares string and integer, returns True
neq2 = 5 != "3"  # Correct - compares integer and string, returns True
neq3 = "5" != "3"  # Correct - compares strings, returns True
neq4 = 5.0 != 3  # Correct - compares float and integer, returns True
neq5 = True != 3  # Correct - compares boolean and integer, returns True
    neq6 = 5 != 4 # incorrect - variable indentation is incorrect (4 spaces or tab)

# Greater than
gt = 5 > 3  # Correct - compares integers
gt1 = "5" > 3  # Incorrect - TypeError, can't compare string and integer
gt2 = 5 > "3"  # Incorrect - TypeError, can't compare integer and string
gt3 = "5" > "3"  # Correct - compares strings, but note that it's lexicographical comparison
gt4 = 5.0 > 3  # Correct - compares float and integer
gt5 = True > 3  # Correct - compares boolean and integer, returns False (True is equivalent to 1 in Python)

# other similar comparison operators:
# Less than <
# Greater than or equal >=
# Less than or equal <=
```

## Group Work

8 minutes in group #correct or #incorrect | #truthy or #falsy (if possible - why?)
4 minutes check against answers (one page without answers | 4 with answers)

# Logical Operators

```py

# Truthy vs Falsy values
print(bool(None))  # Falsy - False
print(bool(False))  # Falsy - False
print(bool(True))  # Truthy - True
print(bool(0))  # Falsy - False
print(bool(1))  # Truthy - True
print(bool(-1))  # Truthy - True
print(bool(0.1))  # Truthy - True
print(bool(0.0))  # Falsy - False
print(bool(""))  # Falsy - False
print(bool("Hello"))  # Truthy - True
print(bool([1, 2, 3]))  # Truthy - True
print(bool([]))  # Falsy - False
print(bool({}))  # Falsy - False
print(bool({"name": "John"}))  # Truthy - True

# And
and_op = True and False  # Correct - returns False
and_op1 = "True" and False  # Correct - returns False because 'and' operation with a falsy value (False) returns the falsy value
and_op2 = True and "False"  # Correct - returns "False" because 'and' operation with a truthy value (True) returns the next value
and_op3 = "True" and "False"  # Correct - returns "False" because 'and' operation with a truthy value ("True") returns the next value
and_op4 = 1 and 0  # Correct - returns 0 because 'and' operation with a truthy value (1) returns the next value
and_op5 = 1.0 and 0  # Correct - returns 0 because 'and' operation with a truthy value (1.0) returns the next value

# Or
or_op = True or False  # Correct - returns True
or_op1 = "True" or False  # Correct - returns "True" because 'or' operation with a truthy value ("True") returns the truthy value
or_op2 = False or "False"  # Correct - returns "False" because 'or' operation with a falsy value (False) returns the next value
or_op3 = "" or "False"  # Correct - returns "False" because 'or' operation with a falsy value ("") returns the next value
or_op4 = 0 or 1  # Correct - returns 1 because 'or' operation with a falsy value (0) returns the next value
or_op5 = 0.0 or 1.0  # Correct - returns 1.0 because 'or' operation with a falsy value (0.0) returns the next value

# Not
not_op = not True  # Correct - returns False
not_op1 = not "True"  # Correct - returns False because 'not' operation with a truthy value ("True") returns False
not_op2 = not False  # Correct - returns True
not_op3 = not ""  # Correct - returns True because 'not' operation with a falsy value ("") returns True
not_op4 = not 0  # Correct - returns True because 'not' operation with a falsy value (0) returns True
not_op5 = not 0.0  # Correct - returns True because 'not' operation with a falsy value (0.0) returns True



```

### Examples (similar to if statements, explained later)

##### print_if_true

True and print('I run because left side is True')

##### print_if_false

False or print('I run because left side is False')

##### Complex Example

import datetime

##### Get the current day of the week

current_day = datetime.datetime.now().strftime('%A')
is_monday = current_day == 'Monday'

##### Print a message if it's not Monday

if not is_monday:
print('I am glad it is not Monday!')

## Logical Operators vs If Statements

### Logical Operators

- **Conciseness:** Logical operators can make your code more concise because they allow you to express complex logic in a single line.
- **Short-Circuit Evaluation:** The `and` and `or` operators in Python use short-circuit evaluation, which can improve performance. If the result of the operation can be determined by the first operand, the second operand is not evaluated.
- **Expression Evaluation:** Logical operators return a value, which can be used in expressions or assigned to a variable.

### If Statements

- **Readability:** `if` statements can make your code more readable, especially when dealing with complex conditions or multiple branches of execution.
- **Flexibility:** `if` statements allow for more complex decision-making structures, including `elif` and `else` clauses.
- **Code Organization:** `if` statements can help organize your code into distinct blocks, which can make it easier to understand and maintain.

In general, if you're performing a simple check with one or two conditions, logical operators can be a concise and efficient choice. For more complex decision-making, `if` statements are usually more appropriate. It's also common to use logical operators within `if` statements to combine conditions.
