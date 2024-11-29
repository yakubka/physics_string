# Spring-Mass System Simulation

This Python program simulates a spring-mass-damper system using Matplotlib for visualization and SciPy for solving the differential equations governing the motion. It features a graphical user interface (GUI) for dynamically adjusting parameters and observing their impact on the system in real-time.
Features
Physics Simulation

    Simulates the motion of a mass-spring-damper system under gravity using the equation:
    
    x¨=g−kxm−bx˙m
    x¨=g−mkx​−mbx˙​ where:
        xx: displacement
        kk: spring stiffness
        mm: mass
        bb: damping coefficient
        gg: gravitational acceleration (9.81 m/s²)

Interactive GUI

    Dynamically update the following parameters:
    
        Spring Stiffness (k)
        Mass (m)
        Damping Coefficient (b)
        Maximum Stretch (x_max)
        
    Text boxes allow real-time updates, with the animation adjusting instantly.

Animation

    Visualizes:
    
        The spring stretching/compressing.
        The mass (as a blue square) moving up and down.
        A red spring color when the spring breaks due to excessive force/stretch.

Requirements

    Python 3.7 or above
    Required libraries:
    
        Matplotlib: for animation and GUI elements.
        NumPy: for numerical computations.
        SciPy: for solving differential equations.

Installation

    Clone the repository or download the script:

git clone https://github.com/your-repo/spring-mass-system.git
cd spring-mass-system

Install the required libraries:

    pip install matplotlib scipy numpy

How to Run

    Execute the script:

    python spring_mass_simulation.py

    Use the GUI to adjust parameters and observe changes in real-time.

Components
1. Differential Equation Solver

    Uses solve_ivp from SciPy to solve the second-order ODE for the spring-mass-damper system.

2. Visualization

    Matplotlib:
        FuncAnimation animates the spring and mass motion.
        TextBox widgets allow parameter adjustments during runtime.
        A dynamic spring and mass visualization with collision detection at the ground level.

3. Spring Break Condition

    Spring turns red and the simulation halts when:
        The force exceeds kmax×xmaxkmax​×xmax​.
        The stretch exceeds the maximum allowable length (xmaxxmax​).

Usage Example

    Set Initial Parameters:
        Stiffness: 100 N/m
        Mass: 1 kg
        Damping Coefficient: 0.25 kg/s
        Maximum Stretch: 1 m
    Visualize System Behavior:
        The spring stretches and compresses based on physical forces.
        Update parameters like stiffness or damping to see how the system's behavior changes.

Customization

    Parameters: Modify gravitational constant gg, maximum stiffness kmaxkmax​, or the frame rate (fps).
    Design: Adjust the appearance of the spring, mass, and GUI elements.

Future Enhancements

    Add energy visualization (potential, kinetic, and damping energy).
    Introduce support for multiple springs and masses.
    Save simulation results for analysis.

License

This project is open-source and available under the MIT License.
