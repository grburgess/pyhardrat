import scipy.integrate as integrate
import astropy.units as u




class HRCalc(object):
    
    def __init__(self, model, ene_lo_min = 50.,ene_lo_max = 300.,ene_hi_min= 300., ene_hi_max=1000.):
        """
        Computes the hardness ratio in photon and energy space given a 3ML model

        :param model:  a 3ML likelihood model
        :param ene_lo_min: min lo energy bound
        :param ene_lo_max: max lo energy bound
        :param ene_hi_min: min hi energy bound
        :param ene_hi_max: max hi energy bound
        """
        
        
        # convert everything to keV
        
        self._ene_lo_min, warn = HRCalc._convert_to_unit(ene_lo_min)
        
        if warn:
            
            RuntimeWarning('Assuming ene_lo_min is in keV')
            
        self._ene_lo_max, warn = HRCalc._convert_to_unit(ene_lo_max)
        
        if warn:
            
            RuntimeWarning('Assuming ene_lo_max is in keV')
            
        self._ene_hi_min, warn = HRCalc._convert_to_unit(ene_hi_min)
        
        if warn:
            
            RuntimeWarning('Assuming ene_hi_min is in keV')
            
        self._ene_hi_max, warn = HRCalc._convert_to_unit(ene_hi_max)
        
        if warn:
            
            RuntimeWarning('Assuming ene_hi_max is in keV')
         
        
        # check we did not fuck up the energies
        
        assert ene_lo_min < ene_lo_max, 'energies are out of order!'
        assert ene_lo_max <= ene_hi_min, 'energies are out of order!'
        assert ene_hi_min < ene_hi_max, 'energies are out of order!'
        
        # save the model call
        
        self._call = lambda ene: model.get_point_source_fluxes(0,ene) # phts/s/cm2/keV
        self._ene_call = lambda ene: model.get_point_source_fluxes(0,ene)*ene # phts/s/cm2/keV
        
        #self._kev2erg = (1*u.keV).to(u.erg).value
        
        self._compute_photon_hardness_ratio()
        self._compute_energy_hardness_ratio()
        
    
    def _compute_photon_hardness_ratio(self):
        
        self._ph_hr_lo = integrate.quad(self._call, self._ene_lo_min, self._ene_lo_max)[0]
        self._ph_hr_hi = integrate.quad(self._call, self._ene_hi_min, self._ene_hi_max)[0]
        self._ph_hr = self._ph_hr_lo/self._ph_hr_hi
        
        
    def _compute_energy_hardness_ratio(self):
        
        self._ene_hr_lo = integrate.quad(self._ene_call, self._ene_lo_min, self._ene_lo_max)[0]
        self._ene_hr_hi = integrate.quad(self._ene_call, self._ene_hi_min, self._ene_hi_max)[0]
        self._ene_hr = self._ene_hr_lo/self._ene_hr_hi
        
        
        
    @property
    def photon_hardness_ratio(self):
        """
        :return : photon hardness ratio 
        """
        
        return self._ph_hr #* self._kev2erg 
    
    @property
    def energy_hardness_ratio(self):
        """
        :return : energy hardness ratio 
        """
        
        return self._ene_hr
        
        
    @staticmethod
    def _convert_to_unit(value):
        
        if isinstance(value,u.Quantity):
            
            value = value.to(u.keV).value
            warn = False
        else:
            
            warn = True
            
        return value, warn
