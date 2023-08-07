'''
Format expected: integer, followed by tuples of int and array of tuples of ints

Example:
size = 256
instructions = [
    (0, [(1, 11)]),
    (2, [(1, 11), (3, 29)])
]

Here, 0 is Noop, and bit 11 is set in the microcode
2 is Reset, and bit 11 is set, as well as the value '3' for bits 29-30

1 instruction per line
'''

import base64
import zlib
import sys
import string
import importlib

def generate_ucode(size: int, instructions: list[tuple]) -> list:
    ucode = [0 for i in range(size)]
    
    for i, bits in instructions:
        code = 0
        for v, s in bits:
            code |= (v << s)
        ucode[i] = code
    
    return ucode

def generate_bp(program: list[int], template: str, length: int = 256) -> str:
    while len(program) < length:
        program.append(0)

    with open(template) as fd:
        t = fd.read()

    for i in range(length):
        t = t.replace('%s', str(program[i]), 1)

    z = zlib.compress(bytes(t, 'utf-8'), level=9)
    b = '0' + str(base64.b64encode(z))[2:-1]

    return b

if __name__ == '__main__':
    mod = importlib.import_module(sys.argv[1])
    
    ucode = generate_ucode(mod.size, mod.instructions)
    
    print(ucode)
    
    bp = generate_bp(ucode, sys.argv[2], mod.size)
    
    if len(sys.argv) >= 4:
        with open(sys.argv[3], 'w') as fd:
            fd.write(bp)
    else:
        print(bp)