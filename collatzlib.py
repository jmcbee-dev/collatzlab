import json
import ast

'''
Generalized Collatz is defined by a set of rules in a given modulo.
The typical written form is a piecewise mapping

T(x) = {
            f_0(x)    if x === v_0 (mod m_0)
            f_1(x)    if x === v_1 (mod m_1)
            f_2(x)    if x === v_2 (mod m_2)
            ...
        }

Each mapping here is called a Collatz rule. 
Each Collatz rule's modulo should conform to being multiples of each other.
That is, if m_0 = 4, then all other m_n should either be k*4, or k*2. Otherwise
certain Collatz rules are guaranteed to overlap.

Ex.

T(x) = {
            1/2 x           if x === 0 (mod 2)
            4/3 x - 1/3     if x === 1 (mod 4)
            4/3 x + 1/3     if x === 3 (mod 4)
        }
Is valid as all modulos conform to k*2. However the system

T(x) = {
            1/2 x           if x === 0 (mod 2)
            4/3 x - 1/3     if x === 2 (mod 3)
            4/3 x + 1/3     if x === 5 (mod 6)
        }  
Is non-conformative as even though 2 | 6, and 3 | 6, 2 !| 3. 
Therefore the system is invalid.

    
Additionally, a Collatz mapping is complete if it is conformative with no overlapping
and defined for all residuals of the maximum modulo.
    m_max = max(m_n)
    set(range(m_max)) contains all possible residuals
    remove from the set all residuals obtained via rules. 
'''


class GeneralizedCollatz:
    def __init__(self, list_of_functions, list_of_expressions):
        # self.function_table = self._extract_functions(list_of_functions)
        self.residual_mapping = self._extract_functions(list_of_expressions)
        self._set_mod_list(list_of_expressions)
        self.max_m = self._find_max_modulo()
        self._set_congruencies(list_of_expressions)
        return

    def _extract_functions(self, list_of_functions):
        '''
        Places each mapping in an array

        Parameters:
            list_of_functions : list<string>
                list of expressions

        Returns:
            function_table : list<rational number-> rational number>
                executable functions stored in a list
        '''
        function_table = []

        for f in list_of_functions:
            function_table.append(create_func(f))

        return function_table

    def _set_mod_list(self, mod_rules):
        self.mod_list = []

        for rule in mod_rules:
            for n in ast.walk(ast.parse(rule)):
                if isinstance(n, ast.BinOp):
                    self.mod_list.append(n.right.value)

    def _find_max_modulo(self):
        return max(self.mod_list)

    def _set_congruencies(self, mod_rules):
        self.congruencies = []

        for rule in mod_rules:
            for n in ast.walk(ast.parse(rule)):
                if isinstance(n, ast.Compare):
                    if isinstance(n.comparators[0], ast.Constant):
                        self.congruencies.append(n.comparators[0].value)

    def is_conformative(self):
        for m in set(self.mod_list):
            for test_against in self.mod_list:
                if test_against > m:
                    continue
                if m % test_against != 0:
                    return False
        return True

    def is_full(self):
        residues = set(range(self.max_m))

        for idx, mod_val in enumerate(self.mod_list):
            for r in residues.copy():
                r_check = r % mod_val
                if r in residues:
                    if r_check == self.congruencies[idx]:
                        residues.remove(r)
                else:
                    print(f'Overlapping residue at {r} mod {self.max_m}')
                    return False
        return len(residues) == 0

    def is_complete(self):
        return

    def iterate_on(self, x, limit=1000):
        return


def create_func(expr):
    def _function_x(x=None):
        return eval(expr)

    return _function_x


class CollatzMapping:
    def __init__(self):
        self.collatz_map = dict()
        self.max_m = None
        return

    def _set_rule_mapping(self, residual, function_x, constant):
        if residual in self.collatz_map.keys():
            self._overlappingError(residual)
            return

        self.collatz_map[residual] = (create_func(function_x), constant)
        return

    def _overlappingError(self, residual):
        print(f'Two rules in table clash for modulo {self.max_m} with residual {residual}')
        return


