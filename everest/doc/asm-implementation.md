# Assembler Implementation

## Scope
Features not implemented due to complexity on the first version of the assembler:
- File includes
- User-defined macros
- Strings (need output first)

## Language syntax considerations
- One instruction per line
- Operations and operands separated by spaces or commas
- No casing, code can be upper, lower or mixed case
- Labels and constants may not be named the same as any reserved word

## Reserved words
### Instructions
Directly translated to machine code. Has an exact or differently named equivalent
in machine code.

- NOOP
- RESET
- MOV/S
- STR
- LDR/S
- ADD/S
- MUL/S
- AND/S
- ORR/S
- XOR/S
- SUB/S
- DIV/S
- MOD/S
- EXP/S
- LSH/S
- RSH/S
- NOT/S
- CMP
- JMP
- JEQ/NE/LT/GT/LE/GE/NG/PZ/VS/VC
- PUSH
- POP/S
- CLSP

### Built-in macros
Translated to one or more instructions, with no direct machine code equivalent.

- HALT
- INC/S
- DEC/S
- CALL
- RETURN

### Preprocessor
- CONST
- DEFINE
- INCLUDE
- REP
- END

### Sections
- DATA
- MACRO
- PROGRAM
- START

## Program Sections
Programs will be split into data and program sections, using a `.[section]` syntax.
Data and macro sections must always come before the program section. If no section is
declared, the default section is a program section.

Data is loaded into RAM at the start of the program, and load instructions will be generated to be executed before the program instructions.

If a start label is present in the program section, the first instruction of the program
section becomes a jump to this label.

## Passes
### First
- [x] Delete `;` comments
- [x] Replace `,` with space
- [x] Split lines into list of operands
- [x] Create label symbol table with addresses
- [x] Process and remove preprocessor directives `@rep ... @end`
- [x] Replace macros with instructions
- [x] Report syntax errors

### Second
- [x] Generate start jump instruction if start label is present
- [ ] Generate data section instructions
- [x] Replace constants with values
- [x] Replace labels with addresses
- [x] Convert registers into values
- [x] Report on any non-numeric symbols left
- [x] Syntax analysis on instructions and operands
- [x] Convert literals into numbers
- [x] Replace mnemonics with opcodes
- [x] Convert instructions with operands into 32-bit machine code

### Third
- [x] Convert machine code into blueprint
