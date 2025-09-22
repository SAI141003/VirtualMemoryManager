Virtual Memory Manager

A lightweight educational tool that demonstrates how operating systems manage memory through paging and page-replacement algorithms.
It provides an interactive GUI for exploring memory allocation, page faults, and process management.


🚀 Features
	•	Paging Simulation – Visualize how logical addresses are translated to physical frames.
	•	Page Replacement – Supports FIFO, LRU, and Optimal algorithms with step-by-step display.
	•	Process Manager – Add/remove processes and watch their memory usage in real time.
	•	Interactive GUI – Clean interface built with Python for better understanding of memory concepts.
	•	Statistics Dashboard – Track hits, misses, and fault rates for each algorithm.

  Project Structure

VirtualMemoryManager/
│
├── main.py                # Entry point
├── memory_manager.py      # Core paging & frame allocation logic
├── page_replacement.py    # FIFO, LRU, Optimal algorithms
├── process_manager.py     # Handles process creation & allocation
├── gui.py                 # GUI controller
├── ui_design.py           # UI layout / widgets
├── csv.csv                # Sample input for testing
└── README.md
