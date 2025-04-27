# Recurrence Relation Solver

![License](https://img.shields.io/github/license/muhammadsamiirshad/recurrence-relation-solver)
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)

A comprehensive tool for solving and analyzing recurrence relations in algorithmic complexity analysis. This solver is part of the Data Algorithms & Analysis (DAA) course assignment.

## Features

- **Multiple Solution Methods**:
  - Master Theorem
  - Substitution Method
  - Iteration Method
  - Characteristic Equation Method

- **Support for Various Recurrence Types**:
  - Divide and Conquer: T(n) = aT(n/b) + f(n)
  - Decrease and Conquer: T(n) = T(n-d) + f(n)
  - Complex Divide and Conquer: T(n) = T(n/b₁) + T(n/b₂) + ... + f(n)

- **Visualization**: Plot the growth rate of the recurrence solution

- **Step-by-Step Solutions**: See the detailed solution process

## Installation

```bash
# Clone the repository
git clone https://github.com/muhammadsamiirshad/recurrence-relation-solver.git
cd recurrence-relation-solver

# Install dependencies
pip install matplotlib numpy sympy
```

## Usage

Run the program:

```bash
python ccp.py
```

### Interactive Menu Guide

The solver offers an intuitive, menu-driven interface:

1. **Select Recurrence Type**:
   - Divide and Conquer (`T(n) = aT(n/b) + f(n)`)
   - Decrease and Conquer (`T(n) = T(n-d) + f(n)`)
   - Complex Recurrence (custom input)

2. **Enter Parameters**:
   - For Divide and Conquer: Enter values for `a` (subproblems) and `b` (size reduction factor)
   - For Decrease and Conquer: Enter the value for `d` (reduction amount)
   - For Complex: Enter the full recurrence relation in a supported format

3. **Specify Complexity Function**:
   - Choose from common functions (constant, logarithmic, linear, etc.)
   - Or enter a custom function like `n^2*log(n)`

4. **Define Base Cases**:
   - Enter values for the smallest instances (e.g., T(1) = 1)
   - Multiple base cases can be entered for complex recurrences

5. **Select Solution Method**:
   - Master Theorem (for eligible divide-and-conquer recurrences)
   - Substitution Method (prove a guessed solution)
   - Iteration Method (recursive expansion)
   - Characteristic Equation (for linear homogeneous recurrences)

6. **View Results**:
   - Asymptotic bound (Θ, O, or Ω)
   - Step-by-step solution walkthrough
   - Growth rate visualization

### Command Options

Additional command-line options:
```bash
python ccp.py --no-plot  # Run without generating plots
python ccp.py --verbose  # Show detailed solution steps
python ccp.py --save     # Save results to output file
```

### Examples

#### Example 1: Master Theorem
For a standard divide and conquer recurrence T(n) = 2T(n/2) + n:
```
Input:
- Recurrence type: Divide and Conquer
- a = 2, b = 2
- f(n) = n
- Base case: T(1) = 1
- Method: Master Theorem

Output:
Solution: T(n) = Θ(n log n)
Case 2 of Master Theorem applies: f(n) = Θ(n^logb(a))
```

#### Example 2: Iteration Method
For a decrease and conquer recurrence T(n) = T(n-1) + n:
```
Input:
- Recurrence type: Decrease and Conquer
- d = 1
- f(n) = n
- Base case: T(0) = 0
- Method: Iteration

Output:
T(n) = T(n-1) + n
     = T(n-2) + (n-1) + n
     = T(n-3) + (n-2) + (n-1) + n
     = ...
     = T(0) + 1 + 2 + ... + (n-1) + n
     = 0 + n(n+1)/2
     = Θ(n²)
```

#### Example 3: Complex Recurrence
For T(n) = 3T(n/2) + 2T(n/3) + n²:
```
Input:
- Recurrence type: Complex
- Custom recurrence: T(n) = 3T(n/2) + 2T(n/3) + n²
- Base cases: T(1) = 1, T(2) = 3
- Method: Substitution

Output:
Guess: T(n) = O(n²)
Verification steps shown...
Solution: T(n) = Θ(n²)
```

## Technical Details

The solver uses several analytical techniques:

- **Master Theorem**: For standard divide-and-conquer recurrences
- **Iteration Method**: Expands the recurrence to find patterns
- **Substitution Method**: Uses mathematical induction principles
- **Asymptotic Analysis**: Determines the Big-O, Theta, or Omega complexity

## Requirements

- Python 3.6+
- NumPy
- SymPy
- Matplotlib

## Documentation

For more information, see the included documentation file: `ccp_flow_documentation.docx`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.