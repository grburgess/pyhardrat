from threeML.io.file_utils import if_directory_not_existing_then_make, file_existing_and_readable
from threeML import FermiGBMBurstCatalog

from hr_calc import HRCalc

import matplotlib.pyplot as plt
import pandas as pd


class HardnessDurationBuilder(object):
    
    def __init__(self):
        
        self._catalog = FermiGBMBurstCatalog()
       
    @property
    def catalog(self):
        
        return self._catalog
    
    @property
    def hr_table(self):
        
        return self._df
    
    def plot_photon(self,color_classes=True):
        """
        Plot the HR vs T90 for photon
        :param color_classes: (bool) color the classes separately
        """
        fig, ax = plt.subplots()
        
        if color_classes:
            
            # divide the classes
            
            short = self._df['T90']<2.
            
            ax.scatter(self._df['T90'][short],self._df['photon HR'][short],c='#66c2a5',label='sGRBs')
            
            ax.scatter(self._df['T90'][~short],self._df['photon HR'][~short],c='#fc8d62',label='LGRBs')
   
            ax.legend()
            
        else:
            
            ax.scatter(self._df['T90'],self._df['photon HR'],c='#8da0cb')
        
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.set_xlabel('T90')
        ax.set_ylabel('Photon Hardness Ratio')
        
        return fig
    
    
    def plot_energy(self,color_classes=True):
        """
        Plot the HR vs T90 for energy
        :param color_classes: (bool) color the classes separately
        """
        
        fig, ax = plt.subplots()
        
        if color_classes:
            
            # divide the classes
            
            short = self._df['T90']<2.
            
            ax.scatter(self._df['T90'][short],self._df['energy HR'][short],c='#e41a1c',label='sGRBs')
            
            ax.scatter(self._df['T90'][~short],self._df['energy HR'][~short],c='#377eb8',label='LGRBs')
   
            ax.legend()
            
        else:
            
            ax.scatter(self._df['T90'],self._df['energy HR'],c='#4daf4a')
        
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.set_xlabel('T90')
        ax.set_ylabel('Energy Hardness Ratio')
        
        return fig
            
            
        
        
   
            
    def build_sample(self,interval='fluence'):
        """
        Build the models after a query
        :param interval: peak of fluence spectrum

        """
        
        if interval == 'fluence':
        
        
            best_fit_model= [x.split('_')[-1] for x in self._catalog.result['flnc_best_fitting_model']]
            
        elif interval == 'peak':
            
            best_fit_model= [x.split('_')[-1] for x in self._catalog.result['pflx_best_fitting_model']]
            
        else:
            
            RuntimeError('peak or fluence')
        
        
            
        self._t90 = []
        self._models = []
        self._grbs = []
        
        grbs_to_use = self._catalog.result.index
        
        
        for grb, bfm in zip(grbs_to_use, best_fit_model):
            
            if bfm:
            
                self._catalog.query_sources(grb)
                
                self._t90.append(self._catalog.result['t90'][grb])
            
                self._models.append(self._catalog.get_model(bfm,interval)[grb])
        
                self._grbs.append(grb)
            
        
            
        
        
        
    
        
    
    def compute_hardness_ratios(self, ene_lo_min = 50.,ene_lo_max = 300.,ene_hi_min= 300., ene_hi_max=1000.):
        
        self._hardrats = [] 
        
        for model in self._models:
            
            self._hardrats.append(HRCalc(model, ene_lo_min ,ene_lo_max ,ene_hi_min, ene_hi_max))
            
        df_dict = {}
        
        df_dict['T90'] = self._t90
        
        df_dict['photon HR'] = []
        df_dict['energy HR'] = []
        
        for hr in self._hardrats:
            
            df_dict['photon HR'].append(hr.photon_hardness_ratio)
            df_dict['energy HR'].append(hr.energy_hardness_ratio)
            
            
        self._df = pd.DataFrame(data=df_dict,index=self._grbs)
            
