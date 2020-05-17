#!/usr/bin/python
import numpy as np
import sys
from math import radians, cos, sin, asin, sqrt




def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6372.8
    return c * r 

def gen_coords(border, spacing):
    """
    :param border: list of list of coordinates in tuples outlining a rectangular area for which coords are to be generated.
    :param spacing: normal distance, in kilometers, between generated coords
    
    note: each border rectange must be given in form [(bottom,left), (top, right)]
    
    output: list of tuples, as per example border input
    """
    
    out_coords = []
    for bound in border:
        bottomleft = bound[0]
        topright = bound[1]
        bottomright = (bound[1][0], bound[0][1])
        topleft = (bound[0][0], bound[1][1])
                
        
        cx=bottomleft[0]
        cy=bottomleft[1]
        
        diffx = haversine(bottomright[0], bottomright[1], bottomleft[0], bottomleft[1])
        diffy = haversine(topleft[0], topleft[1], bottomleft[0], bottomleft[1])

        numx = int(diffx//spacing)
        numy = int(diffy//spacing)
        
        deltax = abs((bottomright[0]-bottomleft[0]))/numx
        deltay = abs((topleft[1]-bottomleft[1]))/numy
        #~ deltax = 1
        #~ deltay = 1

        for x in range(numx):
            for y in range(numy):
                out_coords.append((cx, cy))
                cy = cy + deltay
            cy = bottomleft[1]
            cx = cx + deltax
            
        #~ print(" numx ", numx, " numy ", numy, "deltax", deltax, "deltay", deltay, "diffx", diffx, "diffy", diffy)
    return out_coords





