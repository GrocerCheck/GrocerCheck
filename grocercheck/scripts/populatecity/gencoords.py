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
    return c * r * 1000


def gen_coords(border, spacing):
    """
    :param border: list of list of coordinates in tuples outlining a rectangular area for which coords are to be generated.
    :param hotspots: list of tuples for areas in which more coordinates are to be generated
    :param spacing: normal distance, in meters, between generated coords
    :param hotspot_spacing: distance, in meters, for coord spacing between hotspots

    note: each border rectange must be given in form [(top,left), (top,right), (bottom, right), (bottom,left)]
    Order matters -- try to only go clockwise or only counterclockwise! Refer to matplotlib path.
    output: list of tuples, as per example border input

    coords within 2*np.ln(spacing)*np.sqrt(spacing) of each hotspot will be clustered closer together as per hotspot_spacing
    """
    out_coords = []
    for bound in border:
        cx=bound[3][0]
        cy=bound[3][1]
        diffx = haversine(bound[0][0], bound[0][1], bound[1][0], bound[1][1])
        diffy = haversine(bound[0][0], bound[0][1], bound[3][0], bound[3][1])

        numx = int(diffx//spacing)
        numy = int(diffy//spacing)
        deltax = abs(bound[1][0] - bound[0][0])/numx
        deltay = abs(bound[0][1] - bound[3][1])/numy

        out_coords.append((cx, cy))
        for x in range(numx):
            cx = cx + deltax
            for y in range(numy):
                cy = cy + deltay
                out_coords.append((cx, cy))
    return out_coords






