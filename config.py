__author__ = "aemerick <emerick@astro.columbia.edu>"

# --- external ---
from collections import OrderedDict

# --- internal ---
from constants import CONST as const
import imf as imf


#
# --------- Superclass for all parameters -------
#
class _parameters:

    def __init__(self):
        pass

    def help(self):
        print self.__doc__

    def reset_parameters_to_default(self):
        self.__init__()

#
# ----------- Units ----------------------
#
class _units(_parameters):
    """
    Units:

        Set the conversions between code units and 'base'
        quantities. For the sake of the onezone code,
        the base unit of time is in seconds and the base unit
        of mass is in solar masses. Therefore, in order to 
        set the time units to Myr (default) and mass units
        to solar masses (default), one would just do:

            >>> units.time = 3.1536E13
            >>> units.mass = 1.0

        Output masses are always in solar, while everything else (e.g.
        luminosity) is in cgs, regardless of what the code units are 
        set to.
    """

    def __init__(self):
        self.time      = const.yr_to_s * 1.0E6
        self.mass      = 1.0

        return

units = _units()
#
# -------- Global Zone Parameters ------- 
#
class _zone_parameters(_parameters):
    """
    Zone Parameters:

        The below is a list of all parameters that are set
        by the zone, including default values. Parameters
        are listed in order of : 1) required, 2) not required but
        highly suggested, or 3) optional

        Required Parameters:

        initial_gas_mass (float) : initial gas mass in solar masses
        initial_dark_matter_mass (float) : DM mass of halo in solar
        initial_metallicity (float)      : initial gas metal fraction
        dt (float)                       : constant timestep size in code time
        t_final (float)                  : time to end simulation
        

        Suggested Parameters:

        imf (function) : IMF function used to generate stars. Currently
            function must be one of the imf functional forms defined
            in the ``imf'' module, but user can supply their own.
            Default imf.salpeter()

        star_formation_method (int) : switch between star formation
            schemes:

            1) constant, uniform SFR throughout evolution
            2) SFR computed cosmologically
            3) SFH table provided using SFH_filename parameter where
               either two columns are provided, time and SFR, or 
               time and stellar mass. Column headers must be named
               appropriately as ("time" or "SFR" or "mass").

         use_SF_mass_reservoir (bool , optional) : One of two ways to deal with low
             SFR's to ensure accurate sampling of the IMF (see the second
             below). Make sure you understand these parameters and their
             implications before setting -- know also that they may need to 
             be set in certain situations. This parameter turns on the
             reservoir method whereby M_sf = dt * SFR is added to a 
             reservoir each timestep. If the reservoir exceeds the 
             mass threshold ``SF_mass_reservoir_size'', SF occurs in that timestep
             using up all of the reservoir. This may lead to bursty, intermittent SF
             depnding on size of resivoir. Default = False

         use_stochastic_mass_sampling (bool, optional) : Second and preferred method to deal
             with low SFR's. Prevent normal SF if M_sf = dt * SFR is below some threshold
             value, ``stochastic_sample_mass''. Instead of shutting off SF that
             timestep completely, however, and instead of accumulating mass in a
             reseroir, compute the probablility that a chunk of gas of mass
             ``stochastic_sample_mass'' is made into stars that timestep as
             P = M_sf / stochastic_sample_mass . That chunk is then formed
             completely into stars using a random number draw. Default is True

         SF_mass_reservoir_size (float, optional) : Size of accumulation reservoir used with
         ``use_SF_mass_reservoir''. Default is 1000.0

         stochastic_sample_mass (float, optional) : Size of mass chunk allowed to form
             stochastically when SFR is low. Be careful setting this to too large
             a value. Not recommended to set below ~200.0 Msun depending
             on one's choice of maximum star particle mass. Default is 250.0.

         inflow_factor  (float, optional) : Sets the mass inflow rate as a function of 
             the star formation rate. Default 0.05

         mass_loading_factor (float, optional) : Sets the mass outlflow rate as a function of
             the star formation rate. Default 0.1

         SFR_efficiency (float, optional) : For cosmologically derived SFR's, sets the 
             star formation rate efficiency of converging gas to stars in a free fall time
             Default is 0.01

         Optional:
        
         t_o     (float, optional) : initial time. Default is 0.0
         t_final (float, optional) : simulation end time. Default is 10 Gyr
         
    """

    def __init__(self):
        self.initial_gas_mass         = 0.0
        self.initial_dark_matter_mass = 0.0
        self.initial_metallicity      = 0.0
        self.species_to_track         = OrderedDict()
        self.initial_abundances       = None

        self.imf                      = imf.salpeter()
        self.star_formation_method    = 1          # 1, 2, 3
        self.SFH_filename             = None
        self.constant_SFR             = 10.0        # code mass / code time

        self.cosmological_evolution   = False       # on or off

        self.use_SF_mass_reservoir     = False
        self.SF_mass_reservoir_size    = 1000.0

        self.use_stochastic_mass_sampling = True
        self.stochastic_sample_mass   = 250.0


        # - inflow, outflow, and efficiency parameters
        self.inflow_factor            = 0.05
        self.mass_loading_factor      = 0.1
        self.SFR_efficiency           = 0.01

        self.t_o                      = 0.0             # Myr
        self.t_final                  = 1.0E4           # Myr
        self.dt                       = 1.0             # Myr


        # assert time units here