class DiophantineCollatz:
    def __init__(self, power_of_three, power_of_two, c):
        self.three = power_of_three
        self.two = power_of_two
        self.c = c
        self.general_solution_x = None
        self.general_solution_y = None
        self.particular_solution_x = None
        self.particular_solution_y = None
        self.euclidian_steps = []
        self.solution = None
        self.eq = None

    class EuclidianStep:
        def __init__(self, target, source, factor=1, quotient=None, remainder=None):
            self.factor = factor
            self.target = target
            self.source = source
            if quotient is None:
                self.quotient = target // source
                self.remainder = target % source
            else:
                self.quotient = quotient
                self.remainder = remainder

        def back_substitution(self, prior_step: "EuclidianStep"):
            return DiophantineCollatz.EuclidianStep(
                prior_step.source,
                self.target,
                factor=self.quotient,
                quotient=self.factor + self.quotient * prior_step.quotient,
                remainder=1
            )

        def eprint(self):
            eq = f'{self.target} = ({self.quotient}) * {self.source} + {self.remainder}'
            print(self.eq)
            return eq

    def solve(self):
        step = self.EuclidianStep(3 ** self.three, 2 ** self.two)
        if step.quotient != 0:
            self.euclidian_steps.append(step)

        while step.remainder != 1:
            step = self.EuclidianStep(step.source, step.remainder)
            self.euclidian_steps.append(step)

        last_step = None
        for s in reversed(self.euclidian_steps):
            if last_step is None:
                last_step = s
                continue
            last_step = last_step.back_substitution(s)

        if len(self.euclidian_steps) % 2 == 0:
            # print(f'3^{self.three} ( {-c * last_step.quotient} ) - 2^{self.two} ( {-c * last_step.factor} ) = {-c}')
            self.particular_solution_x = {self.c * last_step.quotient}
            self.particular_solution_y = {self.c * last_step.factor}
        else:
            # print(f'3^{self.three} ( {c * last_step.quotient} ) - 2^{self.two} ( {c * last_step.factor} ) = {-c}')
            self.particular_solution_x = {self.c * last_step.factor}
            self.particular_solution_y = {self.c * last_step.quotient}


def find_c(binary_string, rule_0=2, rule_1=3):
    count_1 = binary_string.count('1')
    count_0_left = 0
    c = 0

    for pos in range(len(binary_string)):
        if binary_string[pos] == '1':
            c_p = 1
            count_1 -= 1
            c_p *= (rule_1 ** count_1) * (rule_0 ** count_0_left)
            c += c_p
        if binary_string[pos] == '0':
            count_0_left += 1
    return c


def find_collatz_stop_binary(n, rule_even=2, rule_odd=3, rule_add=1, limit=120000):
    even_step = 0
    odd_step = 0
    binary_string = ''
    n_orig = n
    mx = n
    # Do while loop
    if n % rule_even == 0:
        n = n // rule_even
        even_step += 1
        binary_string += '0'
    else:
        n = rule_odd * n + rule_add
        odd_step += 1
        binary_string += '1'
    while abs(n) > abs(n_orig) and odd_step + even_step < limit:
        if n > mx:
            mx = n
        if n % rule_even == 0:
            n = n // rule_even
            even_step += 1
            binary_string += '0'
        else:
            n = rule_odd * n + rule_add
            odd_step += 1
            binary_string += '1'
    return even_step, odd_step, even_step + odd_step, binary_string, mx


# Given a binary string, find the infinite rational cycle
# note if rule_even^count_0 - rule_odd^count_1 % c == 0
# Then we've found a cycle with integer values
def find_rational_cycle(binary_string, rule_even=2, rule_odd=3):
    c = find_c(binary_string)
    count_1 = binary_string.count('1')
    count_0 = binary_string.count('0')

    g = 2 ** count_0 - 3 ** count_1
    h = 2 ** count_0 + 3 ** count_1

    return c, rule_even ** count_0 - rule_odd ** count_1


