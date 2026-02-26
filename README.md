# Harmonia

Harmonia is an educational IDE and emulator for the ATmega328p processor, designed to simulate execution of the CS150 AVR instruction subset.

The goal of this project is to provide an interactive simulation environment where assembly programs can be written, stepped through, and observed in real time. The simulator models CPU state, registers, stack behavior, memory, and status flags according to the CS150 AVR specification.

---

## Project Goals

- Implement a virtual ATmega328p machine in Python
- Accurately model the CS150 AVR instruction subset
- Provide an interactive PyQt6-based IDE
- Allow line-by-line execution with visual state updates
- Maintain clean separation between VM logic and UI

This project is structured as a state-transition system where each instruction transforms the CPU state deterministically.

---

## Architecture

The project is divided into clear layers:

### VM Layer (`vm/`)
Contains the virtual machine implementation:
- CPU state
- Registers
- Memory
- Stack
- SREG (status register)
- Instruction decoding and execution

This layer contains no UI code.

### UI Layer (`ui/`)
PyQt6-based interface including:
- Main application window
- Editor pane
- Register and memory views
- Execution controls (step, run, halt)

The UI observes and controls the VM but does not implement machine logic.

### Assembler Layer (`assembler/`)
Future parsing and instruction handling components:
- Lexer
- Parser
- Instruction representation

---

## Repository Structure
