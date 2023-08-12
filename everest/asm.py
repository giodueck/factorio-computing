import base64
import zlib
import sys
import string

def rom_size(name: str) -> int:
    if name[:4] != 'ROM-':
        print('Template name must begin with "ROM-" followed by an integer number of bits.')
        exit(1)
    s = name[4:]
    a = 0
    for c in s:
        if c in [str(i) for i in range(10)]:
            a = a * 10 + int(c)
    return a

def generate_bp(program: list[int], template: str) -> str:
    length = 1 << rom_size(sys.argv[2])
    while len(program) < length:
        program.append(0)

    with open(template) as fd:
        t = fd.read()

    for i in range(length):
        t = t.replace('%s', str(program[i]), 1)

    z = zlib.compress(bytes(t, 'utf-8'), level=9)
    b = '0' + str(base64.b64encode(z))[2:-1]

    return b


## Opcodes
opcodes = {
    'NOOP': 0,
    'RESET': 2, 
    'MOV': [3, 4], 
    'MOVS': [5, 6],
    'STR': [7, 8], 
    'LDR': [9, 10],
    'LDRS': [11, 12],
    'ADD': [15, 20], 
    'MUL': [16, 21], 
    'AND': [17, 22], 
    'ORR': [18, 23], 
    'XOR': [19, 24], 
    'SUB': [25, 31, 37], 
    'DIV': [26, 32, 38], 
    'MOD': [27, 33, 39], 
    'EXP': [28, 34, 40], 
    'LSH': [29, 35, 41], 
    'RSH': [30, 36, 42], 
    'NOT': [43, 44], 
    'NOTS': [45, 46],
    'ADDS': [47, 52],
    'MULS': [48, 53],
    'ANDS': [49, 54],
    'ORRS': [50, 55],
    'XORS': [51, 56],
    'SUBS': [57, 63, 69], 
    'DIVS': [58, 64, 70], 
    'MODS': [59, 65, 71], 
    'EXPS': [60, 66, 72], 
    'LSHS': [61, 67, 73], 
    'RSHS': [62, 68, 74],
    'JMP': [75, 76],
    'JEQ': [77, 87], 
    'JNE': [78, 88], 
    'JLT': [79, 89], 
    'JGT': [80, 90], 
    'JLE': [81, 91], 
    'JGE': [82, 92], 
    'JNG': [83, 93], 
    'JPZ': [84, 94], 
    'JVS': [85, 95], 
    'JVC': [86, 96], 
    'PUSH': [97, 98],
    'POP': 99, 
    'POPS': 100, 
    'CLSP': 101
}

builtin_macros = [
    'HALT',
    'CMP',
    'INC',
    'INCS',
    'DEC',
    'DECS',
    'CALL',
    'RETURN'
]

preprocessor = [
    'CONST',
    'DEFINE',
    'INCLUDE',
    'REP',
    'END'
]

sections = [
    'DATA',
    'MACRO',
    'PROGRAM'
]

registers = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'SP': 13,
    'LR': 14,
    'PC': 15
}

lines = []
lineinfo = []
lineaddr = []
labels = {}
consts = {}
errors = 0
program_reached = 0
curr_section = 0
repeat = 0
repeat_line = 0
code = []
machine_code = []


def syntax_error(msg: str, i: int):
    print(f'Syntax error on line {i}: {msg}')
    global errors; errors += 1

def lexical_error(msg: str, i: int):
    print(f'Unknown token on line {i}: {msg}')
    global errors; errors += 1
    
def instr_to_machine_code(c: list):
    return c

def macro_to_instr(c: list):
    o = c[0]
    out = []
    
    if o == 'HALT':
        out.append(['JMP', 'PC'])
    elif o == 'CMP':
        out.append(c)
        out[-1][0] = 'SUBS'
    elif o == 'INC':
        out.append(['ADD', c[1], c[1], '#1'])
    elif o == 'INCS':
        out.append(['ADDS', c[1], c[1], '#1'])
    elif o == 'DEC':
        out.append(['SUB', c[1], c[1], '#1'])
    elif o == 'DECS':
        out.append(['SUBS', c[1], c[1], '#1'])
    elif o == 'CALL':
        out.append(['ADD', 'LR', 'PC', '#2'])
        out.append(['JMP', c[1]])
    elif o == 'RETURN':
        out.append(['JMP', 'LR'])
    
    return out

