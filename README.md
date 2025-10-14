# Memory Paging Simulator

This project simulates **memory management with paging**, including virtual and physical memory, a **page table with presence bits**, and **page replacement using the FIFO (First-In, First-Out) algorithm**.  
It allows configuration of memory sizes and virtual address sequences, displaying page–frame mappings and counting page faults.

---

##  Features

- Virtual and physical memory simulation  
- Page table with presence bits  
- FIFO page replacement algorithm  
- Page fault detection and counting  
- Clear textual output  
- Modular and extensible structure

---

##  Project Structure
```plaintext
project/
├── src/
│   ├── main.py           # Entry point
│   ├── memory.py         # Memory and page table structures
│   ├── simulator.py      # Simulation loop and FIFO
│   └── interface.py      # Output and visualization
│
├── tests/
│   ├── test_basic.py
│   └── test_fifo.py
│
├── docs/
│   ├── README.txt
│   ├── report.md
│   └── examples.txt
│
├── .gitignore
├── README.md
└── LICENSE (optional)
```

##  Getting Started

### Clone the Repository
```bash
git clone git@github.com:<USER>/<REPO>.git
cd <REPO>
```
### Run 
```
python src/main.py
```

You will be prompted for:
- Physical memory size (frames)
- Virtual memory size (pages)
- A sequence of virtual addresses (e.g. 0 1 2 3 0 1 4 0 1 2 3 4)

### Team 

- Member 1 — Memory structures & input handling
- Member 2 — FIFO algorithm & simulation loop
- Member 3 — Module integration & testing
- Member 4 — Output interface & demo setup