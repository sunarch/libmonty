import secrets
from typing import List
from codetiming import Timer

# for around 1 second for each:
N = 141000

# Definitions 0.0001 for func, negligable for lambda

# for 10,000:
# Lambda one:   0.0644 seconds
# Lambda parts: 0.0861 seconds
# Function:     0.0672 seconds

# for 1,000,000:
# Lambda one:   6.6193 seconds
# Lambda parts: 7.4350 seconds
# Function:     7.3940 seconds

# -------------------------------------------------------------------- #

print("")
print("Lambda one:")
t_lambda = Timer()

# ----- #

print("Definition: ", end="")

t_lambda.start()

randlist_l_1 = lambda n: [int(''.join([str(secrets.randbelow(6) + 1) for i2 in range(5)])) for i1 in range(n)]

t_lambda.stop()

# ----- #

print("Run: ", end="")
t_lambda.start()

ls_lambda_1 = randlist_l_1(N)

t_lambda.stop()

# -------------------------------------------------------------------- #

print("")
print("Lambda parts:")
t_lambda = Timer()

# ----- #

print("Definitions: ", end="")

t_lambda.start()

throws = lambda: [(secrets.randbelow(6) + 1) for i in range(5)]

int_join = lambda ls_throws: int(''.join([str(i_throw) for i_throw in ls_throws]))

randlist_l_2 = lambda n: [int_join(throws()) for i in range(n)]

t_lambda.stop()

# ----- #

print("Run: ", end="")
t_lambda.start()

ls_lambda_2 = randlist_l_2(N)

t_lambda.stop()

# -------------------------------------------------------------------- #

print("")
print("Function:")
t_func = Timer()

# ----- #

print("Definitions: ", end="")
t_func.start()


def randlist(count: int) -> List[int]:
    ls_random = []

    for i1 in range(count):
        ls_throws = []

        for i2 in range(5):
            i_random = secrets.randbelow(6) + 1
            s_random = str(i_random)
            ls_throws.append(s_random)

        s_id = ''.join(ls_throws)
        i_id = int(s_id)

        ls_random.append(i_id)

    return ls_random


t_func.stop()

# ----- #

print("Run: ", end="")
t_func.start()

ls_func = randlist(N)

t_func.stop()

# -------------------------------------------------------------------- #

N2 = 10

print("")
print("Examples:")
print(randlist_l_1(N2))
print(randlist_l_2(N2))
print(randlist(N2))

# -------------------------------------------------------------------- #
