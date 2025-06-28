# CS50's Introduction to Artificial Intelligence - Search

## Introduction

This repository contains the implementation of search algorithms discussed in CS50's Introduction to Artificial Intelligence course. The focus is on various search techniques used to solve problems where an agent needs to find a path from an initial state to a goal state.

## Artificial Intelligence

Artificial Intelligence involves creating systems that can perform tasks that typically require human intelligence. In the context of search problems, AI agents must make decisions about which actions to take to reach their objectives efficiently.

## Search

Search problems involve:
- **Initial State**: The starting point of the problem
- **Actions**: The possible moves available from any given state
- **Transition Model**: How actions change the current state
- **Goal Test**: Determines if the current state is the goal
- **Path Cost**: The cost associated with a particular path

## Solving Search Problems

Search algorithms systematically explore the state space to find a solution. They maintain a **frontier** (set of states to explore) and keep track of **explored** states to avoid cycles.

### Key Components:
- **Node**: Contains state, parent, action, and path cost
- **Frontier**: Data structure holding nodes to be explored
- **Explored Set**: Previously visited states

## Depth First Search (DFS)

DFS explores as far as possible along each branch before backtracking. It uses a **stack** (LIFO) for the frontier.

**Characteristics:**
- Not optimal (doesn't guarantee shortest path)
- Complete in finite state spaces
- Space complexity: O(bm) where b is branching factor, m is maximum depth
- Time complexity: O(b^m)

## Breadth First Search (BFS)

BFS explores all nodes at the current depth before moving to nodes at the next depth. It uses a **queue** (FIFO) for the frontier.

**Characteristics:**
- Optimal for unweighted graphs
- Complete if branching factor is finite
- Space complexity: O(b^d) where d is depth of solution
- Time complexity: O(b^d)

## Greedy Best-First Search

This algorithm selects the node that appears to be closest to the goal based on a heuristic function h(n).

**Characteristics:**
- Uses heuristic to guide search
- Not optimal
- More efficient than uninformed search
- Can get stuck in local optima

## A* Search

A* combines the benefits of Dijkstra's algorithm and Greedy Best-First Search. It uses f(n) = g(n) + h(n), where:
- g(n): Cost from start to current node
- h(n): Heuristic estimate from current node to goal

**Characteristics:**
- Optimal if heuristic is admissible (never overestimates)
- Complete
- Optimally efficient
- Space complexity can be exponential

## Adversarial Search

In adversarial search, multiple agents have conflicting goals. This is common in games where one player's gain is another's loss (zero-sum games).

### Game Components:
- **Players**: The agents in the game
- **Initial State**: Starting position
- **Actions**: Legal moves available
- **Result**: Outcome of an action
- **Terminal Test**: Determines if game is over
- **Utility Function**: Assigns numerical value to terminal states

## Minimax

Minimax is a decision-making algorithm for turn-based games. It assumes both players play optimally:
- **Maximizing player**: Tries to maximize the score
- **Minimizing player**: Tries to minimize the score

The algorithm recursively evaluates all possible moves and chooses the one with the best outcome.

**Characteristics:**
- Optimal against optimal opponent
- Time complexity: O(b^m)
- Space complexity: O(bm)

## Alpha-Beta Pruning

Alpha-Beta pruning optimizes minimax by eliminating branches that won't affect the final decision.

- **Alpha**: Best value maximizer can guarantee
- **Beta**: Best value minimizer can guarantee
- **Pruning**: When alpha ≥ beta, remaining branches can be ignored

**Benefits:**
- Reduces time complexity (best case: O(b^(m/2)))
- Same result as minimax
- Allows deeper search in same time

## Depth-Limited Minimax

For games that are too complex for full minimax search, depth-limited minimax stops at a certain depth and uses an evaluation function to estimate the value of non-terminal states.

**Characteristics:**
- Practical for complex games
- Uses evaluation function for intermediate states
- Trade-off between search depth and computation time
- Often combined with iterative deepening

## Implementation

This repository includes:

### Files:
- `maze.py`: Implementation of maze solver with DFS and BFS
- `maze.txt`: Sample maze for testing algorithms
- `maze.png`: Visual output of the maze solution

### Usage:
```bash
# Run DFS (default)
python maze.py maze.txt

# For BFS, change StackFrontier() to QueueFrontier() in maze.py
```

### Maze Visualization:
The program generates a PNG image showing:
- **Red**: Start position (A)
- **Green**: Goal position (B)
- **Yellow**: Solution path
- **Light red**: Explored cells
- **Dark gray**: Walls
- **Light gray**: Empty spaces

![Maze Solution](maze2.png)

*Example output showing the maze solution path found by the search algorithm*

## Key Takeaways

1. **Choice of Algorithm**: Depends on problem constraints (optimality, time, space)
2. **Heuristics**: Can significantly improve search efficiency when admissible
3. **Trade-offs**: Between optimality, completeness, time, and space complexity
4. **Adversarial Settings**: Require different approaches (minimax, alpha-beta pruning)
5. **Practical Considerations**: Depth-limiting and evaluation functions for complex problems

## References

- CS50's Introduction to Artificial Intelligence
- Search
- Harvard University / edX
