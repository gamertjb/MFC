#!/usr/bin/env python3
import math
import json

# -- Physical constants ------------------------------------------------------

pA = 101598.0
rhoA = 1.18               # air density
gamma_air = 1.4
c1 = math.sqrt(gamma_air * pA / rhoA)

pW = pA                   # water pressure
velJ = 12.01
rhoW = 1000.0             # liquid water density
muW = 1.0e-3              # dynamic viscosity of water
rho_vapor = 0.6          # water-vapor density

# Reference bubble properties and void fraction for dense Eulerian cloud
R0ref = 10e-6             # reference bubble radius
vapor_frac = 0.4          # bubble void fraction in injected water
pv = 2300.0               # vapor pressure
sigma_lw = 0.0794         # surface tension between water & air

# Nondimensional numbers for Eulerian bubble model
Ca = (pW - pv) / (rhoW * velJ**2)
We = rhoW * velJ**2 * R0ref / sigma_lw
Re_inv = muW / (rhoW * velJ * R0ref)

# -- Grid / time setup -------------------------------------------------------

djet = 100e-6
leng = 20 * djet            # domain length in x
Ny = 1000
Nx = 2500
dx = leng / Nx

time_end = 2.0e-4
cfl = 0.5

dt = 2 * 2 * cfl * dx / c1
Nt = int(time_end / dt)

eps = 1.0e-6              # regularization

# -- Dump JSON ----------------------------------------------------------------

print(
    json.dumps(
        {
            # Logistics
            "run_time_info": "T",
            # Domain
            "x_domain%beg": 0.0,
            "x_domain%end": 20 * djet,
            "y_domain%beg": -10 * djet,
            "y_domain%end": 10 * djet,
            "m": Nx,
            "n": Ny,
            "p": 0,
            "dt": dt,
            "cfl_adap_dt": "T",
            "t_stop": time_end,
            "t_save": time_end / 200,
            "t_step_save": 2000,
            "n_start": 0,
            "cfl_target": 1.0,
            # Numerics
            "num_patches": 2,
            "model_eqns": 2,
            "alt_soundspeed": "F",
            # Only water and air are treated as continuum fluids;
            # the vapor cloud is represented by the Eulerian bubble model
            "num_fluids": 3,
            "mpp_lim": "F",
            "mixture_err": "T",
            "bubbles_euler": "T",
            "bubble_model": 2,
            "polytropic": "T",
            "polydisperse": "F",
            "R0_type": 1,
            "thermal": 3,
            "R0ref": R0ref,
            "nb": 1,
            "Ca": Ca,
            "Web": We,
            "Re_inv": Re_inv,
            #"relax": "T",
            #"relax_model": 6,
            #"palpha_eps": 1.0e-2,
            #"ptgalpha_eps": 1.0e-2,
            "time_stepper": 3,
            "weno_order": 3,
            "weno_eps": 1.0e-16,
            "weno_Re_flux": "F",
            "wenoz": "T",
            "weno_avg": "F",
            "null_weights": "F",
            "mp_weno": "F",
            "riemann_solver": 2,
            "wave_speeds": 1,
            "avg_state": 2,
            "surface_tension": "T",
            "sigma": sigma_lw,
            "elliptic_smoothing": "T",
            "elliptic_smoothing_iters": 50,
            # BCs
            "bc_x%beg": -2,
            "bc_x%end": -3,
            "bc_y%beg": -3,
            "bc_y%end": -3,
            "num_bc_patches": 1,
            "patch_bc(1)%dir": 1,
            "patch_bc(1)%loc": -1,
            "patch_bc(1)%geometry": 1,
            "patch_bc(1)%type": -17,
            "patch_bc(1)%centroid(2)": 0.0,
            "patch_bc(1)%length(2)": djet,
            # I/O
            "format": 1,
            "precision": 2,
            "prim_vars_wrt": "T",
            "cf_wrt": "T",
            "parallel_io": "T",

            # -- Patch 1: Cross-flow (air is fluid 2) --------------------------
            "patch_icpp(1)%geometry": 3,
            "patch_icpp(1)%x_centroid": 0.5 * leng,
            "patch_icpp(1)%y_centroid": 0.0,
            "patch_icpp(1)%length_x": leng,
            "patch_icpp(1)%length_y": 20 * djet,
            "patch_icpp(1)%vel(1)": 0.0,
            "patch_icpp(1)%vel(2)": 116.0,
            "patch_icpp(1)%pres": pA,
            # fluid 1 (water) absent
            "patch_icpp(1)%alpha_rho(1)": eps,
            "patch_icpp(1)%alpha(1)": eps,
            # fluid 2 (air) full
            "patch_icpp(1)%alpha_rho(2)": rhoA,
            "patch_icpp(1)%alpha(2)": 1.0 - 2.0 * eps,
            # fluid 3 (vapor) absent
            "patch_icpp(1)%alpha_rho(3)": eps,
            "patch_icpp(1)%alpha(3)": eps,
            "patch_icpp(1)%r0": 1.0,
            "patch_icpp(1)%v0": 0.0,
            "patch_icpp(1)%cf_val": 0,

            # -- Patch 2: Water jet seeded with dense vapor cloud -------------
            "patch_icpp(2)%geometry": 3,
            "patch_icpp(2)%alter_patch(1)": "T",
            "patch_icpp(2)%x_centroid": 20 * dx,
            "patch_icpp(2)%y_centroid": 0.0,
            "patch_icpp(2)%length_x": 40 * dx,
            "patch_icpp(2)%length_y": djet,
            "patch_icpp(2)%vel(1)": velJ,
            "patch_icpp(2)%vel(2)": 0.0,
            "patch_icpp(2)%pres": pW,
            # fluid 1 (water) with dense bubble cloud
            "patch_icpp(2)%alpha_rho(1)": (1.0 - vapor_frac) * rhoW,
            "patch_icpp(2)%alpha(1)": 1.0 - vapor_frac,
            # fluid 2 (air) absent
            "patch_icpp(2)%alpha_rho(2)": eps,
            "patch_icpp(2)%alpha(2)": eps,
            # fluid 3 (vapor) present
            "patch_icpp(2)%alpha_rho(3)": vapor_frac * rho_vapor,
            "patch_icpp(2)%alpha(3)": vapor_frac,
            "patch_icpp(2)%r0": 1.0,
            "patch_icpp(2)%v0": 0.0,
            "patch_icpp(2)%cf_val": 1,

            # -- Fluid EOS (1=water, 2=air, 3=bubble gas) ----------------------
            "fluid_pp(1)%gamma": 1.0 / (6.3 - 1.0),   # liquid water
            "fluid_pp(1)%pi_inf": 3.43e8,
            "fluid_pp(2)%gamma": 1.0 / (1.4 - 1.0),   # air
            "fluid_pp(2)%pi_inf": 0.0,
            "fluid_pp(3)%gamma": 1.0 / (1.33 - 1.0),  # bubble vapor
            "fluid_pp(3)%pi_inf": 0.0,

        }
    )
)
