import sys
import csv
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QSpinBox, QMessageBox, QFileDialog, QHBoxLayout, QTextEdit, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from memory_manager import MemoryManager
from process_manager import ProcessManager

class VirtualMemoryGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virtual Memory Manager - Full Feature Edition")
        self.setGeometry(100, 100, 1400, 1000)
        self.layout = QVBoxLayout()

        self.label = QLabel("Virtual Memory Manager with Full Comparison and Advanced Features", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.label)

        self.algorithm_dropdown = QComboBox(self)
        self.algorithm_dropdown.addItems(["FIFO", "LRU", "Optimal"])
        self.page_input = QLineEdit(self)
        self.page_input.setPlaceholderText("Enter page reference sequence (e.g., 1,2,3,4)")
        self.frame_size_input = QSpinBox(self)
        self.frame_size_input.setRange(1, 10)
        self.frame_size_input.setValue(4)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Algorithm:"))
        controls.addWidget(self.algorithm_dropdown)
        controls.addWidget(QLabel("Page Sequence:"))
        controls.addWidget(self.page_input)
        controls.addWidget(QLabel("Frames:"))
        controls.addWidget(self.frame_size_input)
        self.layout.addLayout(controls)

        self.run_button = QPushButton("Run Simulation")
        self.compare_button = QPushButton("Compare All Algorithms")
        self.animate_button = QPushButton("Animate Step-by-Step")
        self.export_comparison_btn = QPushButton("Export Comparison CSV")
        self.plot_faults_btn = QPushButton("Show Fault Comparison Chart")
        self.import_sequence_btn = QPushButton("Import Sequence from CSV")
        self.export_chart_btn = QPushButton("Export Chart as PNG")
        self.random_sequence_btn = QPushButton("Generate Random Sequence")
        self.clear_button = QPushButton("Clear All")

        buttons = [self.run_button, self.compare_button, self.animate_button, self.export_comparison_btn,
                   self.plot_faults_btn, self.import_sequence_btn, self.export_chart_btn,
                   self.random_sequence_btn, self.clear_button]

        for btn in buttons:
            btn.setMinimumWidth(160)

        action_layout = QHBoxLayout()
        for btn in buttons:
            action_layout.addWidget(btn)
        self.layout.addLayout(action_layout)

        self.page_fault_label = QLabel("Total Page Faults: 0 (0%)")
        self.page_fault_label.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.page_fault_label)

        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Step", "Page", "Frames", "Page Fault"])
        self.layout.addWidget(self.result_table)

        self.memory_grid = QGridLayout()
        self.memory_frame_label = QLabel("Memory Frame Visualizer")
        self.layout.addWidget(self.memory_frame_label)

        self.memory_widget = QWidget()
        self.memory_widget.setLayout(self.memory_grid)
        self.layout.addWidget(self.memory_widget)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.log_label = QLabel("Simulation Log:")
        self.layout.addWidget(self.log_label)
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.layout.addWidget(self.log_console)

        self.memory_manager = MemoryManager()
        self.process_manager = ProcessManager()
        self.setLayout(self.layout)
        self.last_simulation_results = []
        self.animation_step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.play_next_step)

        self.run_button.clicked.connect(self.run_simulation)
        self.compare_button.clicked.connect(self.compare_algorithms)
        self.animate_button.clicked.connect(self.animate_simulation)
        self.export_comparison_btn.clicked.connect(self.export_comparison_csv)
        self.plot_faults_btn.clicked.connect(self.plot_fault_bar_graph)
        self.import_sequence_btn.clicked.connect(self.import_sequence)
        self.export_chart_btn.clicked.connect(self.export_chart_png)
        self.random_sequence_btn.clicked.connect(self.generate_random_sequence)
        self.clear_button.clicked.connect(self.clear_all)

    def run_simulation(self):
        algorithm = self.algorithm_dropdown.currentText()
        page_sequence = self.page_input.text().strip()
        try:
            page_list = [int(x.strip()) for x in page_sequence.split(",") if x.strip().isdigit()]
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter a valid sequence.")
            return

        frame_size = self.frame_size_input.value()
        results = self.memory_manager.simulate_memory_management(algorithm, page_list, frame_size)
        self.last_simulation_results = results
        self.populate_table(results)
        self.update_memory_grid(results)
        self.update_log(results)
        self.plot_graph(results)

        total_faults = sum(1 for r in results if r["page_fault"] == "Yes")
        fault_rate = (total_faults / len(results)) * 100
        self.page_fault_label.setText(f"Total Page Faults: {total_faults} ({fault_rate:.1f}%)")

    def populate_table(self, results):
        self.result_table.setRowCount(len(results))
        for i, result in enumerate(results):
            self.result_table.setItem(i, 0, QTableWidgetItem(str(result["step"])))
            self.result_table.setItem(i, 1, QTableWidgetItem(str(result["page"])))
            self.result_table.setItem(i, 2, QTableWidgetItem(", ".join(map(str, result["frames"]))))
            pf_item = QTableWidgetItem(result["page_fault"])
            if result["page_fault"] == "Yes":
                pf_item.setBackground(Qt.GlobalColor.red)
            self.result_table.setItem(i, 3, pf_item)

    def update_memory_grid(self, results, step=None):
        for i in reversed(range(self.memory_grid.count())):
            self.memory_grid.itemAt(i).widget().deleteLater()
        if not results:
            return
        frames = results[step]["frames"] if step is not None else results[-1]["frames"]
        for i, page in enumerate(frames):
            frame_box = QLabel(str(page))
            frame_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            frame_box.setStyleSheet("background-color: lightgreen; border: 1px solid black; padding: 8px;")
            self.memory_grid.addWidget(frame_box, 0, i)

    def update_log(self, results):
        self.log_console.clear()
        for r in results:
            self.log_console.append(f"Step {r['step']}: Page {r['page']} → Frames: {r['frames']} → Page Fault: {r['page_fault']}")

    def plot_graph(self, results):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        steps = [r["step"] for r in results]
        pages = [r["page"] for r in results]
        ax.plot(steps, pages, marker='o', linestyle='-', color='blue', label=self.algorithm_dropdown.currentText())
        ax.set_title("Page Reference String Processing")
        ax.set_xlabel("Step")
        ax.set_ylabel("Page Number")
        ax.legend()
        ax.grid(True)
        self.canvas.draw()

    def animate_simulation(self):
        self.animation_step = 0
        if not self.last_simulation_results:
            QMessageBox.warning(self, "No Simulation", "Run a simulation first.")
            return
        self.timer.start(800)

    def play_next_step(self):
        if self.animation_step < len(self.last_simulation_results):
            step_data = self.last_simulation_results[self.animation_step]
            self.update_memory_grid(self.last_simulation_results, step=self.animation_step)
            self.log_console.append(f"Step {step_data['step']}: Page {step_data['page']} → Frames: {step_data['frames']} → Page Fault: {step_data['page_fault']}")
            self.animation_step += 1
        else:
            self.timer.stop()

    def compare_algorithms(self):
        try:
            page_list = [int(x.strip()) for x in self.page_input.text().strip().split(",") if x.strip().isdigit()]
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter a valid sequence.")
            return
        frame_size = self.frame_size_input.value()
        all_results = self.memory_manager.compare_all_algorithms(page_list, frame_size)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        for algo, results in all_results.items():
            steps = [r["step"] for r in results]
            pages = [r["page"] for r in results]
            ax.plot(steps, pages, marker='o', linestyle='-', label=algo)
        ax.set_title("Comparison of Algorithms")
        ax.set_xlabel("Step")
        ax.set_ylabel("Page")
        ax.legend()
        ax.grid(True)
        self.canvas.draw()

    def export_comparison_csv(self):
        try:
            page_list = [int(x.strip()) for x in self.page_input.text().strip().split(",") if x.strip().isdigit()]
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter a valid sequence.")
            return
        frame_size = self.frame_size_input.value()
        all_results = self.memory_manager.compare_all_algorithms(page_list, frame_size)
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
        if path:
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Algorithm", "Step", "Page", "Frames", "Page Fault"])
                for algo, results in all_results.items():
                    for r in results:
                        writer.writerow([algo, r["step"], r["page"], " ".join(map(str, r["frames"])), r["page_fault"]])

    def plot_fault_bar_graph(self):
        try:
            page_list = [int(x.strip()) for x in self.page_input.text().strip().split(",") if x.strip().isdigit()]
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter a valid sequence.")
            return
        frame_size = self.frame_size_input.value()
        all_results = self.memory_manager.compare_all_algorithms(page_list, frame_size)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        algorithms = []
        faults = []
        for algo, results in all_results.items():
            algorithms.append(algo)
            faults.append(sum(1 for r in results if r["page_fault"] == "Yes"))
        ax.bar(algorithms, faults)
        ax.set_title("Page Fault Comparison")
        ax.set_ylabel("Faults")
        self.canvas.draw()

    def import_sequence(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Sequence", "", "CSV Files (*.csv)")
        if path:
            with open(path, 'r') as f:
                seq = f.readline().strip()
                self.page_input.setText(seq)

    def export_chart_png(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Chart", "", "PNG Files (*.png)")
        if path:
            self.figure.savefig(path)

    def generate_random_sequence(self):
        sequence = [str(random.randint(0, 9)) for _ in range(15)]
        self.page_input.setText(",".join(sequence))

    def clear_all(self):
        self.result_table.setRowCount(0)
        self.page_input.clear()
        self.log_console.clear()
        self.page_fault_label.setText("Total Page Faults: 0 (0%)")
        self.last_simulation_results = []
        self.update_memory_grid([])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VirtualMemoryGUI()
    window.show()
    sys.exit(app.exec())

