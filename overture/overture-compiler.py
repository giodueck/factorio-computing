import base64
import zlib
import sys
import string

# program = [-4, 129, 1, 130, 64, 153, 4, 197, 9, 196, 0, 196]

def generate_bp(program: list[int], template: str) -> str:
    length = 64
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
    # arg 0 = program name
    # arg 1 = input
    # arg 2 = template
    # arg 3 = output filename (default print to stdout)
    
    ''' Assembly definition
    0-63 (immediates)
    add                          64
    sub                          65
    mul                          66
    div                          67
    and                          68
    orr                          69
    not                          70
    xor                          71
    mov rs rd   (2<<6) | (s<<3) | d
        s/d in (0-7)
    nop                         192
    jeq                         193
    jlt                         194
    jle                         195
    jmp                         196
    jne                         197
    jge                         198
    jgt                         199
    '''
    assembly = {
        'add':  64,
        'sub':  65,
        'mul':  66,
        'div':  67,
        'and':  68,
        'orr':  69,
        'not':  70,
        'xor':  71,
        'nop': 192,
        'jeq': 193,
        'jlt': 194,
        'jle': 195,
        'jmp': 196,
        'jne': 197,
        'jge': 198,
        'jgt': 199
    }
    program = []
    
    with open(sys.argv[1]) as fd:
        # blank lines and lines wich start with a ';' are ignored
        # instructions cannot be followed by ';'
        all_lines = [l.strip() for l in fd.readlines() if len(l.strip())]
        lines = [l for l in all_lines if l[0] != ';' and l[-1]]
        
        # extract labels and set line number
        labels = [[l[:-1], lines.index(l)] for l in lines if l[-1] == ':']
        for l in labels:
            l[1] -= labels.index(l)
        labels = dict(labels)
        
        # eliminate labels from program
        lines = [l for l in lines if l[-1] != ':']
    
    for w in lines:
        if w[:3] == 'mov':
            c = 2 << 6;
            c += int(w[5:6]) << 3
            c += int(w[8:9])
            program.append(c)
        
        # if numeric literal
        elif len([c for c in w if c not in string.digits]) == 0:
            program.append(int(w))
        
        # replace labels for literals
        elif w in labels:
            program.append(labels[w])

        else:
            program.append(assembly[w])
    
    bp = generate_bp(program, sys.argv[2])
    
    if len(sys.argv) >= 4:
        with open(sys.argv[3], 'w') as fd:
            fd.write(bp)
    else:
        print(bp)