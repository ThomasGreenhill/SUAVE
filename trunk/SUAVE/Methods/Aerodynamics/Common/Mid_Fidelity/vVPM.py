## @ingroup Methods-Aerodynamics-Common-Mid_Fidelity
# vVPM.py
# 
# Created:  Dec 2020, R. Erhard
#           

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# package imports 
import numpy as np 
from SUAVE.Core import Data
from SUAVE.Methods.Aerodynamics.Common.Mid_Fidelity.discretize_vortex_particles              import discretize_vortex_particles
from SUAVE.Methods.Aerodynamics.Common.Mid_Fidelity.compute_particle_induced_velocities      import compute_particle_induced_velocities
from SUAVE.Methods.Aerodynamics.Common.Mid_Fidelity.update_particle_positions                import update_particle_positions
from SUAVE.Methods.Aerodynamics.Common.Mid_Fidelity.vorticity_evolution                      import vorticity_evolution
from SUAVE.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_wing_vortex_distribution  import generate_wing_vortex_distribution

# Four functions to calculate the induced velocity, the vortex stretching term, the diffusion term and udating the circulation strength after each time step

#The vortex particles are vector elements (vorticity vector x volume). The element is convected with the fluid velocity,
# and the strength vector is stretched according to the velocity gradient tensor.

# A vortex particle is essentially a discretization of a vortex filament. Since they are not connected as in a vortex filament, the vorticity field represented 
# by a collection of vortex particles does not necessarily remain divergence free all times.

# Each vortex particle has an associated position vector, strength vector (=vorticity x volume), and in some cases a core size



def vVPM(conditions,settings,geometry):
    # Discretize vortex particles and initialize their strength
    vp_positions = discretize_vortex_particles()
    
    time_steps = 100
    N_particles = 100
    
    # generate vortex distribution on the surface
    VD   = generate_wing_vortex_distribution(geometry,settings)  
    
    # Define the control point locations on wing:
    x = VD.XC 
    y = VD.YC
    z = VD.ZC
    x_vec = np.array([VD.XC[i],VD.YC[i],VD.ZC[i]] for i in range(len(VD.XC)))
    
    # Initialize particle locations and strengths
    particles = Data()
    particles.positions = 
    particles.strengths = 
    
    vp_induced_velocities = np.zeros(N_particles,time_steps)
    vp_positions = np.zeros(N_particles,time_steps)
    vp_vorticity = np.zeros(N_particles,time_steps)
    
    for t in range(time_steps):
        # Evaluate the induced velocities using the Biot-Savart kernel
        vp_induced_velocities[:,t] = compute_particle_induced_velocities(x_vec,particles)
        
        # Update the particle positions due to convection and diffusion of particles (PSE)
        vp_positions[:,t] = update_particle_positions()
        
        # Evolve the vorticity by one time step:
        vp_vorticity[:,t] = vorticity_evolution()
    
    
    # Use the velocities to compute the wing lift, drag, etc.
    
    # --------------------------------------------------------------------------------------------------------
    # LIFT                                                                          
    # --------------------------------------------------------------------------------------------------------    
    # lift coefficients on each wing   
    L_wing            = np.sum(np.multiply(u_n_w+1,(gamma_n_w*Del_Y_n_w)),axis=2).T
    CL_wing           = L_wing/(0.5*wing_areas)
    
    # Calculate spanwise lift 
    spanwise_Del_y    = Del_Y_n_w_sw[:,:,0]
    spanwise_Del_y_w  = np.array(np.array_split(Del_Y_n_w_sw[:,:,0].T,n_w,axis = 1))
    
    cl_y              = (2*(np.sum(gamma_n_w_sw,axis=2)*spanwise_Del_y).T)/CS
    cl_y_w            = np.array(np.array_split(cl_y ,n_w,axis=1)) 
    
    # total lift and lift coefficient
    L                 = np.atleast_2d(np.sum(np.multiply((1+u),gamma*Del_Y),axis=1)).T 
    CL                = L/(0.5*Sref)   # validated form page 402-404, aerodynamics for engineers
    
    # --------------------------------------------------------------------------------------------------------
    # DRAG                                                                          
    # --------------------------------------------------------------------------------------------------------         
    # drag coefficients on each wing   
    w_ind_sw_w        = np.array(np.array_split(np.sum(w_ind_n_w_sw,axis = 2).T ,n_w,axis = 1))
    Di_wing           = np.sum(w_ind_sw_w*spanwise_Del_y_w*cl_y_w*CS_w,axis = 2) 
    CDi_wing          = Di_wing.T/(wing_areas)  
    
    # total drag and drag coefficient 
    spanwise_w_ind    = np.sum(w_ind_n_w_sw,axis=2).T    
    D                 = np.sum(spanwise_w_ind*spanwise_Del_y.T*cl_y*CS,axis = 1) 
    cdi_y             = spanwise_w_ind*spanwise_Del_y.T*cl_y*CS
    CDi               = np.atleast_2d(D/(Sref)).T  
    
    # --------------------------------------------------------------------------------------------------------
    # PRESSURE                                                                      
    # --------------------------------------------------------------------------------------------------------          
    L_ij              = np.multiply((1+u),gamma*Del_Y) 
    CP                = L_ij/VD.panel_areas  
    
    # --------------------------------------------------------------------------------------------------------
    # MOMENT                                                                        
    # --------------------------------------------------------------------------------------------------------             
    CM                = np.atleast_2d(np.sum(np.multiply((X_M - VD.XCH*ones),Del_Y*gamma),axis=1)/(Sref*c_bar)).T     
        
    
    return CL, CDi, CP, CM, cl_y, cdi_y
