# Config file for the simulation
# All parameters should be defined here
# As well as their type and constraints

# This example file defines the configuration 
# for a simulation run with fv2d

# Lucas Barbier-Goy, 18-04-2025

from dataclasses import dataclass, field
# from enum import IntEnum, StrEnum
import configparser

from validators import IntRange, MultipleChoice, FloatRange, Boolean
# class RiemannSolver(StrEnum):
#     HLL = "hll"
#     HLLC = "hllc"
#     HLLD = "hlld"
#     FIVEWAVES = "fivewaves"


# class DivCleaning(StrEnum):
#     NO_DC = "no_dc"
#     DEDNER = "dedner"
#     DERIGS = "derigs"


@dataclass
class Mesh:
    Nx: IntRange = IntRange(512, min_value=1)
    Ny: IntRange = IntRange(512, min_value=1)
    Nz: IntRange = IntRange(0, min_value=1)
    Ng: IntRange = IntRange(2, min_value=0)  # Nghosts


@dataclass
class Run:
    tend: FloatRange = FloatRange(1.0, min_value=0.001)
    multiple_outputs: Boolean = Boolean(False)
    # restart_file: bool
    save_freq: FloatRange = FloatRange(1e-1, min_value=0.001)
    output_filename: str = "run"
    boundary_x: MultipleChoice = MultipleChoice(["reflecting", "absorbing", "periodic"], default="reflecting")
    boundary_y: MultipleChoice = MultipleChoice(["reflecting", "absorbing", "periodic"], default="reflecting")


@dataclass
class Solvers:
    reconstruction: MultipleChoice = MultipleChoice(["pcm", "pcm_wb", "plm"], default="pcm")
    riemann_solver: MultipleChoice = MultipleChoice(["hll", "hllc", "hlld", "fivewaves"], default="hllc")
    div_cleaning: MultipleChoice = MultipleChoice(["none", "dedner", "derigs"], default="none")
    time_stepping: MultipleChoice = MultipleChoice(["euler", "rk2"], default="euler")
    cfl: FloatRange = FloatRange(0.1, min_value=1e-3, max_value=1.0)


@dataclass
class Misc:
    epsilon: FloatRange = FloatRange(1e-10, min_value=-1e-16, max_value=1e-5)
    seed: IntRange = IntRange(12345)
    log_frequency: IntRange = IntRange(10, min_value=1)


@dataclass
class Physics:
    gamma0: FloatRange = FloatRange(5/3, min_value=1.0, max_value=2.0)
    gravity: Boolean = Boolean(False)
    g: FloatRange = FloatRange(0.0)
    cr: FloatRange = FloatRange(0.1)
    problem: MultipleChoice = MultipleChoice(["sod", "blastwave", "shocktube"], default="sod")


@dataclass
class Polytrope:
    m1: FloatRange = FloatRange(1.0)
    theta1: FloatRange = FloatRange(10.0)
    m2: FloatRange = FloatRange(1.0)
    theta2: FloatRange = FloatRange(10.0)


@dataclass
class ThermalConduction:
    kappa: FloatRange = FloatRange(0.0)
    bc_xmin:  MultipleChoice = MultipleChoice(["none", "fixed_temperature", "fixed_gradient"], default="none")
    bc_ymin:  MultipleChoice = MultipleChoice(["none", "fixed_temperature", "fixed_gradient"], default="none")
    bc_xmin_value: FloatRange = FloatRange(1.0)
    bc_ymin_value: FloatRange = FloatRange(1.0)


@dataclass
class Viscosity:
    active: Boolean = Boolean(False)
    viscosity_mode: MultipleChoice = MultipleChoice(["constant"], default="constant")
    mu: FloatRange = FloatRange(1.0)


@dataclass
class H84:
    perturbation: FloatRange = FloatRange(1e-4)


@dataclass
class C91:
    perturbation: FloatRange = FloatRange(1e-4)


@dataclass
class Parameters:
    mesh: Mesh = field(default_factory=Mesh)
    run: Run = field(default_factory=Run)
    solvers: Solvers = field(default_factory=Solvers)
    physics: Physics = field(default_factory=Physics)
    polytrope: Polytrope = field(default_factory=Polytrope)
    misc: Misc = field(default_factory=Misc)
    thermal_conduction: ThermalConduction = field(default_factory=ThermalConduction)
    viscosity: Viscosity = field(default_factory=Viscosity)
    h84: H84 = field(default_factory=H84)
    c91: C91 = field(default_factory=C91)

    def write_ini(self, filename: str):
        config = configparser.ConfigParser()
        for section in self.__dataclass_fields__.keys():
            config.add_section(section)
            for field in getattr(self, section).__dataclass_fields__.keys():
                value = getattr(getattr(self, section), field)
                if isinstance(value, (MultipleChoice, Boolean)):
                    value = value.selected_value
                config.set(section, field, str(value))
        with open(filename, 'w') as configfile:
            config.write(configfile)

    def validate(self):
        # ici valider que les valeurs sont dans les bornes
        # ce qui devrait être assuré par les validateurs
        # surtout vérifier que des valeurs ne sont pas incohérentes entre-elles
        pass
