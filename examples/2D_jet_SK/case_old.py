import math
import json

pA = 101598.0
rhoA = 1.18   
gam = 1.4
c1 = math.sqrt(1.4*pA/rhoA)

pW = 1.0 * pA
velJ = 12.01
rhoW = 1000.0

leng=1e-3
djet = 100e-6
Ny = 1000
Nx = 2500
dx = leng/Nx

time_end = 2.0e-04
cfl = 0.5

dt=cfl * dx / c1
Nt=int(time_end/dt)

eps=0.000001

#Case dictionary

print(
        json.dumps(
            {
                #Logistics
                "run_time_info": "T",
                #Computational domain parameters
                "x_domain%beg": 0.0,
                "x_domain%end": 20*djet,
                "y_domain%beg": -10*djet,
                "y_domain%end": 10*djet,
                "m": int(Nx),
                "n": int(Ny),
                "p": 0,
                "dt": dt,
                "cfl_adap_dt": "T",
                "t_stop": time_end,
                "t_save": time_end/20,
                "n_start":0,
                "cfl_target": 1.0,
                #Simulation algorithm parameters
                "num_patches": 2,
                "model_eqns":3,
                "alt_soundspeed": "F",
                "num_fluids": 2,
                "mpp_lim": "T",
                "mixture_err": "T",
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
                "elliptic_smoothing":"T",
                "elliptic_smoothing_iters": 50,
                "bc_x%beg":-2,
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
                #Formatted Database File Structures
                "format": 1,
                "precision": 2,
                "prim_vars_wrt": "T",
                "cf_wrt": "T",
                "parallel_io": "T",
                #Patch 1: Initial
                "patch_icpp(1)%geometry": 3,
                "patch_icpp(1)%x_centroid": 0.0,
                "patch_icpp(1)%y_centroid":0.0,
                "patch_icpp(1)%length_x": 10*leng,
                "patch_icpp(1)%length_y": 10*leng,
                "patch_icpp(1)%vel(1)": 0.0,
                "patch_icpp(1)%vel(2)": 116.0,
                "patch_icpp(1)%pres": pA,
                "patch_icpp(1)%alpha_rho(1)": rhoA,
                "patch_icpp(1)%alpha(1)": 1.0-eps,
                "patch_icpp(1)%cf_val": 0,
                "patch_icpp(1)%alpha_rho(2)":eps,
                "patch_icpp(1)%alpha(2)": eps,
                #Patch 2: Jet
                "patch_icpp(2)%geometry": 3,
                "patch_icpp(2)%alter_patch(1)": "T",
                "patch_icpp(2)%x_centroid": 0.0,
                "patch_icpp(2)%y_centroid": 0.0,
                "patch_icpp(2)%length_x": 40*dx,
                "patch_icpp(2)%length_y": djet,
                "patch_icpp(2)%vel(1)": velJ,
                "patch_icpp(2)%vel(2)": 0.0,
                "patch_icpp(2)%pres": pW,
                "patch_icpp(2)%alpha_rho(1)": eps,
                "patch_icpp(2)%alpha(1)": eps,
                "patch_icpp(2)%alpha_rho(2)":(1.0-eps)*rhoW,
                "patch_icpp(2)%alpha(2)": 1.0-eps,
                "patch_icpp(2)%cf_val": 1,
                #Fluid properties
                "fluid_pp(1)%gamma": 1.00/(1.4-1.0),
                "fluid_pp(1)%pi_inf": 0.0,
                "fluid_pp(2)%gamma": 1.0/(6.3-1.0),
                "fluid_pp(2)%pi_inf": 3.43e8,
                "sigma": 0.0794,
                }
            )
        )
