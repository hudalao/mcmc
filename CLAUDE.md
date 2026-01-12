# CLAUDE.md - AI Assistant Guide for MCMC Project

## Project Overview

This is a **Markov Chain Monte Carlo (MCMC)** simulation library that uses the Metropolis-Hastings algorithm to generate and analyze random graph structures. The project simulates connected graphs on a 2D grid, where vertices are positioned uniformly and edges have weights based on Euclidean distance.

**Key Information:**
- **Language:** Python 2.6, 2.7, 3.3, 3.4, 3.5
- **License:** MIT
- **Author:** Wenxiang Hu (wenxiang.hu@outlook.com)
- **Version:** 0.1.0
- **Repository:** https://github.com/hudalao/mcmc

## Codebase Structure

```
mcmc/
├── mcmc/                          # Main package directory
│   ├── __init__.py               # Package initialization (version info)
│   ├── mcmc.py                   # Main simulation program (runnable script)
│   ├── edge_oper.py              # Edge operations class
│   ├── graph.py                  # Graph connectivity class (connec_graph)
│   ├── Metripolis_Hastings.py    # M-H algorithm implementation
│   ├── theta.py                  # Theta function calculation
│   ├── posi_assign.py            # Vertex position assignment
│   └── plot_graph.py             # Graph visualization utilities
├── tests/
│   ├── __init__.py
│   └── test_mcmc.py              # Unit tests
├── docs/                         # Sphinx documentation
├── .github/
│   └── ISSUE_TEMPLATE.md
├── setup.py                      # Package setup and dependencies
├── setup.cfg                     # Build configuration
├── tox.ini                       # Testing automation config
├── .travis.yml                   # CI/CD configuration
├── Makefile                      # Development tasks automation
├── README.rst                    # User-facing documentation
├── CONTRIBUTING.rst              # Contribution guidelines
├── requirements_dev.txt          # Development dependencies
└── LICENSE                       # MIT license
```

## Core Components

### 1. **mcmc.py** - Main Simulation Program
**Location:** `mcmc/mcmc.py`

The main executable that runs the MCMC simulation. Key parameters:
- `Time_points`: Total simulation iterations (default: 20000)
- `T`: Temperature constant (default: 10)
- `r`: Edge weight coefficient (default: 5)
- `N`: Number of vertices (default: 5)
- `Dx`, `Dy`: Grid dimensions (default: 5x5)
- `Lx`, `Ly`: Grid physical size (default: 1x1)

**Main Outputs:**
1. Most probable graph configuration
2. Expected number of edges connected to vertex 0
3. Expected total number of edges
4. Expected maximum shortest path distance from vertex 0

**Important:** The script runs as a standalone simulation and stores all graph states in list `G`.

### 2. **edge_oper.py** - Edge Operations Class
**Location:** `mcmc/edge_oper.py`

Class managing all edge-related operations:
- `weight_calc()`: Calculates Euclidean distance matrix between vertices
- `ran_edge()`: Generates random edge uniformly
- `update_edges_list(edge_gene, edges_keep_list)`: Adds/removes edges while maintaining connectivity
- `edges_weighted(weight)`: Assigns weights to graph edges

**Key Behavior:**
- Edges are always stored in sorted order (smaller vertex first)
- Protected edges (from spanning tree) cannot be deleted

### 3. **graph.py** - Connected Graph Class
**Location:** `mcmc/graph.py`

Class `connec_graph` handles graph connectivity:
- `init_graph()`: Creates initial star graph (vertex 0 connected to all others)
- `edges_keep()`: Identifies critical edges that maintain connectivity (spanning tree edges)

**Algorithm:** Tests each edge for criticality by temporarily removing it and checking connectivity.

### 4. **Metripolis_Hastings.py** - M-H Algorithm
**Location:** `mcmc/Metripolis_Hastings.py`

Implements the Metropolis-Hastings acceptance/rejection logic:
- Proposes new graph state by adding/removing random edge
- Calculates acceptance probability: `α = min(1, (π_j/π_i) × (q_ji/q_ij))`
- Accepts/rejects based on uniform random draw
- Returns updated graph or keeps current state

**Critical:** Uses deep copying to prevent unintended mutations when proposals are rejected.

### 5. **theta.py** - Objective Function
**Location:** `mcmc/theta.py`

Calculates the energy function (theta):
```
θ = r × Σ(edge_weights) + Σ(shortest_path_distances_from_vertex_0)
```

This balances:
- First term: Penalizes long edges
- Second term: Penalizes disconnected/sparse graphs

### 6. **posi_assign.py** - Position Assignment
**Location:** `mcmc/posi_assign.py`

Generates unique random positions for N vertices on a 2D grid.
- Creates uniform grid
- Randomly samples N unique positions
- Ensures no duplicate positions

### 7. **plot_graph.py** - Visualization
**Location:** `mcmc/plot_graph.py`

Plots graphs with:
- Solid lines for edges with weight > 0.5
- Dashed lines for edges with weight ≤ 0.5

**Note:** Plotting code is commented out in current version.

