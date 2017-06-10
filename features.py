# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 15:56:46 2017

@author: idear
"""

import numpy as np
from MRCG import MRCG
#import util
import soundfile
import essentia.standard as ess
import time
def features(filename):
    
    wav,fs = soundfile.read(filename)
    audio  = ess.MonoLoader(downmix = 'left',filename = filename,sampleRate =fs)()
    features,d_MRCG,dd_MRCG = MRCG(audio,fs=fs)
    
    print(features)
    return

if __name__ == '__main__':
    begin = time.time()
    features('1.wav')
    end = time.time()
    time = end - begin
    print('TIME is',time)

   
