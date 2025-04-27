#!/usr/bin/env python3
"""
Complex Computing Problem (CCP) - Recurrence Relation Solver
Data Algorithms & Analysis Assignment
"""

import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from sympy import Symbol, solve, simplify
# from tabulate import tabulate # Commented out as this dependency might not be available
import time

class RecurrenceRelationSolver:
    """
    A solver for recurrence relations using various methods:
    1. Substitution Method
    2. Master Theorem
    3. Iteration Method
    4. Characteristic Equation Method 
    """

    def __init__(self):
        """Initialize the Recurrence Relation Solver"""
        self.recurrence = None
        self.base_cases = {}  # Dictionary to store base cases
        self.solution = None
        self.solution_method = None
        self.execution_time = 0
        self.steps = []
        self.asymptotic_notation = None

    def parse_recurrence(self, recurrence_str):
        """
        Parse the recurrence relation string into a structured format
        Args:
            recurrence_str: String representation of the recurrence relation
        Returns:
            Dictionary with parsed components
        """
        self.steps.append(f"Parsing recurrence relation: {recurrence_str}")
        
        # Check if it's in the format with multiple T(n/b) terms like T(n)=T(n/2)+T(n/6)+n*log(n)
        complex_divide_conquer_pattern = r'T\(n\)\s*=\s*((?:(?:\d+)?T\(n\s*/\s*\d+\)\s*\+?\s*)+)(.*)'
        match = re.match(complex_divide_conquer_pattern, recurrence_str)
        
        if match:
            # Extract all T(n/b) terms
            t_terms = match.group(1).strip()
            f_n = match.group(2).strip()
            if not f_n:  # If there's no extra term, default to 0
                f_n = "0"
                
            # Extract individual subproblems
            subproblems = []
            t_term_pattern = r'(\d+)?T\(n\s*/\s*(\d+)\)'
            for term in re.finditer(t_term_pattern, t_terms):
                a = int(term.group(1) if term.group(1) else 1)  # Default to 1 if a is not specified
                b = int(term.group(2))
                subproblems.append({'a': a, 'b': b})
            
            self.recurrence = {
                'type': 'complex_divide_and_conquer',
                'subproblems': subproblems,
                'f(n)': f_n
            }
            self.steps.append(f"Identified complex divide and conquer recurrence with {len(subproblems)} subproblems, f(n)={f_n}")
            return self.recurrence
            
        # Check if it's in the standard format T(n) = aT(n/b) + f(n)
        divide_conquer_pattern = r'T\(n\)\s*=\s*(\d+)?T\(n\s*/\s*(\d+)\)\s*\+\s*(.+)'
        match = re.match(divide_conquer_pattern, recurrence_str)
        
        if match:
            a = int(match.group(1) if match.group(1) else 1)  # Default to 1 if a is not specified
            b = int(match.group(2))
            f_n = match.group(3).strip()
            self.recurrence = {
                'type': 'divide_and_conquer',
                'a': a,
                'b': b,
                'f(n)': f_n
            }
            self.steps.append(f"Identified divide and conquer recurrence with a={a}, b={b}, f(n)={f_n}")
            return self.recurrence
        
        # Check if it's in the format T(n) = T(n-d) + f(n) (decrease and conquer)
        decrease_conquer_pattern = r'T\(n\)\s*=\s*T\(n\s*-\s*(\d+)\)\s*\+\s*(.+)'
        match = re.match(decrease_conquer_pattern, recurrence_str)
        
        if match:
            d = int(match.group(1))
            f_n = match.group(2).strip()
            self.recurrence = {
                'type': 'decrease_and_conquer',
                'd': d,
                'f(n)': f_n
            }
            self.steps.append(f"Identified decrease and conquer recurrence with d={d}, f(n)={f_n}")
            return self.recurrence
            
        self.steps.append("Failed to parse the recurrence relation.")
        return None

    def add_base_case(self, n, value):
        """Add a base case T(n) = value"""
        self.base_cases[n] = value
        self.steps.append(f"Added base case: T({n}) = {value}")

    def parse_fn_growth(self, f_n):
        """
        More robustly parse the f(n) function to determine its growth rate
        Args:
            f_n: String representation of f(n)
        Returns:
            Tuple of (growth_category, power)
        """
        f_n = f_n.strip().lower()
        
        # Check for constant time
        if f_n == "1" or f_n == "o(1)" or f_n == "o(1)" or f_n == "θ(1)" or "constant" in f_n:
            return ("constant", 0)
            
        # Check for logarithmic time
        if "log" in f_n or "ln" in f_n:
            if "n^" in f_n or "n**" in f_n:  # Check for n^something * log
                power_pattern = r'n\^?(?:\*\*)?\s*(\d*\.?\d*)'
                power_match = re.search(power_pattern, f_n)
                if power_match and power_match.group(1):
                    power = float(power_match.group(1)) if power_match.group(1) else 1
                    return ("n_log", power)  # Like n^2 * log n
                return ("n_log", 1)  # Default to n log n
            return ("logarithmic", 0)
        
        # Check for polynomial time
        if "n" in f_n:
            power_pattern = r'n\^?(?:\*\*)?\s*(\d*\.?\d*)'
            power_match = re.search(power_pattern, f_n)
            
            if power_match and power_match.group(1):
                power = float(power_match.group(1)) if power_match.group(1) else 1
                return ("polynomial", power)
            
            # If we just have "n" without a power
            if "n^" not in f_n and "n**" not in f_n and "n *" not in f_n and "n*" not in f_n:
                return ("polynomial", 1)
        
        # Check for specific notations like O(n), Θ(n^2), etc.
        notation_pattern = r'[oOθΘ]\(n\^?(?:\*\*)?\s*(\d*\.?\d*)\)'
        notation_match = re.search(notation_pattern, f_n)
        if notation_match:
            if notation_match.group(1):
                power = float(notation_match.group(1))
            else:
                power = 1  # Default to 1 if just O(n)
            return ("polynomial", power)
            
        # Return default if nothing matches
        return ("unknown", None)

    def format_solution(self, solution):
        """
        Format the solution with proper asymptotic notation
        Args:
            solution: The solution string to format
        Returns:
            Formatted solution string
        """
        self.steps.append(f"Formatting solution: {solution}")
        
        # Store the asymptotic notation for later use
        self.asymptotic_notation = solution
        
        # Replace common notation with proper symbols
        formatted = solution
        # Replace Theta with Θ
        formatted = formatted.replace("Theta", "Θ")
        formatted = formatted.replace("theta", "Θ")
        # Replace Big O with O
        formatted = formatted.replace("O(", "O(")
        # Replace n^2 with n²
        formatted = formatted.replace("n^2", "n²")
        # Replace n^3 with n³
        formatted = formatted.replace("n^3", "n³")
        # Format any other common powers or notations
        
        self.steps.append(f"Formatted solution: {formatted}")
        return formatted

    def solve(self, method=None):
        """
        Solve the recurrence relation using the specified or best available method
        Args:
            method: Solution method ('master', 'substitution', 'iteration', 'characteristic')
        Returns:
            The solution as a string
        """
        if not self.recurrence:
            self.steps.append("No recurrence relation has been parsed yet.")
            return None
            
        start_time = time.time()
        
        # Handle complex divide and conquer recurrences
        if self.recurrence['type'] == 'complex_divide_and_conquer':
            self.steps.append("Complex divide and conquer recurrence detected with multiple subproblems.")
            self.steps.append("Using iterative expansion to analyze the solution.")
            
            # Set solution method
            self.solution_method = "Iterative Expansion"
            
            # For complex recurrences, we need more sophisticated analysis
            subproblems = self.recurrence['subproblems']
            f_n = self.recurrence['f(n)']
            
            # Calculate total work at each level
            total_a = sum(sub['a'] for sub in subproblems)
            
            # Find the dominant term (smallest b leads to largest n/b terms)
            min_b = min(sub['b'] for sub in subproblems)
            
            self.steps.append(f"Total coefficient sum: {total_a}")
            self.steps.append(f"Minimum divisor: {min_b}")
            
            # Use a simplified approach for the complex case
            growth_category, power = self.parse_fn_growth(f_n)
            
            # Calculate log_b(total_a) for each b
            ratios = [np.log(total_a) / np.log(sub['b']) for sub in subproblems]
            max_ratio = max(ratios)
            
            self.steps.append(f"Log ratios for subproblems: {ratios}")
            self.steps.append(f"Maximum log ratio: {max_ratio}")
            
            # Use a simplified decision making process
            if growth_category == "polynomial":
                if abs(max_ratio - power) < 1e-10:  # They are equal (Case 2)
                    self.solution = f"Θ(n^{power} log n)"
                elif max_ratio > power:  # Case 1
                    self.solution = f"Θ(n^{max_ratio})"
                else:  # Case 3
                    self.solution = f"Θ(n^{power})"
            elif growth_category == "logarithmic":
                if max_ratio > 0:
                    self.solution = f"Θ(n^{max_ratio})"
                else:
                    self.solution = "Θ(log n)"
            elif growth_category == "constant":
                if max_ratio > 0:
                    self.solution = f"Θ(n^{max_ratio})"
                else:
                    self.solution = "Θ(1)"
            elif growth_category == "n_log":
                if max_ratio >= power:
                    self.solution = f"Θ(n^{max_ratio})"
                else:
                    self.solution = f"Θ(n^{power} log n)"
            else:
                self.solution = "Cannot determine asymptotic behavior for complex recurrence"
                
            # Format the solution
            if self.solution:
                self.solution = self.format_solution(self.solution)
                
            return self.solution
        
        # Handle standard recurrence types
        if method == 'master' and self.recurrence['type'] == 'divide_and_conquer':
            solution = self.solve_using_master_theorem()
        elif method == 'substitution':
            solution = self.solve_using_substitution()
        elif method == 'iteration':
            solution = self.solve_using_iteration()
        else:
            # Try to find the best method
            if self.recurrence['type'] == 'divide_and_conquer':
                solution = self.solve_using_master_theorem()
                if not solution:
                    solution = self.solve_using_iteration()
                    if not solution:
                        solution = self.solve_using_substitution()
            else:  # decrease_and_conquer or other
                solution = self.solve_using_iteration()
                if not solution:
                    solution = self.solve_using_substitution()
        
        self.execution_time = time.time() - start_time
        self.steps.append(f"Solution found in {self.execution_time:.6f} seconds.")
        
        # Format the solution before returning
        if solution:
            solution = self.format_solution(solution)
            
        return solution
        
    def display_steps(self):
        """Display the steps taken to solve the recurrence"""
        print("\nSolution Steps:")
        for i, step in enumerate(self.steps, 1):
            print(f"Step {i}: {step}")
            
    def plot_growth(self, n_values=None):
        """
        Plot the growth of the recurrence relation and its solution
        Args:
            n_values: List of n values to plot
        """
        if not n_values:
            n_values = range(1, 101)
            
        plt.figure(figsize=(10, 6))
        plt.title(f"Growth of Recurrence Relation Solution\n{self.solution}")
        plt.xlabel("n")
        plt.ylabel("T(n)")
        plt.grid(True)
        
        # This is a simplified plotting function that only plots the asymptotic growth
        if "n log n" in self.solution:
            y_values = [n * np.log(n) for n in n_values]
            plt.plot(n_values, y_values, label="n log n")
        elif "n²" in self.solution or "n^2" in self.solution:
            y_values = [n**2 for n in n_values]
            plt.plot(n_values, y_values, label="n²")
        elif "n" in self.solution and "log" not in self.solution:
            y_values = [n for n in n_values]
            plt.plot(n_values, y_values, label="n")
        elif "log" in self.solution.lower():
            y_values = [np.log(n) for n in n_values]
            plt.plot(n_values, y_values, label="log n")
        elif "^" in self.solution:
            # Extract power from things like Θ(n^2.5)
            power_match = re.search(r'n\^?(\d*\.?\d*)', self.solution)
            if power_match:
                power = float(power_match.group(1)) if power_match.group(1) else 1
                y_values = [n**power for n in n_values]
                plt.plot(n_values, y_values, label=f"n^{power}")
        
        plt.legend()
        plt.show()


