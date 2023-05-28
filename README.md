# Factorio Computing
Tools for creating program ROMs for my factorio CPUs. Hobby project

# Project description
`bp` contains blueprint strings and templates (butchered JSON) with '%s' placed where machine code is to be inserted.

'Overture' is the first architecture, with 8-bit instructions and a small assembly compiler. A few example
programs are included.

Compilers are run as follows:
```
python <compiler>.py <input file> <blueprint template file> <optional output file>
```
If the output file is ommitted, the resulting blueprint string is printed on `stdout`.

`string-to-json.py` is a helper program that takes an input file containing a blueprint string and outputs the JSON representation in `out.json`.

## To Do
- [ ] Add Overture blueprint string
- [x] Add more compact ROM (6-bit) blueprint
- [ ] Add features to overture-compiler
  - [ ] named constants
  - [ ] inline comments (maybe)
- [ ] Implement and add more powerful architectures
  - Features needed for compilers
    - Assembly translation
    - Label translation
    - Constant declarations
    - Macros (condense several instructions into 1 command)
    - Standalone and inline comments
- [ ] Add larger compact ROM blueprints
- [ ] Universal compiler tool
  - Option, magic number or file extension based architecture detection

# Architectures
## Overture
8-bit ISA based on the "tutorial" architecture featured in the game "Turing Complete". The ALU operations have been replaced to suit Factorio better, but all other characteristics remain mostly the same.

[This Steam guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2782647016) contains a fairly complete overview of the ISA.

This implementation differes in the calculate section, where the operations are instead (in the order presented):
- ADD
- SUB
- MUL
- DIV
- AND
- OR
- NOT
- XOR

It also does not currently include an input/output pseudo-register, although this is a potential feature to be added.