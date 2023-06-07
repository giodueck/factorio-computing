# Assembly language features
## General considerations
Casing doesn't matter and whitespace will be ignored. Tokens are separated by whitespace.
One sentence per line, no line endings but for the newline character itself.

## Registers
There are 13 general-purpose registers named `R0`, `R1`, ..., `R12`.
`R13` or `SP` is the stack pointer, `R14` or `LR` is the link register, and `R15` or `PC`
is the program counter which is only writable by jump instructions.

`NIL` is a pseudo-register which is defined as `R255` and does not really exist, causing
reads from it to result in `0` and writes to it to be discarded. This can be used to get
a zero or when only the secondary effects of an instruction are desired.

Addressing a non-existent register will cause the same behavior as `NIL` but is considered
an error.

## General instruction syntax
In general, instructions will be written as
```
    instruction result operand1 operand2
```
with some variations for instructions which take less arguments, like jump or load.
Instructions should, but don't have to, be indented.

If the instruction takes a result and at least one operand, writing it like
```
    instruction operand1 operand2
```
will cause the result to be stored in `operand1`, and it cannot be an immediate value.

## Immediate values
Immediate values can be used for some instructions and are written as
```
#num
```

For example
```
#10
```

The number can also be prefixed with `0x` to be interpreted as a hexadecimal number
```
#0xBEEF
```

## Labels
Code labels are constants holding immediate values, and are written as
```
.label
```
and have to be placed in a line by themselves. The value they represent is the address
of the next instruction below the label.

Labels can be used wherever immediate values can, and are invoqued simply by their name:
```
jmp label
```

## Comments
Comments are ignored when assembling, and are denoted by `;`.
Everything that follows a `;` is discarded on assembly, and can be used on an otherwise
empty line or following an instruction.
```
; This is a comment
jmp label  ; This is another one
```

## Macros
### Constants
Constants are similar to labels in that they represent an immediate value and can be
invoqued by their name. They are declared like
```
@const name value
```

As an example:
```
@const beginning 0

jmp beginning
```

### Defines
Defines are user-defined instructions which are replaced at assembly by a sequence of
instructions, similarly to the C preprocessor.

They are written like
```
@define name a b c ...
[instruction 0]
[instruction 1]
...
@end
```
where name is the name of the define and a, b, c, ... are the operands.

As an example:
```
@define swap a b
    xor a a b
    xor b a b
    xor a a b
@end
```

### Includes
Files containing only `@const`, `@define` and other includes can be included using
```
@include "filename"
```

Macros in included files are defined for the file they are included in. This allows
for libraries of macros and constants.

### Repeat
The repeat macro repeats the instruction block in the macro, which can be more manageable
than actually copying the same instructions in the code. It is used like
```
@rep N
[instruction 0]
[instruction 1]
...
@end
```

Using `@rep 0` `...` `@end` can also be used as a multi-line comment.

Sometimes it is necessary to use different numbers for every repeat, which can be done
with the `@{s,i}` construction. Here, `s` is the start immediate, and `i` the increment
for every repeat. For example:
```
@rep 4
    add r0 r0 @{#0,#1}
@end
```

## Instructions
For all instructions, `Rd`, `Rn` and `Rm` represent registers, `imm8` and `imm16` represent
8-bit and 16-bit immediates respectively, and labels and contants.

#### The flag register
The flags register is set by instructions which have the `s` suffix. The flags are

Name | Bit | Description
-----|-----|------------
`Z`  |   0 | Result is zero
`N`  |   1 | Result is negative
`V`  |   2 | Overflow or underflow occurred

`V` is like the carry flag, but all operations are signed anyways so `C` is not needed.

### Noop
`noop`\
No operation. Skip instruction with no effects.

### Halt
`halt`\
Stop clock and halt program execution.

### Reset
`reset`\
Power cycle the computer, clearing volatile memory, registers and the program counter.

### Move/Copy
`mov[s] Rd Rn/imm16`\
Copy a value into a register.

### Load
`ldr[s] Rd Rn/imm16`\
Loads a memory address denoted by `Rn/imm16` into `Rd`.

### Store
`str Rv Rn/imm16`\
Stores the value in `Rv` into the memory address denoted by `Rn/imm16`.

### Add, Multiply, AND, OR, XOR
`<op>[s] Rd Rn Rm/imm8`\
`<op>[s] Rd Rm/imm16`

`<op>` can be one of\
`add`\
`mul`\
`and`\
`orr`\
`xor`

These operations perform the represented operation on the operands.

### Subtract, Divide, Modulo, Exponentiation, Logical Shift Left, Logical Shift Right
`<op>[s] Rd Rn Rm/imm8`\
`<op>[s] Rd Rn/imm8 Rm`\
`<op>[s] Rd Rm/imm16`

`<op>` can be one of\
`sub`\
`div`\
`mod`\
`exp`\
`shl`\
`shr`

These operations perform the represented operation on the operands. As they are not
commutative, an additional variant is available in which the first operand can be
an immediate value.

### Compare
`cmp Rn Rm/imm16`

Compares the operands and updates the flags accordingly. The same as `subs` with NIL
as the destination register.

### NOT
`not Rd Rn/imm16`\
`not Rd`\
Bitwise NOT a value.

### Jumps
`jmp Rd/imm16`\
`j<c> Rd/imm16`

Where `<c>` can be one of\
`lt` (N != V)\
`gt` (!Z & N = V)\
`le` (Z | N != V)\
`ge` (N = V)\
`eq` (Z)\
`ne` (!Z)

Jump to the instruction at the address denoted by `Rd/imm16`.\
`jmp` is an inconditional jump, whereas `<c>` is a condition which checks the flags
register. In order, they are '<', '>', '<=', '>=', '=', '!=', all signed.

### Push
`push Rn/imm16`\
Push a value to the stack. Uses and increments the `SP` register. If the stack is full
the `SP` register wraps around to the beginning and overwrites the value at that position.

### Pop
`pop Rd`\
Pop a value from the stack. Uses and decrements the `SP` register. If the stack is empty
the `SP` register wraps around on decrement, and an undefined value at that position is
returned.

### Call
`call Rd/imm16`\
Jump to the address denoted by `Rd/imm16` and store the address of the next instruction
in the `LR` register.

The registers `R0`-`R3` are free to use inside a call and are the arguments. Additional
arguments are loaded on the stack. `R4`-`R11` are variable registers and their value
must be the same on return as on call.

`R0` is also the return value of a call.

### Return
`return`\
Return from a subroutine call with the value in `R0`. The address to jump to is the one
stored in the `LR` register.

