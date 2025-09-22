from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt
from memory_manager import MemoryManager

class VirtualMemoryGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Virtual Memory Manager")
        self.setGeometry(200, 200, 800, 500)
        
        # Main layout
        self.layout = QVBoxLayout()
        
        # Title label
        self.label = QLabel("Virtual Memory Manager", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        # Dropdown for selecting the algorithm
        self.algorithm_dropdown = QComboBox(self)
        self.algorithm_dropdown.addItems(["FIFO", "LRU", "Optimal"])
        self.layout.addWidget(self.algorithm_dropdown)

        # Input field for the page reference sequence
        self.page_input = QLineEdit(self)
        self.page_input.setPlaceholderText("Enter page reference sequence (comma-separated)")
        self.layout.addWidget(self.page_input)

        # Input field for the frame size (number of frames)
        self.frame_size_input = QSpinBox(self)
        self.frame_size_input.setRange(1, 10)
        self.frame_size_input.setValue(4)
        self.layout.addWidget(self.frame_size_input)

        # Run simulation button
        self.run_button = QPushButton("Run Simulation", self)
        self.run_button.clicked.connect(self.run_simulation)
        self.layout.addWidget(self.run_button)

        # Results table
        self.result_table = QTableWidget(self)
        self.layout.addWidget(self.result_table)

        # Set the layout for the window
        self.setLayout(self.layout)

        # Memory manager instance
        self.memory_manager = MemoryManager()

    def run_simulation(self):
        # Get the selected algorithm and input values
        algorithm = self.algorithm_dropdown.currentText()
        page_sequence = self.page_input.text()
        
        # Validate input for page reference sequence
        try:
            # Split the input string into a list of integers
            page_list = [int(x.strip()) for x in page_sequence.split(",")]
            if not page_list:  # Ensure the list is not empty
                raise ValueError("Empty sequence")
        except ValueError:
            # Show an error message if the input is invalid
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid sequence of integers.")
            return

        # Get the frame size from the input field
        frame_size = self.frame_size_input.value()

        # Run the memory management simulation
        results = self.memory_manager.simulate_memory_management(algorithm, page_list, frame_size)

        # Set the table to display the results
        self.result_table.setRowCount(len(results))
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["Step", "Page", "Frames"])

        # Populate the table with results
        for i, (step, page, frames) in enumerate(results):
            self.result_table.setItem(i, 0, QTableWidgetItem(str(step)))
            self.result_table.setItem(i, 1, QTableWidgetItem(str(page)))
            self.result_table.setItem(i, 2, QTableWidgetItem(str(frames)))
