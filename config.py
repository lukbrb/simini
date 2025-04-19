# Config file for the simulation
# All parameters should be defined here
# As well as their type and constraints

# This example file defines the configuration 
# for a simulation run with fv2d

# Lucas Barbier-Goy, 18-04-2025

from dataclasses import dataclass

@dataclass
class Mesh:
    Nx: int
    Ny: int
    Nz: int
    Ng: int  # Nghosts


@dataclass
class Run:
    tend: float
    multiple_outputs: bool
    restart_file: bool
    save_freq: float
    output_filename: str
    boundary_x: str
    boundary_y: str


@dataclass
class Solvers:
    reconstruction: str
    riemann_solver: str
    div_cleaning: str
    time_stepping: str
    cfl: float


@dataclass
class Misc:
    epsilon: float


@dataclass
class Physics:
    gamma0: float
    gravity: bool
    g: float
    cr: float
    problem: str


@dataclass
class Polytrope:
    m1: float
    theta1: float
    m2: float
    theta2: float


@dataclass
class Parameters:
    mesh: Mesh
    run: Run
    solvers: Solvers
    physics: Physics
    polytrope: Polytrope
    misc: Misc

