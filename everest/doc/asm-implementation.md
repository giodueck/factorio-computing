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
- [ ] Process and remove preprocessor commands like `@rep ... @end`
- [x] Create label symbol table with line number
- [ ] Replace mnemonics with opcodes
- [ ] Replace constants with values
- [x] Report syntax errors
- [ ] Convert literals into numbers, report value errors
- [ ] Convert operands into values

### Second
- [ ] Generate start jump instruction if start is present
- [ ] Generate data section instructions
- [ ] Replace label line numbers with addresses

### Third
- [ ] Replace labels with corresponding addresses
- [ ] Report on any non-numeric symbols left
- [ ] Convert instructions with operands into machine code
- [ ] Convert machine code into blueprint
