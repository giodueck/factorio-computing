# Assembly language features
## General considerations
Casing doesn't matter and whitespace will be ignored. Tokens are separated by whitespace.
One sentence per line, newline character for line endings.

## Registers
There are 12 general-purpose registers named `R0`, `R1`, ..., `R11`.
`AR` is the address register used for load and store operations, `SP` is the stack
pointer, `LR` is the link register, and `PC` is the program counter which
is only writable by jump instructions.

`NIL` is a pseudo-register which is defined as `255` and does not really exist, causing
reads from it to result in `0` and writes to it to be discarded. This can be used to get
a zero or when only the secondary effects of an instruction are desired.

Addressing a non-existent register will cause the same behavior as `NIL` but is considered
an error.

## Memory layout
Program instructions and data are all stored in RAM. The layout is as follows:

0. `jmp start` instruction, automatically added to skip data section.
1. Declared data section
2. Program section, instructions
3. Free memory

The free memory space starting address depends on the previous sections, and is pointed to by
the constant `ram_start`. A program can then work with offsets from this address.

Memory is in no way protected, self modifying code, buffer overflows, and executing any memory
address are all possible and are the responsibility of the programmer.

## General instruction syntax
In general, instructions will be written as
```
    instruction result operand1 operand2
```
with some variations for instructions which take less arguments, like jump or load.

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

The `start` label is the entry point for a program, and by default is the first instruction.

## Comments
Comments are ignored when assembling, and are denoted by `;`.
Everything that follows a `;` is discarded on assembly, and can be used on an otherwise
empty line or following an instruction.
```
; This is a comment
jmp label  ; This is another one
```

### Program Label and description
The blueprint label and description fields will be filled with text from the program comments
according to the following rules:
- The first comment to start with `;;` is taken to be the label
- All comments and empty lines before the start of any section (e.g. an instruction), except
    for the label, are taken to be the description of the program

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
**TO-DO**
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
**TO-DO**
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

Implicitly, the first section is assumed to be the program section, unless `.data` is specified. Data
sections may only appear before any `.program` section, which itself contains instructions or macros.

<!-- A `.macro` section may also be declared before the program section to add any user-defined
macros which can be used in the program section. -->

A reserved label `start:` can be used to define the entry-point of a program for cases
in which it is not the first instruction in the program section.

## Data section
The data section may contain named and initialized memory blocks. Unlike with instructions, all arguments
must be numeric or `@const`ants and do not need to be prefixed with `#`. They can be in decimal, binary
or hexadecimal using no prefix or `0b` and `0x` respectively.

```
identifier1 [initialization]
identifier2 [initialization]
```

Initialization can be done in one of two ways, and the size of the memory block allocated is dependent on
initialization.

### Explicit initialization
The values can be listed individually separated by commas or spaces. The number of items defines the size of
the memory block.

```
identifier1 42
identifier2 0xf00d, 0xbeef, 0b101010
```

### Uniform initialization
To define a sequence of the same repeating number a more compact way to write it is using the `times` keyword.
Here the first number is the size of the allocation, and the second is the value.

```
identifier times 5 0
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

In Factorio, memory registers can hold several signals at once, meaning the signals can be
held in 3 different signals, saving several bitwise operations when using and storing them.

### Noop
`noop`\
No operation. Executing has no effects on registers or memory.

In machine code, this instruction is translated to a jump with the condition `never`.

### Halt
`halt`\
Halt program execution by jumping to the same instruction, creating an infinite loop.

### Reset
`reset`\
Reset the program counter and stack pointer, stack and memory are kept the same since turning off power
does not clear the contents of RW memory cells.

Is implemented as a Macro, as its behavior is the same as
`xor SP SP`
`jmp #0`

### Move/Copy
`mov[s] Rd Rn/imm8`\
Copy a value into a register.

This instruction is translated to\
`add[s] Rd NIL Rn/imm8`

For 16-bit immediates:\
`mov16 Rd imm16`

Which is translated to\
`push imm16`\
`pop Rd`

For bigger immediates, the instruction can be built using\
`mov16 Rd imm16H`\
`bcat[s] Rd imm16L`\
where `imm16H` and `imm16L` are the high and low halfwords respectively.

### Store
`store Rn/imm16`\
Stores the value in `Rn/imm16` into the memory address stored in `AR`.

### Load
`load Rd`\
Loads the word stored in the memory address in `AR` into `Rd`.

### Add, Multiply, AND, OR, XOR, Subtract, Divide, Modulo, Exponentiation, Logical Shift Left, Arithmetic Shift Right, Byte concatenate, Halfword concatenate
`<op>[s] Rd Rn Rm/imm8`\
`<op>[s] Rd Rm/imm8`

`<op>` can be one of\
`add`\
`mul`\
`and`\
`orr`\
`xor`\
`sub`\
`div`\
`mod`\
`exp`\
`lsh`\
`rsh`\
`bcat`\
`hcat`

These operations perform the represented operation on the operands.

### Increment, Decrement
`<op>[s] Rn`

`<op>` can be one of\
`inc`\
`dec`

These instructions increment or decrement the value in a register.
They are respectively translated to either\
`add[s] Rn #1`\
or\
`sub[s] Rn #1`

### NOT
`not[s] Rd Rn`\
`not[s] Rd`\
Bitwise NOT `Rn`, or `Rd` if omitted, and store in `Rd`.

### Compare
`cmp Rn Rm/imm8`

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
`pop Rd`\
Pop a value from the stack. Uses and decrements the `SP` register. If the stack is empty
the `SP` register decrements into negative values and `pop`ed values are always 0, and
`push`ing to a non-valid stack address will result in `SP` incrementing and the value
to be discarded.

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
