'''
 * Copyright (C) 2016  Music Technology Group - Universitat Pompeu Fabra
 *
 * This file is part of jingjuPhoneticSegmentation
 *
 * pypYIN is free software: you can redistribute it and/or modify it under
 * the terms of the GNU Affero General Public License as published by the Free
 * Software Foundation (FSF), either version 3 of the License, or (at your
 * option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the Affero GNU General Public License
 * version 3 along with this program.  If not, see http://www.gnu.org/licenses/
 *
 * If you have any problem about this python version code, please contact: Rong Gong
 * rong.gong@upf.edu
 *
 *
 * If you want to refer this code, please use this article:
 *
'''

import numpy as np

def get_avg( m , v_span, h_span):
    # This function produces a smoothed version of cochleagram
    [nr,nc] = m.shape
    out = np.zeros((nr,nc))
    fil_size = (2*v_span+1)*(2*h_span+1)

    for i in range(nr):
        row_begin = 0
        row_end = nr-1
        col_begin =0
        col_end = nc-1
        if (i - v_span)>=0:
            row_begin = i - v_span
        if (i + v_span)<=nr-1:
            row_end = i + v_span

        for j in range(nc):
            if (j - h_span)>=0:
                col_begin = j - h_span

            if (j + h_span)<=nc-1:
                col_end = j + h_span

            tmp = m[row_begin:row_end,col_begin:col_end]
            out[i,j] = np.sum(np.sum(tmp))/fil_size

    return out
