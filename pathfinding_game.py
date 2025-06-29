import sys
import time
import heapq
from typing import List, Tuple, Optional, Set
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QComboBox, 
                               QSpinBox, QGridLayout, QFrame, QMessageBox,
                               QSlider, QGroupBox, QCheckBox)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPixmap, QIcon

class Node:
    """Node class for search algorithms"""
    def __init__(self, state: Tuple[int, int], parent=None, action=None, g_cost=0, h_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g_cost = g_cost  # Cost from start to current node
        self.h_cost = h_cost  # Heuristic cost from current node to goal
        self.f_cost = g_cost + h_cost  # Total cost (f = g + h)

    def __lt__(self, other):
        return self.f_cost < other.f_cost

class SearchWorker(QThread):
    """Worker thread for running search algorithms"""
    progress = Signal(tuple, str)  # (position, color)
    finished = Signal(list, int)   # (path, explored_count)
    error = Signal(str)

    def __init__(self, grid, start_pos, goal, algorithm):
        super().__init__()
        self.grid = grid
        self.start_pos = start_pos
        self.goal = goal
        self.algorithm = algorithm
        self.running = True

    def stop(self):
        self.running = False

    def manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_neighbors(self, pos):
        """Get valid neighbors of a position"""
        row, col = pos
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < len(self.grid) and 
                0 <= new_col < len(self.grid[0]) and 
                not self.grid[new_row][new_col]):
                neighbors.append((new_row, new_col))
        return neighbors

    def greedy_best_first_search(self):
        """Greedy Best-First Search implementation"""
        start_node = Node(state=self.start_pos, h_cost=self.manhattan_distance(self.start_pos, self.goal))
        frontier = [start_node]
        explored = set()
        explored_count = 0

        while frontier and self.running:
            current = heapq.heappop(frontier)
            
            if current.state in explored:
                continue
                
            explored.add(current.state)
            explored_count += 1
            
            # Emit progress signal for visualization
            self.progress.emit(current.state, "explored")
            time.sleep(0.05)  # Slow down for visualization
            
            if current.state == self.goal:
                # Reconstruct path
                path = []
                node = current
                while node:
                    path.append(node.state)
                    node = node.parent
                return path[::-1], explored_count
            
            for neighbor_pos in self.get_neighbors(current.state):
                if neighbor_pos not in explored:
                    h_cost = self.manhattan_distance(neighbor_pos, self.goal)
                    neighbor = Node(state=neighbor_pos, parent=current, h_cost=h_cost)
                    heapq.heappush(frontier, neighbor)
        
        return None, explored_count

    def a_star_search(self):
        """A* Search implementation"""
        start_node = Node(state=self.start_pos, g_cost=0, h_cost=self.manhattan_distance(self.start_pos, self.goal))
        frontier = [start_node]
        explored = set()
        explored_count = 0

        while frontier and self.running:
            current = heapq.heappop(frontier)
            
            if current.state in explored:
                continue
                
            explored.add(current.state)
            explored_count += 1
            
            # Emit progress signal for visualization
            self.progress.emit(current.state, "explored")
            time.sleep(0.05)  # Slow down for visualization
            
            if current.state == self.goal:
                # Reconstruct path
                path = []
                node = current
                while node:
                    path.append(node.state)
                    node = node.parent
                return path[::-1], explored_count
            
            for neighbor_pos in self.get_neighbors(current.state):
                if neighbor_pos not in explored:
                    g_cost = current.g_cost + 1  # Cost to move to neighbor
                    h_cost = self.manhattan_distance(neighbor_pos, self.goal)
                    neighbor = Node(state=neighbor_pos, parent=current, g_cost=g_cost, h_cost=h_cost)
                    heapq.heappush(frontier, neighbor)
        
        return None, explored_count

    def run(self):
        """Run the selected search algorithm"""
        try:
            if self.algorithm == "Greedy Best-First Search":
                path, explored_count = self.greedy_best_first_search()
            elif self.algorithm == "A* Search":
                path, explored_count = self.a_star_search()
            else:
                self.error.emit("Unknown algorithm")
                return
            
            if path:
                # Emit path visualization
                for pos in path:
                    if self.running:
                        self.progress.emit(pos, "path")
                        time.sleep(0.1)
                
            self.finished.emit(path if path else [], explored_count)
            
        except Exception as e:
            self.error.emit(str(e))

