import base64
import zlib
import sys
import string

def generate_bp(program: list[int], template: str) -> str:
    length = 1024
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
    bp = generate_bp([i for i in range(1024)], sys.argv[2])
    
    if len(sys.argv) >= 4:
        with open(sys.argv[3], 'w') as fd:
            fd.write(bp)
    else:
        print(bp)