# From a given number n, return the path until the number is reduced
def find_reducing_path(n):
    even_step = 0
    odd_step = 0
    path = [n]
    n_orig = n
    mx = n
    # Do while loop
    if n % 2 == 0:
        n = n // 2
        even_step += 1
    else:
        n = 3 * n + 1
        odd_step += 1
    while abs(n) > abs(n_orig):
        path.append(n)
        if n > mx:
            mx = n
        if n % 2 == 0:
            n = n // 2
            even_step += 1
        else:
            n = 3 * n + 1
            odd_step += 1
    return path


#
# n = 1980976057694848447
# # n = 2674309547647
# n = 77671
# n = 763
#
#
# two, three, total, b, m = find_collatz_stop_binary(n)
# c = find_c(b)
# # print(n, m)
# # print(f'D(x,y) : 3 ^ {three} x - 2 ^ {two} y = {-c}')
# # print(b)
# # print(find_rational_cycle(b))
#
# d = DiophantineCollatz(three, two, c)
# d.solve()
#
# for e in d.euclidian_steps:
#     e.eprint()

#
# block_size = 15
# numbers_to_check = [1]
# block_dictionary = {}
#
# for b in range(block_size+1):
#     removed = set()
#     for n in numbers_to_check:
#         if n not in block_dictionary:
#             deciding_block, _, _, _, _ = find_collatz_stop_binary(n)
#             block_dictionary[n] = deciding_block
#         if block_dictionary[n] < b:
#             block_dictionary.pop(n)
#             removed.add(n)
#     for n in removed:
#         numbers_to_check.remove(n)
#     numbers_to_check.extend([n + 2 ** b for n in numbers_to_check.copy()])
#     print(f'Block size: 2 ^ {b} : Percentage to check: {len(block_dictionary.keys()) / 2 ** (b)}')
# # print(numbers_to_check)
# print(f'Numbers to check at the 2 ^ {block_size} block:\n\t {len(block_dictionary.keys())}')
#
# print(max(block_dictionary.values()))
#
# with open('checknums.dat', 'w') as f:
#     json.dump(numbers_to_check, f)
#
# with open('blockdict.dat', 'w') as f:
#     json.dump(block_dictionary, f)

# print(block_dictionary)
# print(numbers_to_check)


# print(f'Binary string for {n}: {b}\nc : {c}')
# print(f'D(x,y) : 3 ^ {three} x - 2 ^ {two} y = {-c}')
# X_2 = m / n ** 2
# print(X_2)
#
# print( c / 2 ** two)

# print(2**two + 27)

# n, d = find_rational_cycle(b)
# print(f'Cycle: {n} / {d}  =  {n / d}')
# n, d = find_rational_cycle(b*2)
# print(f'Cycle: {n} / {d}  =  {n / d}')
# n, d = find_rational_cycle(b*3)
# print(f'Cycle: {n} / {d}  =  {n / d}')
# n, d = find_rational_cycle(b*4)
# print(f'Cycle: {n} / {d}  =  {n / d}')
#
# n, d = find_rational_cycle('10'*2+'0'*2)
# print(f'Cycle: {n} / {d}  =  {n / d}')
# print(b)
# for i in range(len(b)):
#     b_1 = b[i:] + b[0:i]
#     print(b_1)
#     c = find_c(b_1)
#     print(c, 3*c)

from array import *
# sum_of_power_table = [ [2 ** i + 3 ** j for j in range(10)] for i in range(10)]
#
# print(sum_of_power_table)

# e, o, total, b, m = find_collatz_stop_binary(1087)
# print(find_c(b))
# print(3 ** o,- 2 ** e)
# print(b)
#
# print(find_c('10'*6 + '0'*4))
