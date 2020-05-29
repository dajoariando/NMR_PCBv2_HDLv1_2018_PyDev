'''
Created on May 04, 2020

This module characterizes the preamp gain and show the gain over frequency

@author: David Ariando
'''

import os
import time
from nmr_std_function.nmr_functions import compute_iterate
from nmr_std_function.nmr_functions import compute_gain
from nmr_std_function.data_parser import parse_simple_info
from nmr_std_function.nmr_class import tunable_nmr_system_2018

# variables
data_parent_folder = "/root/NMR_DATA"
en_remote_dbg = 0
fig_num = 1
en_fig = 1

# measurement properties
sta_freq = 1
sto_freq = 10
spac_freq = 0.05
samp_freq = 25

# instantiate nmr object
nmrObj = tunable_nmr_system_2018( data_parent_folder, en_remote_dbg )

# system setup
nmrObj.initNmrSystem()  # necessary to set the GPIO initial setting

nmrObj.assertControlSignal( nmrObj.PSU_5V_TX_N_EN_msk |
                           nmrObj.PSU_5V_ADC_EN_msk | nmrObj.PSU_5V_ANA_P_EN_msk |
                           nmrObj.PSU_5V_ANA_N_EN_msk )

nmrObj.deassertControlSignal( nmrObj.RX_IN_SEL_1_msk | nmrObj.RX_IN_SEL_2_msk | nmrObj.PAMP_IN_SEL_RX_msk | nmrObj.PAMP_IN_SEL_TEST_msk )

nmrObj.setPreampTuning( -2.7, -0.4 )  # try -2.7, -1.8 if fail
nmrObj.setMatchingNetwork( 0, 0 )
nmrObj.setMatchingNetwork( 0, 0 )

while True:
    nmrObj.assertControlSignal( nmrObj.RX_IN_SEL_2_msk | nmrObj.PAMP_IN_SEL_TEST_msk )
    nmrObj.assertControlSignal( nmrObj.AMP_HP_LT1210_EN_msk | nmrObj.PSU_15V_TX_P_EN_msk | nmrObj.PSU_15V_TX_N_EN_msk )
    time.sleep( 0.1 )

    nmrObj.wobble( sta_freq, sto_freq, spac_freq, samp_freq )

    nmrObj.deassertControlSignal( nmrObj.RX_IN_SEL_2_msk | nmrObj.PAMP_IN_SEL_TEST_msk )
    nmrObj.deassertControlSignal( nmrObj.AMP_HP_LT1210_EN_msk | nmrObj.PSU_15V_TX_P_EN_msk | nmrObj.PSU_15V_TX_N_EN_msk )

    meas_folder = parse_simple_info( data_parent_folder, 'current_folder.txt' )

    maxS21, maxS21_freq, _ = compute_gain( nmrObj, data_parent_folder, meas_folder[0], en_fig, fig_num )
    print( 'maxS21={0:0.2f} maxS21_freq={1:0.2f}'.format( 
         maxS21, maxS21_freq ) )
