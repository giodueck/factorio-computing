# Assembly language features
## General considerations
Casing doesn't matter and whitespace will be ignored. Tokens are separated by whitespace.
One sentence per line, no line endings but for the newline character itself.

## Registers
There are 13 general-purpose registers named `R0`, `R1`, ..., `R12`.
`R13` or `SP` is the stack pointer, `R14` or `LR` is the link register, and `R15` or `PC`
is the program counter which is only writable by jump instructions.

`LR` has no special purpose in the first generation of Everest, but keeping the
return address of a subroutine call in this register simplifies the code.

`NIL` is a pseudo-register which is defined as `255` and does not really exist, causing
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

The number can also be prefixed with `0x` to be interpreted as a hexadecimal number,
or `0b` to be interpreted as a binary number
```
#0xBEEF
#0b00101010
```

## Labels
Code labels are constants holding immediate values, and are written as
```
label:
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

## Preprocessor directives
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

### User-defined Macros
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

### Include
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

## Sections
Files may be split into data and program sections, with the following syntax.
```
.data
[data section]
.program
[instructions]
```

Implicitly, the first section is assumed to be the program section, unless `.data` is specified. Data sections may only appear before any `.program` section, which itself
contains instructions or macros.

A `.macro` section may also be declared before the program section to add any user-defined
macros which can be used in the program section.

A reserved label `start:` can be used to define the entry-point of a program for cases
in which it is not the first instruction in the program section.

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

In Factorio, memory registers can hold several signals at once, meaning the signals can be
held in 3 different signals, saving several bitwise operations when using and storing them.

### Noop
`noop`\
No operation. Executing has no effects on registers or memory.

### Halt
`halt`\
Halt program execution by jumping to the same instruction, creating an infinite loop.

### Reset
`reset`\
Reset the program counter, registers and memory are kept the same since turning off power
does not clear the contents of RW memory cells.

### Move/Copy
`mov[s] Rd Rn/imm16`\
Copy a value into a register.

### Store
`str Rn Rm/imm16`\
Stores the value in `Rn` into the memory address denoted by `Rm/imm16`.

### Load
`ldr[s] Rd Rn/imm16`\
Loads a memory address denoted by `Rn/imm16` into `Rd`.

### Add, Multiply, AND, OR, XOR
`<op>[s] Rd Rn Rm/imm8`\
`<op>[s] Rd Rm/imm8`

`<op>` can be one of\
`add`\
`mul`\
`and`\
`orr`\
`xor`

These operations perform the represented operation on the operands.

### Subtract, Divide, Modulo, Exponentiation, Logical Shift Left, Logical Shift Right
`<op>[s] Rd Rn Rm/imm8`\
`<op>[s] Rd imm8 Rm`\
`<op>[s] Rd Rm/imm8`

`<op>` can be one of\
`sub`\
`div`\
`mod`\
`exp`\
`lsh`\
`rsh`

These operations perform the represented operation on the operands. As they are not
commutative, an additional variant is available in which the first operand can be
an immediate value.

### Increment, Decrement
`<op>[s] Rn`

`<op>` can be one of\
`inc`\
`dec`

These instructions increment or decrement the value in a register.

### NOT
`not[s] Rd Rn/imm8`\
`not[s] Rd`\
Bitwise NOT `Rn/imm8`, or `Rd` if omitted, and store in `Rd`.

### Compare
`cmp Rn Rm/imm8`
`cmp Rn/imm8 Rm`

Compares the operands and updates the flags accordingly. The same as `subs` with NIL
as the destination register.

### Jumps
`jmp Rn/imm16`\
`j<c> Rn/imm16`

Where `<c>` can be one of\
`eq` (Z)\
`ne` (!Z)\
`lt` (N != V)\
`gt` (!Z & N = V)\
`le` (Z & N != V)\
`ge` (N = V)\
`ng` (N)\
`pz` (!N)\
`vs` (V)\
`vc` (!V)\
`al` (always)

Jump to the instruction at the address denoted by `Rn/imm16`.\
`jmp` is an inconditional jump, whereas `<c>` is a condition which checks the flags
register. In order, they are '=', '!=', '<', '>', '<=', '>=' (all signed), negative,
positive or zero, overflow, no overflow, and always.

### Push
`push Rn/imm16`\
Push a value to the stack. Uses and increments the `SP` register. If the stack is full
the `SP` register still increments, but no more values are stored and `pop`ing will
result in a `0` result.

### Pop
`pop[s] Rd`\
Pop a value from the stack. Uses and decrements the `SP` register. If the stack is empty
the `SP` register decrements into negative values and `pop`ed values are always 0, and
`push`ing to a non-valid stack address will result in `SP` incrementing and the value
to be discarded.

### Clear SP
`clsp`\
Clears the SP register to 0. Useful in "reset" programs but not recommended for normal
operation.

### Call
`call Rd/imm16`\
Jump to the address denoted by `Rd/imm16` and store the address of the next instruction
in the `LR` register.

The registers `R0`-`R3` and `R12` are free to use inside a call and are the arguments. Additional
arguments are loaded on the stack. `R4`-`R11` are variable registers and their value
must be the same on return as on call.

`R0` is also the return value of a call.

Is implemented as a Macro, as its behavior is the same as
`add LR PC #2`
`jmp Rd/imm16`

### Return
`return`\
Return from a subroutine call with the value in `R0`. The address to jump to is the one
stored in the `LR` register.

Is implemented as a macro, as its behavior is the same as
`jmp LR`
