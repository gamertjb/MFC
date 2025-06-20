#!/usr/bin/env python3
import json
import math

# Basic dimensional parameters (SI units)
Lx = 0.05   # domain length in x
Ly = 0.05   # domain length in y
Lz = 0.20   # domain length in z

# Crossflow velocity (in +z)
Ucf = 5.0

# Jet parameters
jet_radius = 0.005
jet_length = 0.05  # along x direction
Ujet = 10.0

# Thermodynamic properties (stiffened-gas) for water and its vapor
# Values are representative and can be adjusted as needed
p0 = 1.0e5
T0 = 300.0

# Liquid water properties
gamma_l = 6.12
pi_inf_l = 3.43e8
cv_l = 4181.0
qv_l = -2.3e6
qvp_l = 0.0
rho_l = (p0 + pi_inf_l)/((gamma_l-1.0)*cv_l*T0)

# Water vapor properties
gamma_v = 1.4
pi_inf_v = 0.0
cv_v = 1410.0
qv_v = 2.0e6
qvp_v = -23400.0
rho_v = (p0 + pi_inf_v)/((gamma_v-1.0)*cv_v*T0)

# Air properties
gamma_a = 1.4
pi_inf_a = 0.0
cv_a = 717.0
rho_a = (p0 + pi_inf_a)/((gamma_a-1.0)*cv_a*T0)

# Volume fractions for crossflow (mostly air)
alpha_l_cf = 0.0
alpha_v_cf = 0.0
alpha_a_cf = 1.0

# Volume fractions for jet (liquid with some vapor)
alpha_l_jet = 0.95
alpha_v_jet = 0.05
alpha_a_jet = 0.0

# Simulation parameters
m = 64
n = 64
p = 256
CFL = 0.5

dt = CFL * (Lx/m) / max(Ucf, Ujet)
Nt = 1000
AS = 100

print(
    json.dumps(
        {
            "run_time_info": "T",
            "x_domain%beg": -Lx/2,
            "x_domain%end": Lx/2,
            "y_domain%beg": -Ly/2,
            "y_domain%end": Ly/2,
            "z_domain%beg": 0.0,
            "z_domain%end": Lz,
            "m": m,
            "n": n,
            "p": p,
            "cyl_coord": "F",
            "dt": dt,
            "t_step_start": 0,
            "t_step_stop": Nt,
            "t_step_save": AS,
            "num_patches": 2,
            "model_eqns": 3,
            "num_fluids": 3,
            "mixture_err": "T",
            "relax": "T",
            "relax_model": 6,
            "palpha_eps": 1.0e-8,
            "ptgalpha_eps": 1.0e-2,
            "time_stepper": 3,
            "weno_order": 3,
            "mapped_weno": "T",
            "riemann_solver": 2,
            "wave_speeds": 1,
            "avg_state": 2,
            "bc_x%beg": -2,
            "bc_x%end": -2,
            "bc_y%beg": -2,
            "bc_y%end": -2,
            "bc_z%beg": -6,
            "bc_z%end": -6,
            "format": 1,
            "precision": 2,
            "prim_vars_wrt": "T",
            "parallel_io": "T",
            # Patch 1: crossflow
            "patch_icpp(1)%geometry": 9,
            "patch_icpp(1)%x_centroid": 0.0,
            "patch_icpp(1)%y_centroid": 0.0,
            "patch_icpp(1)%z_centroid": Lz/2,
            "patch_icpp(1)%length_x": Lx,
            "patch_icpp(1)%length_y": Ly,
            "patch_icpp(1)%length_z": Lz,
            "patch_icpp(1)%vel(1)": 0.0,
            "patch_icpp(1)%vel(2)": 0.0,
            "patch_icpp(1)%vel(3)": Ucf,
            "patch_icpp(1)%pres": p0,
            "patch_icpp(1)%alpha_rho(1)": alpha_l_cf*rho_l,
            "patch_icpp(1)%alpha_rho(2)": alpha_v_cf*rho_v,
            "patch_icpp(1)%alpha_rho(3)": alpha_a_cf*rho_a,
            "patch_icpp(1)%alpha(1)": alpha_l_cf,
            "patch_icpp(1)%alpha(2)": alpha_v_cf,
            "patch_icpp(1)%alpha(3)": alpha_a_cf,
            # Patch 2: jet cylinder oriented along x
            "patch_icpp(2)%geometry": 10,
            "patch_icpp(2)%x_centroid": -Lx/2 + jet_length/2,
            "patch_icpp(2)%y_centroid": 0.0,
            "patch_icpp(2)%z_centroid": Lz/2,
            "patch_icpp(2)%radius": jet_radius,
            "patch_icpp(2)%length_x": jet_length,
            "patch_icpp(2)%vel(1)": Ujet,
            "patch_icpp(2)%vel(2)": 0.0,
            "patch_icpp(2)%vel(3)": 0.0,
            "patch_icpp(2)%pres": p0,
            "patch_icpp(2)%alpha_rho(1)": alpha_l_jet*rho_l,
            "patch_icpp(2)%alpha_rho(2)": alpha_v_jet*rho_v,
            "patch_icpp(2)%alpha_rho(3)": alpha_a_jet*rho_a,
            "patch_icpp(2)%alpha(1)": alpha_l_jet,
            "patch_icpp(2)%alpha(2)": alpha_v_jet,
            "patch_icpp(2)%alpha(3)": alpha_a_jet,
            "patch_icpp(2)%alter_patch(1)": "T",
            # Fluid properties
            "fluid_pp(1)%gamma": 1.0/(gamma_l-1.0),
            "fluid_pp(1)%pi_inf": gamma_l*pi_inf_l/(gamma_l-1.0),
            "fluid_pp(1)%cv": cv_l,
            "fluid_pp(1)%qv": qv_l,
            "fluid_pp(1)%qvp": qvp_l,
            "fluid_pp(2)%gamma": 1.0/(gamma_v-1.0),
            "fluid_pp(2)%pi_inf": gamma_v*pi_inf_v/(gamma_v-1.0),
            "fluid_pp(2)%cv": cv_v,
            "fluid_pp(2)%qv": qv_v,
            "fluid_pp(2)%qvp": qvp_v,
            "fluid_pp(3)%gamma": 1.0/(gamma_a-1.0),
            "fluid_pp(3)%pi_inf": gamma_a*pi_inf_a/(gamma_a-1.0),
            "fluid_pp(3)%cv": cv_a,
        }
    )
)