zone = _zone_parameters()

#
# ----------------- Stars and Stellar Evolution ------------------
#
class _star_particle_parameters(_parameters):
    """
    Star and Stellar Physics Parameters:

        The below is a list of all parameters that are set to be 
        used in evolving stars and controlling the underlying stellar
        physics properties.

        SNII_mass_threshold (float) : Lower mass limit for stars to
            explode as a Type II supernovae at the end of their life.
            Default is 8.0

        SNIa_candidate_mass_bounds (list or array of floats) : Size
            two (lower and upper bound) boundaries for mass range where
            stars turn into WD's that are candidates for exploding as
            Type 1a. Default [3.0, 8.0]

        DTD_slope (float) : Slope of the delay time distribution (DTD)
            model used to compute probability of SNIa candidates 
            exploding as SNIa in a given timestep. Slope is beta,
            where probability goes as t^(-beta). Default 1.0

        NSNIa (float) : Fraction of SNIa candidates that will explode
            as Type Ia supernovae in a hubble time. Default 0.043

    """

    def __init__(self):
    
        self.SNII_mass_threshold           = 8.0    
        self.SNIa_candidate_mass_bounds    = [3.0, 8.0]

        self.DTD_slope                     = 1.0
        self.NSNIa                         = 0.043

        self.use_AGB_wind_phase            = True
        self.AGB_wind_phase_mass_threshold = 8.0
        

        self.normalize_black_body_to_OSTAR = True
        self.black_body_correction_mass    = 20.0
        self.black_body_q0_factors         = const.black_body_q0
        self.black_body_q1_factors         = const.black_body_q1
        self.black_body_FUV_factors        = const.black_body_fuv


stars = _star_particle_parameters()
#
# ----------------- Input and Output --------------
#
class _io_parameters(_parameters):

    def __init__(self):
        self.dump_output_basename     = 'dump'
        self.dt_dump                  = 0.0
        self.cycle_dump               = 0

        self.summary_output_filename  = 'summary_output.txt' 
        self.dt_summary               = 0.0
        self.cycle_summary            = 0

io  = _io_parameters()

#
# ------------- Helper Functions -------------
#

def information():
    """
    Welcome to the configuration parameters for the onezone
    chemical enrichment model. Parameters are classified by
    whether or not they belong to the more global onezone gas
    reservoir, the stars (and stellar physics) itself, or 
    input/output. The parameters can be accessed and modified
    as attributes of the following objects:
 
        Zone            :    zone
        Stars           :    stars
        Input / Output  :    io
        
    More information about these parameters can be found by
    calling the help method on a given object, e.g.:
         zone.help()
    which will print an explanation about each parameter, whether or 
    not it requires user to set (i.e. will fail if defaults are kept),
    and its default value.

    Call the 'help' function in this module to see a description of
    all parameters at once.
    """

    print information.__doc__

def help():
    """
    Print the docstrings for all config parameter types.
    """

    for obj in [zone, stars, io]:
        obj.help()

    return

def reset_all_parameters():
    """
    Reset all parameter types to their default values
    """

    for obj in [zone, stars, io]:
        obj.reset_parameters_to_default()

    print "ALL parameters reset to default"

    return