## Development Workflows

### Setting Up Development Environment

1. **Clone and create virtual environment:**
```bash
git clone git@github.com:hudalao/mcmc.git
cd mcmc
mkvirtualenv mcmc
```

2. **Install in development mode:**
```bash
python setup.py develop
```

3. **Install dependencies:**
```bash
pip install -r requirements_dev.txt
```

### Running Tests

**Quick test:**
```bash
python setup.py test
# or
py.test
# or
python -m unittest tests.test_mcmc
```

**With coverage:**
```bash
make coverage
```

**All Python versions with tox:**
```bash
tox
```

**Lint checking:**
```bash
make lint
# or
flake8 mcmc tests
```

### Building Documentation

```bash
make docs
```

### Running the Simulation

```bash
cd mcmc/
python mcmc.py
```

### Common Make Targets

- `make clean` - Remove build/test artifacts
- `make lint` - Run flake8 style checking
- `make test` - Run tests quickly
- `make test-all` - Run tests on all Python versions
- `make coverage` - Generate coverage report
- `make docs` - Build documentation
- `make dist` - Build distribution packages
- `make install` - Install package

## Testing Strategy

### Test Suite Location
**File:** `tests/test_mcmc.py`

### Current Test Coverage

1. **test_prohibited_cutedges** - Verifies spanning tree edge identification
2. **test_edge_delet** - Tests edge deletion for non-critical edges
3. **test_edge_add** - Tests edge addition
4. **test_no_edge_change** - Tests that critical edges cannot be deleted
5. **test_theta** - Validates theta function calculation

### Testing Conventions

- Uses `unittest` framework
- Setup creates standard test graph (star from vertex 0)
- Tests use N=5 vertices
- All tests use deterministic positions for reproducibility

### CI/CD

- **Travis CI** configured for continuous integration
- Tests run on Python 3.3, 3.4
- Uses conda environment with dependencies: numpy, scipy, matplotlib, networkx, pandas
- Coverage reports sent to Coveralls

## Code Conventions

### Import Organization
All modules follow this pattern:
1. Standard library imports
2. Third-party imports (numpy, networkx, matplotlib)
3. Local imports
4. Path manipulation (if needed for module resolution)

### Naming Conventions

- **Classes:** `PascalCase` (e.g., `edge_oper`, `connec_graph`) - Note: Current code uses snake_case for classes
- **Functions:** `snake_case` (e.g., `weight_calc`, `init_graph`)
- **Variables:** `snake_case` with descriptive names
- **Constants:** `UPPER_CASE` (e.g., `Time_points`, `N`, `T`, `r`)

### Code Style

- **Indentation:** 4 spaces
- **Line length:** Not strictly enforced, but keep reasonable
- **String quotes:** Single quotes preferred
- **Comments:** Inline comments for complex logic, docstrings minimal

### Graph Handling

**CRITICAL PATTERN:** Always use `copy.deepcopy()` when preserving graph state:
```python
R = copy.deepcopy(Xi)  # Reference graph for proposals
```

**Why:** NetworkX Graph objects are mutable; shallow copies lead to unintended modifications.

### Edge Representation

- Edges always stored as tuples: `(start, end)` where `start < end`
- Use `tuple(sorted(edge))` to normalize
- Edge lists converted to strings for dictionary keys: `','.join(str(e) for e in G.edges())`

## Key Algorithms and Mathematical Background

### Metropolis-Hastings Algorithm

**Purpose:** Sample from complex probability distribution π(x) over graph space

**Acceptance Probability:**
```
α = min(1, [π(x_j) / π(x_i)] × [q(x_i|x_j) / q(x_j|x_i)])
```

Where:
- `π(x) ∝ exp(-θ(x)/T)` - Target distribution (Boltzmann)
- `q(x_j|x_i)` - Proposal distribution (uniform edge flip)
- `T` - Temperature parameter (controls exploration)

**Proposal Mechanism:**
1. Select random edge uniformly from all possible edges
2. If edge exists and is deletable → delete it
3. If edge doesn't exist → add it
4. If edge exists but is critical → no change

**Transition Probabilities:**
- `q_ij = 1 / (N(N-1)/2 - critical_edges_count_i)`
- `q_ji = 1 / (N(N-1)/2 - critical_edges_count_j)`

### Theta Function (Energy/Cost)

```python
θ(G) = r × Σ(edge_weights) + Σ(shortest_paths_from_0)
```

**Interpretation:**
- Minimizes total edge weight (favors short edges)
- Minimizes path distances (favors connectivity)
- Parameter `r` balances these objectives

### Ergodicity

The algorithm assumes ergodic conditions, so expectations are computed as time averages:
```
E[h(x)] ≈ (1/N) × Σ h(x_i)
```

## Dependencies

### Runtime Dependencies
- **Click** >= 6.0 - Command-line interface
- **NetworkX** - Graph operations
- **NumPy** - Numerical computations
- **Matplotlib** - Visualization
- **SciPy** - Scientific computing (indirect, via conda)