def interpret_instr(c: list, i: int):
    # Instructions
    if c[0] in opcodes:
        if curr_section != 0:
            syntax_error('instruction not allowed outside ".PROGRAM" section', lineinfo[i])
            return
        machine_code.append(instr_to_machine_code(c))
    
    # Built-in macro instructions
    elif c[0] in builtin_macros:
        if curr_section != 0:
            syntax_error('instruction not allowed outside ".PROGRAM" section', lineinfo[i])
            return
        new_code = macro_to_instr(c)
        for d in new_code:
            machine_code.append(instr_to_machine_code(d))

    else:
        syntax_error(f'unkown instruction "{c[0]}"')

def repeat_block(c: list, i: int):
    if len(c) < 2:
        syntax_error(f'"{c[0]}" must be followed by a non-negative integer', lineinfo[i])
        return
    if len(c) > 2:
        syntax_error(f'"{c[0]}" takes only one non-negative integer as an argument', lineinfo[i])
        return
    
    try:
        n = int(c[1])
        if n < 0:
            raise ValueError
    except:
        syntax_error(f'"{c[0]}" must be followed by a non-negative integer', lineinfo[i])
        return
    
    # Get code until END is found
    r = []
    ended = 0
    counters = []
    for j in range(i + 1, len(code)):
        if code[j][0] == '@END':
            ended = 1
            break
        
        # @{s, i} blocks are counters: s=start value, i=increment value
        len_counters = -1
        while len_counters < len(counters):
            len_counters = len(counters)
            
            for k, a in enumerate(code[j]):
                k_ = 0
                s_, i_ = 0, 0
                if a.startswith('@{'):
                    if len(a) > 2:
                        s_ = int(a[2:])
                    else:
                        k_ += 1
                        s_ = int(code[j][k + k_])
                    k_ += 1
                
                    if code[j][k + k_].endswith('}'):
                        i_ = int(code[j][k + k_][:-1])
                    else:
                        i_ = int(code[j][k + k_])
                        k_ += 1
                    
                    counters.append((s_, i_))
            
                    # remove counter block and replace with string format ('{i}') placeholder
                    while k_ >= 0:
                        code[j].pop(k + k_)
                        k_ -= 1
                    code[j].insert(k, f'({len(counters) - 1})')

        r.append(code[j])
        
    if not ended:
        # This error will be detected while parsing the rest of the code inside the first pass
        return
    
    for j in range(n):
        ri = [e.copy() for e in r]
        for k, rk in enumerate(r):
            for l, a in enumerate(rk):
                if a.startswith('(') and a.endswith(')'):
                    index = int(a[1:-1])
                    ri[k][l] = '#' + str(counters[index][0])
                    updated_ctr = (counters[index][0] + counters[index][1], counters[index][1])
                    counters.pop(index)
                    counters.insert(index, updated_ctr)

        for k, rk in enumerate(ri):
            interpret_instr(rk, k)

    return