class GridCell(QFrame):
    """Individual grid cell widget"""
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.cell_type = "empty"  # empty, wall, start, goal, explored, path
        self.setFixedSize(30, 30)
        self.setFrameStyle(QFrame.Shape.Box)
        self.update_appearance()

    def update_appearance(self):
        """Update cell appearance based on type"""
        colors = {
            "empty": QColor(255, 255, 255),      # White
            "wall": QColor(64, 64, 64),          # Dark gray
            "start": QColor(255, 0, 0),          # Red
            "goal": QColor(0, 255, 0),           # Green
            "explored": QColor(255, 182, 193),   # Light pink
            "path": QColor(255, 255, 0),         # Yellow
            "frontier": QColor(173, 216, 230)    # Light blue
        }
        
        self.setStyleSheet(f"background-color: {colors[self.cell_type].name()}; border: 1px solid #ccc;")

    def set_type(self, cell_type):
        """Set cell type and update appearance"""
        self.cell_type = cell_type
        self.update_appearance()

class PathfindingGame(QMainWindow):
    """Main game window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pathfinding Search Visualization")
        self.setGeometry(100, 100, 1200, 800)
        
        # Game state
        self.grid_size = 20
        self.grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.start_pos = None
        self.goal_pos = None
        self.cells = []
        self.search_worker = None
        self.is_searching = False
        
        self.init_ui()
        self.create_grid()

    def init_ui(self):
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Title
        title = QLabel("Pathfinding Search Visualization")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(title)
        
        # Grid size control
        size_group = QGroupBox("Grid Size")
        size_layout = QHBoxLayout(size_group)
        size_layout.addWidget(QLabel("Size:"))
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(10, 50)
        self.size_spinbox.setValue(self.grid_size)
        self.size_spinbox.valueChanged.connect(self.change_grid_size)
        size_layout.addWidget(self.size_spinbox)
        left_layout.addWidget(size_group)
        
        # Algorithm selection
        algo_group = QGroupBox("Search Algorithm")
        algo_layout = QVBoxLayout(algo_group)
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Greedy Best-First Search", "A* Search"])
        algo_layout.addWidget(self.algo_combo)
        left_layout.addWidget(algo_group)
        
        # Control buttons
        control_group = QGroupBox("Controls")
        control_layout = QVBoxLayout(control_group)
        
        self.start_btn = QPushButton("Start Search")
        self.start_btn.clicked.connect(self.start_search)
        control_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop Search")
        self.stop_btn.clicked.connect(self.stop_search)
        self.stop_btn.setEnabled(False)
        control_layout.addWidget(self.stop_btn)
        
        self.clear_btn = QPushButton("Clear Grid")
        self.clear_btn.clicked.connect(self.clear_grid)
        control_layout.addWidget(self.clear_btn)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_grid)
        control_layout.addWidget(self.reset_btn)
        
        left_layout.addWidget(control_group)
        
        # Instructions
        instructions_group = QGroupBox("Instructions")
        instructions_layout = QVBoxLayout(instructions_group)
        instructions = QLabel(
            "1. Click cells to place walls\n"
            "2. Right-click to place start (red)\n"
            "3. Right-click again to place goal (green)\n"
            "4. Select algorithm and click Start Search\n"
            "5. Watch the visualization!"
        )
        instructions.setWordWrap(True)
        instructions_layout.addWidget(instructions)
        left_layout.addWidget(instructions_group)
        
        # Legend
        legend_group = QGroupBox("Legend")
        legend_layout = QVBoxLayout(legend_group)
        legend_items = [
            ("White", "Empty"),
            ("Gray", "Wall"),
            ("Red", "Start"),
            ("Green", "Goal"),
            ("Pink", "Explored"),
            ("Yellow", "Path")
        ]
        for color, desc in legend_items:
            legend_layout.addWidget(QLabel(f"• {color}: {desc}"))
        left_layout.addWidget(legend_group)
        
        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.status_label)
        
        left_layout.addStretch()
        
        # Right panel - Grid
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Grid title
        grid_title = QLabel("Search Grid")
        grid_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        grid_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(grid_title)
        
        # Grid widget
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(1)
        right_layout.addWidget(self.grid_widget)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 3)

    def create_grid(self):
        """Create the grid of cells"""
        # Clear existing grid
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)
        
        self.cells = []
        self.grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Create new grid
        for row in range(self.grid_size):
            row_cells = []
            for col in range(self.grid_size):
                cell = GridCell(row, col)
                cell.mousePressEvent = lambda event, r=row, c=col: self.cell_clicked(r, c, event)
                self.grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def change_grid_size(self, new_size):
        """Change the grid size"""
        self.grid_size = new_size
        self.create_grid()
        self.start_pos = None
        self.goal_pos = None
        self.status_label.setText("Grid size changed")

    def cell_clicked(self, row, col, event):
        """Handle cell click events"""
        if self.is_searching:
            return
            
        if event.button() == Qt.MouseButton.LeftButton:
            # Toggle wall
            if (row, col) != self.start_pos and (row, col) != self.goal_pos:
                self.grid[row][col] = not self.grid[row][col]
                cell_type = "wall" if self.grid[row][col] else "empty"
                self.cells[row][col].set_type(cell_type)
        elif event.button() == Qt.MouseButton.RightButton:
            # Place start/goal
            if self.start_pos is None:
                # Place start
                if self.cells[row][col].cell_type != "wall":
                    self.start_pos = (row, col)
                    self.cells[row][col].set_type("start")
                    self.status_label.setText("Start placed. Right-click to place goal.")
            elif self.goal_pos is None:
                # Place goal
                if self.cells[row][col].cell_type != "wall" and (row, col) != self.start_pos:
                    self.goal_pos = (row, col)
                    self.cells[row][col].set_type("goal")
                    self.status_label.setText("Goal placed. Ready to search!")

    def start_search(self):
        """Start the search algorithm"""
        if self.start_pos is None or self.goal_pos is None:
            QMessageBox.warning(self, "Warning", "Please place both start and goal positions!")
            return
            
        if self.is_searching:
            return
            
        # Clear previous search results
        self.clear_search_results()
        
        # Start search worker
        self.is_searching = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        algorithm = self.algo_combo.currentText()
        self.status_label.setText(f"Running {algorithm}...")
        
        self.search_worker = SearchWorker(self.grid, self.start_pos, self.goal_pos, algorithm)
        self.search_worker.progress.connect(self.update_cell)
        self.search_worker.finished.connect(self.search_finished)
        self.search_worker.error.connect(self.search_error)
        self.search_worker.start()

    def stop_search(self):
        """Stop the current search"""
        if self.search_worker and self.is_searching:
            self.search_worker.stop()
            self.search_worker.wait()
            self.is_searching = False
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.status_label.setText("Search stopped")

    def update_cell(self, pos, cell_type):
        """Update cell appearance during search"""
        row, col = pos
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            # Don't overwrite start/goal
            if self.cells[row][col].cell_type not in ["start", "goal"]:
                self.cells[row][col].set_type(cell_type)

    def search_finished(self, path, explored_count):
        """Handle search completion"""
        self.is_searching = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if path:
            self.status_label.setText(f"Path found! Explored {explored_count} cells. Path length: {len(path)}")
        else:
            self.status_label.setText(f"No path found! Explored {explored_count} cells.")

    def search_error(self, error_msg):
        """Handle search errors"""
        self.is_searching = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText(f"Error: {error_msg}")
        QMessageBox.critical(self, "Error", f"Search failed: {error_msg}")

    def clear_search_results(self):
        """Clear search visualization results"""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell_type = self.cells[row][col].cell_type
                if cell_type in ["explored", "path", "frontier"]:
                    if (row, col) == self.start_pos:
                        self.cells[row][col].set_type("start")
                    elif (row, col) == self.goal_pos:
                        self.cells[row][col].set_type("goal")
                    elif self.grid[row][col]:
                        self.cells[row][col].set_type("wall")
                    else:
                        self.cells[row][col].set_type("empty")

    def clear_grid(self):
        """Clear the entire grid"""
        if self.is_searching:
            return
            
        self.grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.start_pos = None
        self.goal_pos = None
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.cells[row][col].set_type("empty")
        
        self.status_label.setText("Grid cleared")

    def reset_grid(self):
        """Reset the grid to initial state"""
        if self.is_searching:
            return
            
        self.clear_grid()
        self.status_label.setText("Grid reset")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application properties
    app.setApplicationName("Pathfinding Search Visualization")
    app.setApplicationVersion("1.0")
    
    window = PathfindingGame()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 