### Development Dependencies
- **flake8** - Linting
- **tox** - Testing automation
- **coverage/coveralls** - Code coverage
- **sphinx** - Documentation
- **pytest/nose** - Testing frameworks
- **bumpversion** - Version management

## Important Considerations for AI Assistants

### When Modifying Code

1. **Maintain Python 2/3 Compatibility**
   - Code must run on Python 2.6+ and 3.3+
   - Avoid Python 3-only syntax
   - Test with `tox` before committing

2. **Preserve Mathematical Correctness**
   - The M-H algorithm is subtle; changes to acceptance logic can break ergodicity
   - Always verify theta function calculations match mathematical definition
   - Don't modify the proposal distribution without careful consideration

3. **Deep Copy Graph Objects**
   - NetworkX graphs are mutable
   - Always use `copy.deepcopy()` when preserving state
   - Forgetting this causes subtle bugs in M-H algorithm

4. **Edge Ordering**
   - Edges must be consistently ordered (smaller vertex first)
   - Use `tuple(sorted(edge))` pattern throughout

5. **Testing New Features**
   - Add unit tests to `tests/test_mcmc.py`
   - Ensure tests pass for all Python versions via tox
   - Update documentation in README.rst

6. **Performance Considerations**
   - The main simulation runs for 20,000 iterations by default
   - Profiling changes is important for core functions
   - NetworkX operations (esp. `shortest_path_length`) can be slow

### Common Pitfalls

1. **Modifying Graph During Iteration**
   ```python
   # BAD
   for edge in G.edges():
       G.remove_edge(edge[0], edge[1])

   # GOOD
   edges_to_remove = list(G.edges())
   for edge in edges_to_remove:
       G.remove_edge(edge[0], edge[1])
   ```

2. **Forgetting to Update edges_keep_list**
   - After modifying graph, spanning tree may change
   - Always recalculate: `edges_keep_num, edges_keep_list = connec_graph(N, G).edges_keep()`

3. **Incorrect Transition Probability**
   - Must account for critical edges that cannot be proposed
   - Formula: `q = 1 / (total_possible_edges - critical_edges)`

4. **Not Handling Rejected Proposals**
   - When proposal is rejected, must use PREVIOUS state for all variables
   - This includes `theta_j`, `qji`, `edges_keep_list_j`

### Code Quality Standards

- **Flake8 compliance:** Code must pass `flake8 mcmc tests`
- **Test coverage:** New code should include tests
- **Documentation:** Update README.rst for user-facing changes
- **Commit messages:** Descriptive, follow conventional format

### File Locations Reference

| Functionality | File | Key Functions/Classes |
|--------------|------|----------------------|
| Main simulation | `mcmc/mcmc.py` | Main execution script |
| Edge operations | `mcmc/edge_oper.py` | `edge_oper` class |
| Graph connectivity | `mcmc/graph.py` | `connec_graph` class |
| M-H algorithm | `mcmc/Metripolis_Hastings.py` | `Metripolis_Hastings()` |
| Energy function | `mcmc/theta.py` | `theta()` |
| Position setup | `mcmc/posi_assign.py` | `posi_assign()` |
| Visualization | `mcmc/plot_graph.py` | `plot_graph()` |
| Tests | `tests/test_mcmc.py` | `TestMcmc` class |

### When Asked to Add Features

1. **Read existing code first** - Understand current architecture
2. **Follow existing patterns** - Match coding style and structure
3. **Add tests** - Every feature needs unit tests
4. **Update documentation** - Modify README.rst as needed
5. **Check compatibility** - Ensure Python 2/3 compatibility
6. **Run test suite** - `make test` before committing

### When Debugging

1. **Check deep copy usage** - Most graph-related bugs stem from this
2. **Verify edge ordering** - Inconsistent ordering causes lookup failures
3. **Validate theta calculation** - Mathematical errors here break the algorithm
4. **Test with small N** - Use N=3 or N=4 for faster debugging
5. **Print intermediate states** - Log graph edges, theta values, acceptance decisions

## Git Workflow

### Branch Naming
- Feature branches: `feature/<description>`
- Bug fixes: `bugfix/<description>`
- Current working branch: `claude/add-claude-documentation-9mEmG`

### Commit Guidelines
- Clear, descriptive messages
- Reference issues when applicable
- Atomic commits (one logical change per commit)

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Ensure all tests pass: `tox`
5. Ensure linting passes: `make lint`
6. Submit PR with description

## Additional Resources

- **Documentation:** https://mcmc.readthedocs.io
- **Issue Tracker:** https://github.com/hudalao/mcmc/issues
- **CI/CD:** https://travis-ci.org/hudalao/mcmc
- **Coverage:** https://coveralls.io/github/hudalao/mcmc

## Version History

- **0.1.0** - Initial release with core MCMC functionality

---

**Last Updated:** 2026-01-12
**Maintainer:** Wenxiang Hu
**For AI Assistants:** This document provides comprehensive context for understanding and modifying the MCMC codebase. Always prioritize mathematical correctness and backward compatibility.
