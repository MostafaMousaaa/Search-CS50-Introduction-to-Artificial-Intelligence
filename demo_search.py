#!/usr/bin/env python3
"""
Demo script for Greedy Best-First Search and A* Search algorithms.
This script demonstrates the algorithms on a simple maze without GUI.
"""

import heapq
import time
from typing import List, Tuple, Optional, Set

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

def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """Calculate Manhattan distance between two positions"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_neighbors(pos: Tuple[int, int], grid: List[List[bool]]) -> List[Tuple[int, int]]:
    """Get valid neighbors of a position"""
    row, col = pos
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if (0 <= new_row < len(grid) and 
            0 <= new_col < len(grid[0]) and 
            not grid[new_row][new_col]):
            neighbors.append((new_row, new_col))
    return neighbors

def greedy_best_first_search(grid: List[List[bool]], start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], int]:
    """Greedy Best-First Search implementation"""
    print("Running Greedy Best-First Search...")
    
    start_node = Node(state=start, h_cost=manhattan_distance(start, goal))
    frontier = [start_node]
    explored = set()
    explored_count = 0

    while frontier:
        current = heapq.heappop(frontier)
        
        if current.state in explored:
            continue
            
        explored.add(current.state)
        explored_count += 1
        
        print(f"Exploring: {current.state} (h={current.h_cost})")
        
        if current.state == goal:
            # Reconstruct path
            path = []
            node = current
            while node:
                path.append(node.state)
                node = node.parent
            return path[::-1], explored_count
        
        for neighbor_pos in get_neighbors(current.state, grid):
            if neighbor_pos not in explored:
                h_cost = manhattan_distance(neighbor_pos, goal)
                neighbor = Node(state=neighbor_pos, parent=current, h_cost=h_cost)
                heapq.heappush(frontier, neighbor)
    
    return None, explored_count

def a_star_search(grid: List[List[bool]], start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], int]:
    """A* Search implementation"""
    print("Running A* Search...")
    
    start_node = Node(state=start, g_cost=0, h_cost=manhattan_distance(start, goal))
    frontier = [start_node]
    explored = set()
    explored_count = 0

    while frontier:
        current = heapq.heappop(frontier)
        
        if current.state in explored:
            continue
            
        explored.add(current.state)
        explored_count += 1
        
        print(f"Exploring: {current.state} (g={current.g_cost}, h={current.h_cost}, f={current.f_cost})")
        
        if current.state == goal:
            # Reconstruct path
            path = []
            node = current
            while node:
                path.append(node.state)
                node = node.parent
            return path[::-1], explored_count
        
        for neighbor_pos in get_neighbors(current.state, grid):
            if neighbor_pos not in explored:
                g_cost = current.g_cost + 1  # Cost to move to neighbor
                h_cost = manhattan_distance(neighbor_pos, goal)
                neighbor = Node(state=neighbor_pos, parent=current, g_cost=g_cost, h_cost=h_cost)
                heapq.heappush(frontier, neighbor)
    
    return None, explored_count

def print_grid(grid: List[List[bool]], path: Optional[List[Tuple[int, int]]] = None, 
               start: Optional[Tuple[int, int]] = None, goal: Optional[Tuple[int, int]] = None):
    """Print the grid with path visualization"""
    print("\nGrid:")
    for i, row in enumerate(grid):
        for j, is_wall in enumerate(row):
            if (i, j) == start:
                print("S", end=" ")
            elif (i, j) == goal:
                print("G", end=" ")
            elif path and (i, j) in path:
                print("*", end=" ")
            elif is_wall:
                print("█", end=" ")
            else:
                print(".", end=" ")
        print()
    print()

def create_demo_maze() -> Tuple[List[List[bool]], Tuple[int, int], Tuple[int, int]]:
    """Create a demo maze for testing"""
    # Create a 10x10 grid with some walls
    grid = [[False for _ in range(10)] for _ in range(10)]
    
    # Add some walls
    walls = [
        (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
        (4, 1), (4, 2), (4, 3), (4, 4),
        (6, 4), (6, 5), (6, 6), (6, 7), (6, 8),
        (8, 2), (8, 3), (8, 4), (8, 5)
    ]
    
    for wall in walls:
        grid[wall[0]][wall[1]] = True
    
    start = (1, 1)
    goal = (8, 8)
    
    return grid, start, goal

def main():
    """Main demo function"""
    print("=" * 60)
    print("PATHFINDING SEARCH ALGORITHMS DEMO")
    print("=" * 60)
    
    # Create demo maze
    grid, start, goal = create_demo_maze()
    
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    print_grid(grid, start=start, goal=goal)
    
    print("=" * 60)
    print("COMPARING ALGORITHMS")
    print("=" * 60)
    
    # Test Greedy Best-First Search
    print("\n1. GREEDY BEST-FIRST SEARCH")
    print("-" * 30)
    greedy_path, greedy_explored = greedy_best_first_search(grid, start, goal)
    
    if greedy_path:
        print(f"\n✅ Path found!")
        print(f"Path length: {len(greedy_path)}")
        print(f"Cells explored: {greedy_explored}")
        print(f"Path: {greedy_path}")
        print_grid(grid, path=greedy_path, start=start, goal=goal)
    else:
        print("\n❌ No path found!")
    
    print("\n" + "=" * 60)
    
    # Test A* Search
    print("\n2. A* SEARCH")
    print("-" * 30)
    astar_path, astar_explored = a_star_search(grid, start, goal)
    
    if astar_path:
        print(f"\n✅ Path found!")
        print(f"Path length: {len(astar_path)}")
        print(f"Cells explored: {astar_explored}")
        print(f"Path: {astar_path}")
        print_grid(grid, path=astar_path, start=start, goal=goal)
    else:
        print("\n❌ No path found!")
    
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    
    if greedy_path and astar_path:
        print(f"Greedy Best-First Search:")
        print(f"  - Path length: {len(greedy_path)}")
        print(f"  - Cells explored: {greedy_explored}")
        print(f"  - Optimal: {'No' if len(greedy_path) > len(astar_path) else 'Yes'}")
        
        print(f"\nA* Search:")
        print(f"  - Path length: {len(astar_path)}")
        print(f"  - Cells explored: {astar_explored}")
        print(f"  - Optimal: Yes (guaranteed)")
        
        print(f"\nKey Differences:")
        print(f"  - A* explores {astar_explored - greedy_explored} more cells")
        print(f"  - A* path is {'longer' if len(astar_path) > len(greedy_path) else 'shorter' if len(astar_path) < len(greedy_path) else 'same length'}")
        print(f"  - Greedy is faster but may not find optimal path")
        print(f"  - A* is slower but guarantees optimal path")
    
    print("\n" + "=" * 60)
    print("EDUCATIONAL NOTES")
    print("=" * 60)
    print("• Greedy Best-First Search uses only heuristic (h) to guide search")
    print("• A* Search uses both path cost (g) and heuristic (h) for f = g + h")
    print("• Manhattan distance is an admissible heuristic for grid pathfinding")
    print("• A* is complete and optimal when using admissible heuristics")
    print("• Greedy is faster but not guaranteed to be optimal")

if __name__ == "__main__":
    main() 