#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Spectrum
# Generated: Fri Jun 29 09:30:58 2018

#Edited by Danny Jacobs
# June 2018

##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter as gr_filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import time


class spectrum(gr.top_block):

    def __init__(self,FFT_size,SDR_BW):
        gr.top_block.__init__(self, "Spectrum")

        ##################################################
        # Variables
        ##################################################
        self.tuning = tuning = 0
        self.samp_rate = samp_rate = 200e6
        self.integration_time = integration_time = 100
        self.data_address = data_address = "tcp://127.0.0.1:5555"
        self.SDR_BW = SDR_BW
        self.FFT_size = FFT_size #take the FFT_size from the input

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_gr_complex, FFT_size, data_address, 100, False, -1)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_subdev_spec("B:0", 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(tuning, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.fft_vxx_0 = fft.fft_vcc(FFT_size, True, (window.blackmanharris(FFT_size)), True, 1)
        self.dc_blocker_xx_0 = gr_filter.dc_blocker_cc(32, True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, FFT_size)
        #self.blocks_integrate_xx_0 = blocks.integrate_cc(1, FFT_size)

        ##################################################
        # Connections
        ################################################## 
        self.connect((self.uhd_usrp_source_0, 0), (self.dc_blocker_xx_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
	#self.connect((self.uhd_usrp_source_0,0),(self.blocks_stream_to_vector_0,0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0)) 
        self.connect((self.fft_vxx_0, 0), (self.zeromq_push_sink_0, 0))  
 

#        self.connect((self.blocks_integrate_xx_0, 0), (self.zeromq_push_sink_0, 0))    
#        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
#        self.connect((self.fft_vxx_0, 0), (self.blocks_integrate_xx_0, 0))    
#        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_stream_to_vector_0, 0))    

    def get_tuning(self):
        return self.tuning

    def set_tuning(self, tuning):
        self.tuning = tuning
        self.uhd_usrp_source_0.set_center_freq(self.tuning, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_integration_time(self):
        return self.integration_time

    def set_integration_time(self, integration_time):
        self.integration_time = integration_time

    def get_data_address(self):
        return self.data_address

    def set_data_address(self, data_address):
        self.data_address = data_address

    def get_SDR_BW(self):
        return self.SDR_BW

    def set_SDR_BW(self, SDR_BW):
        self.SDR_BW = SDR_BW

    def get_FFT_size(self):
        return self.FFT_size

    def set_FFT_size(self, FFT_size):
        self.FFT_size = FFT_size


def main(top_block_cls=spectrum, options=None):

    tb = top_block_cls()
    tb.start(1)
    tb.wait()


if __name__ == '__main__':
    main()
