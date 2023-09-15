def find_reduced_c(binary_string, rule_0=2, rule_1=3):
    count_1 = binary_string.count('1')
    count_0_left = 0
    count_1_left = 0
    c = 0

    for pos in range(len(binary_string)):
        if binary_string[pos] == '1':
            c_p = 1
            count_1 -= 1
            c_p *= (rule_1 ** count_1) * (rule_0 ** (count_0_left + count_1_left))
            c += c_p
            count_1_left += 1
        if binary_string[pos] == '0':
            count_0_left += 1
    return c


def find_diff_of_power(binary_string):
    count_1 = binary_string.count('1')
    count_0 = binary_string.count('0') + count_1
    return (2 ** count_0) - (3 ** count_1)


def get_mod_of_b(binary_string):
    m = find_diff_of_power(binary_string)
    c = find_reduced_c(binary_string)
    return c, m, c % m

def generate_binary_strings(bit_count):
    binary_strings = []

    def genbin(n, bs=''):
        if len(bs) == n:
            binary_strings.append(bs)
        else:
            genbin(n, bs + '0')
            genbin(n, bs + '1')
    genbin(bit_count)
    return binary_strings



# binary_strings = generate_binary_strings(13)
#
# for b in binary_strings:
#     if b.count('1') == 8:
#         c, m, mod = get_mod_of_b(b)
#         print(f'[{b}] :  c: {c}, m: {m}, c % m {mod}')

import ast
expression_1 = 'x % 2 == 0'
expression_2 = 'x % 2 == 1'
expression_3 = 'x % 6 == 5'
expr_list = [expression_1, expression_2, expression_3, 'x % 6 == 3']
# parsed = ast.parse(expression)
# test = ast.dump(parsed,indent=4)
# print(test)
# walked = ast.walk(parsed)
#
# for n in walked:
#     if isinstance(n, ast.BinOp):
#         print(ast.dump(n))

exec('x = 5')
for e in expr_list:
    for n in ast.walk(ast.parse(e)):
        # print(ast.dump(n, indent=4))
        if isinstance(n, ast.Compare):
            print(ast.dump(n))
            if isinstance(n.comparators[0], ast.Constant):
                print(n.comparators[0].value)

import collatzlib as cl
col = cl.GeneralizedCollatz('t', expr_list)
print(col.max_m, col.mod_list)
print(f'Conformity {col.is_conformative()}')
for f in col.residual_mapping:
    print(f(5))

print(f'Is full {col.is_full()}')

import collatzlib as cl
# l = cl.create_func('1')
# test = l(6)
# print(test)