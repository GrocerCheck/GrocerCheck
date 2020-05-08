import livepopulartimes as lpt
from multiprocessing.pool import Pool
import time



addr = "(Save-On-Foods) 5945 Berton Ave, Vancouver, BC V6S 0B3, Canada"

NUM_SCRAPE=40

def regtest(addr):
    st = time.time()
    regout = []
    for i in range(NUM_SCRAPE):
        res = lpt.get_populartimes_by_formatted_address(addr)
        regout.append(res)
        print(i)
    et = time.time()
    print('len: ', len(regout))
    print("time ", et-st)

def cube(x):
    return x**3


def ordertest():
    st = time.time()
    pool = Pool(8)
    out = {}
    for i in range(400):
        out[i]=pool.apply_async(cube, args=(i,))
    for i in range(400):
        out[i]=out[i].get()
    et = time.time()
    for i in range(400):
        print(i, "  ", out[i], "  ", i**3)
    print(et-st)

def mptest(addr):
    st = time.time()
    pool = Pool(8)
    mpout = []
    for i in range(NUM_SCRAPE):
        res = pool.apply_async(lpt.get_populartimes_by_formatted_address, args=(addr,))
        mpout.append(res)

    mpout =[p.get() for p in mpout]
    et = time.time()
    print("len", len(mpout))
    print("time", et-st)

ordertest()