if __name__ == '__main__':
    # arg 0 = program name
    # arg 1 = input
    # arg 2 = template ('ROM-N[.]*'), where N is a decimal number of bits denoting address range
    # arg 3 = output filename (default print to stdout)
    
    if len(sys.argv) not in (3, 4):
        print(f"Usage: python {sys.argv[0]} <input_file> <template_file> <optional_ouput_file>")
        exit(1)
    
    ## First pass
    # Read source lines into lines array
    with open(sys.argv[1], 'r') as fd:
        lines = [l.strip().upper() for l in fd.readlines()]
        lineinfo = [i + 1 for i in range(len(lines))]
    
    # Strip comments and empty lines, replace commas with spaces
    lines = [line.split(';')[0].replace(',', ' ').strip() for line in lines]
    
    indices = [i for i, l in enumerate(lines) if len(l) == 0]
    while len(indices):
        lineinfo.pop(indices[-1])
        lines.pop(indices[-1])
        indices.pop()
    
    # Split lines into tokens
    code = [l.split() for l in lines]
    
    # Identify tokens and translate
    errors = 0
    for i, c in enumerate(code):
        
        # REP..END blocks are interpreted when REP is found, discard instructions until END is found
        if repeat:
            if c[0] == '@END':
                repeat = 0
            continue
        
        # Preprocessor directives
        if c[0][0] == '@' and c[0][1:] in preprocessor:
            if c[0] == '@REP':
                repeat = 1
                repeat_line = lineinfo[i]
                if curr_section != 0:
                    syntax_error(f'"{c[0]}" only allowed in ".PROGRAM" section', lineinfo[i])
                    continue
                repeat_block(c, i)
                continue
            elif c[0] == '@END':
                syntax_error(f'"{c[0]}" without a corresponding "@REP"', lineinfo[i])
                continue
            
            if curr_section != 1:
                syntax_error('preprocessor directives not allowed outside ".MACRO" section, except "@REP"', lineinfo[i])
                continue
            if c[0] == '@CONST':
                if len(c) != 3:
                    syntax_error(f'"{c[0]}" must be followed by an identifier and a value', lineinfo[i])
                    continue
                else:
                    if c[1] in opcodes or c[1] in builtin_macros or c[1] in preprocessor or c[1] in sections or c[1] in registers:
                        syntax_error(f'"{c[0]}" name may not be a reserved word', lineinfo[i])
                        continue
                    elif c[1] in consts:
                        syntax_error(f'"{c[0]}" "{c[1]}" defined multiple times', lineinfo[i])
                    consts[c[1]] = c[2]
            elif c[0][1:] in ['DEFINE', 'INCLUDE']:
                syntax_error(f'"{c[0]}" is reserved but has not been implemented', lineinfo[i])
                continue
            else:
                syntax_error(f'unkown preprocessor directive "{c[0]}"')
                continue
            
        # Sections
        elif c[0][0] == '.' and c[0][1:] in sections:
            if program_reached:
                syntax_error('sections cannot be declared after ".PROGRAM" section begins', lineinfo[i])
                continue
            elif c[0][1:] == 'PROGRAM':
                program_reached = 1
                curr_section = 0
            elif c[0][1:] == 'MACRO':
                curr_section = 1
            elif c[0][1:] == 'DATA':
                curr_section = 2
                syntax_error(f'"{c[0]}" has not been implemented', lineinfo[i])
                continue
            else:
                syntax_error(f'unkown section "{c[0]}"')
                continue
        
        # Labels
        elif c[0][-1] == ':' or len(c) > 1 and c[1] == ':':
            l = c[0].strip(':')
            if l in opcodes or l in builtin_macros or l in preprocessor or l in sections or l in registers:
                syntax_error(f'label may not be a reserved word', lineinfo[i])
                continue
            elif l in consts:
                syntax_error(f'"{l}" was already defined as a "@CONST"', lineinfo[i])
                continue
            elif l in labels:
                syntax_error(f'"{l}" defined multiple times', lineinfo[i])
                continue
            
            labels[l] = len(machine_code)
        
        # Instructions and Built-in macros
        elif c[0] in opcodes or c[0] in builtin_macros:
            interpret_instr(c, i)
            program_reached = 1
            
        # Everything not picked up is a lexical error
        else:
            lexical_error(c[0], lineinfo[i])
    
    if repeat:
        syntax_error('"@REP" without a corresponding "@END"', repeat_line)
    
    for c in machine_code:
        print(c)
    print()
    print(labels)
    print(consts)
    
    ## Second pass
    
    
    ## Third pass
    
    ## Output
    if errors:
        print(f'{errors} error{"s" if errors > 1 else ""} detected')
        exit(0)
    exit(0)
    
    bp = generate_bp(machine_code, sys.argv[2])
    
    if len(sys.argv) == 4:
        with open(sys.argv[3], 'w') as fd:
            fd.write(bp)
    else:
        print(bp)