def main():
    """Main function to run the CCP (Complex Computing Problem) solver"""
    print("Welcome to the Complex Computing Problem (CCP) Solver!")
    print("This program solves recurrence relations using various methods.")
    
    solver = RecurrenceRelationSolver()
    
    print("\nPlease select the type of recurrence relation:")
    print("1. Divide and Conquer: T(n) = aT(n/b) + f(n)")
    print("2. Decrease and Conquer: T(n) = T(n-d) + f(n)")
    print("3. Complex Divide and Conquer: T(n) = T(n/b1) + T(n/b2) + ... + f(n)")
    
    choice = input("\nEnter your choice (1, 2, or 3): ")
    
    if choice == '1':
        a = int(input("Enter the value of a (coefficient): "))
        b = int(input("Enter the value of b (divisor): "))
        
        print("\nChoose f(n):")
        print("1. O(1) - Constant")
        print("2. O(n) - Linear")
        print("3. O(n^c) - Polynomial")
        print("4. O(log n) - Logarithmic")
        
        fn_choice = input("\nEnter your choice for f(n) (1-4): ")
        
        if fn_choice == '1':
            f_n = "1"
        elif fn_choice == '2':
            f_n = "n"
        elif fn_choice == '3':
            c = float(input("Enter the value of c (power): "))
            f_n = f"n^{c}"
        elif fn_choice == '4':
            f_n = "log n"
        else:
            print("Invalid choice. Using O(1) as default.")
            f_n = "1"
            
        recurrence_str = f"T(n) = {a}T(n/{b}) + {f_n}"
        
    elif choice == '2':
        d = int(input("Enter the value of d (decrement): "))
        
        print("\nChoose f(n):")
        print("1. O(1) - Constant")
        print("2. O(n) - Linear")
        print("3. O(n^c) - Polynomial")
        
        fn_choice = input("\nEnter your choice for f(n) (1-3): ")
        
        if fn_choice == '1':
            f_n = "1"
        elif fn_choice == '2':
            f_n = "n"
        elif fn_choice == '3':
            c = float(input("Enter the value of c (power): "))
            f_n = f"n^{c}"
        else:
            print("Invalid choice. Using O(1) as default.")
            f_n = "1"
            
        recurrence_str = f"T(n) = T(n-{d}) + {f_n}"
        
    elif choice == '3':
        # Handle complex divide and conquer recurrences
        recurrence_str = input("Enter the recurrence relation (e.g., T(n)=T(n/2)+T(n/6)+n*log(n)): ")
        
        # Add "T(n) =" prefix if not provided by the user
        if not recurrence_str.lower().startswith("t(n)"):
            recurrence_str = "T(n) = " + recurrence_str
        
        print(f"\nSolving recurrence relation: {recurrence_str}")
        
        # Parse the recurrence relation
        parsed = solver.parse_recurrence(recurrence_str)
        
        # If parsing failed, try some common fixes
        if not parsed:
            # Try adding a missing "+" between terms
            fixed_recurrence = re.sub(r'(\)\s*)T', r'\1+T', recurrence_str)
            if fixed_recurrence != recurrence_str:
                print(f"Trying with fixed syntax: {fixed_recurrence}")
                parsed = solver.parse_recurrence(fixed_recurrence)
                
        # If still not parsed, inform the user
        if not parsed:
            print("Failed to parse the recurrence relation.")
            print("Please make sure it follows the format: T(n) = T(n/b1) + T(n/b2) + ... + f(n)")
            return
        
        # For complex recurrences, automatically add default base cases
        solver.add_base_case(1, 1)  # T(1) = 1 as default base case
        
        # Solve using automatic method selection
        solution = solver.solve()
        
        if solution:
            print(f"\nSolution: T(n) = {solution}")
            print(f"Method used: {solver.solution_method}")
            
            # Display steps
            print("\nSolution Steps:")
            solver.display_steps()
            
            # Ask if user wants to see the plot
            plot_growth = input("\nWould you like to see a plot of the solution's growth? (y/n): ")
            if plot_growth.lower() == 'y':
                solver.plot_growth()
        else:
            print("\nFailed to solve the recurrence relation.")
        
        # Return to avoid the regular flow below for other recurrence types
        return
            
    else:
        print("Invalid choice. Exiting.")
        return
        
    print(f"\nSolving recurrence relation: {recurrence_str}")
    
    # Parse the recurrence relation
    parsed = solver.parse_recurrence(recurrence_str)
    
    if not parsed:
        print("Failed to parse the recurrence relation.")
        return
        
    # Add base cases - get input from the user
    print("\nEnter base cases:")
    if choice == '1':  # Divide and conquer
        print("For divide and conquer recurrences, base cases are typically for the smallest input size.")
    else:  # Decrease and conquer
        print("For decrease and conquer recurrences, base cases are typically for initial values.")
    
    base_case_count = int(input("How many base cases would you like to add? "))
    for i in range(base_case_count):
        try:
            n = int(input(f"Enter the value of n for base case {i+1}: "))
            value = float(input(f"Enter T({n}) = "))
            solver.add_base_case(n, value)
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            n = 1
            value = 1
            print(f"Using default: T({n}) = {value}")
            solver.add_base_case(n, value)
        
    # Choose solution method
    print("\nChoose solution method:")
    print("1. Automatic (best method)")
    print("2. Master Theorem (only for divide and conquer)")
    print("3. Substitution Method")
    print("4. Iteration Method")
    
    method_choice = input("\nEnter your choice (1-4): ")
    
    if method_choice == '2':
        method = 'master'
    elif method_choice == '3':
        method = 'substitution'
    elif method_choice == '4':
        method = 'iteration'
    else:
        method = None  # Automatic
        
    # Solve the recurrence
    solution = solver.solve(method)
    
    if solution:
        print(f"\nSolution: T(n) = {solution}")
        print(f"Method used: {solver.solution_method}")
        
        # Display steps
        display_steps = input("\nWould you like to see the solution steps? (y/n): ")
        if display_steps.lower() == 'y':
            solver.display_steps()
            
        # Plot growth
        plot_growth = input("\nWould you like to see a plot of the solution's growth? (y/n): ")
        if plot_growth.lower() == 'y':
            solver.plot_growth()
    else:
        print("\nFailed to solve the recurrence relation.")

if __name__ == "__main__":
    main()


