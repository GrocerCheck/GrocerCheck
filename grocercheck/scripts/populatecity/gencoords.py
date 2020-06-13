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

    if len(border[0]) == 2:
        print("gen with 2")
        cl = gen_coords_with_two_points(border, spacing)
        return cl
    elif len(border[0]) == 4:
        print("gen with quad")
        cl = gen_coords_with_quadrilateral(border, spacing)
        return cl
    else:
        print("Border error")


#[
#[(bottom, left), (bottom, right), (top, left), (top, right)],
#]
def gen_coords_with_quadrilateral(border, spacing):
    out_coords = []

    for bound in border:
        maxy = max(bound[0][1], bound[1][1], bound[2][1], bound[3][1])
        miny = min(bound[0][1], bound[1][1], bound[2][1], bound[3][1])
        maxx = max(bound[0][0], bound[1][0], bound[2][0], bound[3][0])
        minx = min(bound[0][0], bound[1][0], bound[2][0], bound[3][0])

        chunk_coords = gen_coords_with_two_points([[(minx, miny), (maxx, maxy)]]  , spacing)

        #slopetop (slt), slopeleft, right, bottom..

        print("Num In Chunk: ", len(chunk_coords))

        slt = (bound[3][1] - bound[2][1])/(bound[3][0]-bound[2][0]) #done

        if (bound[2][0] >= bound[0][0]):
            sll = (bound[2][1] - bound[0][1])/(bound[2][0]-bound[0][0])
        else:
            sll = (bound[0][1] - bound[2][1])/(bound[0][0]-bound[2][0])
        if (bound[3][0] >= bound[1][0]):
            slr = (bound[3][1] - bound[1][1])/(bound[3][0]-bound[1][0])
        else:
            slr = (bound[1][1] - bound[3][1])/(bound[1][0]-bound[3][0])

        slb = (bound[1][1] - bound[0][1])/(bound[1][0]-bound[0][0])
        print(bound)
        print("slt, slb, sll ,slr", slt, slb, sll, slr)


        for coord in chunk_coords:
#filter coords from top left top top right, moving downwards

#initial y + slope * deltax
            bt = bound[2][1] + slt*(coord[0]-bound[2][0])#bound top
            bb = bound[0][1] + slb*(coord[0]-bound[0][0])#bound bottom..
            if (bound[0][0] >= bound[2][0]):
                bl = (coord[1]-bound[2][1])/sll
            else:
                bl = (coord[1]-bound[0][1])/sll

            if (bound[3][0] >= bound[1][0]):
                br = (coord[1]-bound[1][1])/slr
            else:
                br = (coord[1]-bound[3][1])/slr

#             print('-------------------------')
#             print("  ", bt, "  ")
#             print(bl, "    ", br)
#             print("  ", bb, "  ")
#             print("coord", coord)
#             print("-------------------------")
            if (((coord[0] <= br) and (coord[0] >= bl)) and ((coord[1] <= bt) and (coord[1] >= bb))):
                print("asdf")
                out_coords.append(coord)

    return out_coords



def gen_coords_with_two_points(border, spacing):
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

        if (diffx < spacing) or (diffy < spacing):
            spacing = min(diffx, diffy)

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

        print(" numx ", numx, " numy ", numy, "deltax", deltax, "deltay", deltay, "diffx", diffx, "diffy", diffy)
    return out_coords





