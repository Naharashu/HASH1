import string
import secrets
import math
import itertools

def imul(a, b):
    return ((a & 0xFFFFFFFF) * (b & 0xFFFFFFFF)) & 0xFFFFFFFF

def h1(src):
    hi = 0xABCDEF01 ^ (len(src) * 2)
    lo = 0x12345678 ^ (len(src) * 4)
    mo = 0xABCDEF0123456789 ^ (len(src) * 8)
    va = 0xDEADBEEF ^ (len(src) * 16)

    if len(src) % 2 == 0:
        src = "".join(reversed(list(src)))
    
    t = 0

    while t < 5:
        i = 0
        while i < len(src):
            nextChar = ord(src[i + 1]) if (i + 1 < len(src)) else 0
            code = ((ord(src[i]) << 32) | nextChar) & 0xFFFFFFFFFFFFFFFF  

            hi ^= code & 0xFFFFFFFF
            lo ^= (code + 3) & 0xFFFFFFFF
            mo ^= (code + 5) & 0xFFFFFFFF
            va ^= (code + 7) & 0xFFFFFFFF

            j = 4  
            while j >= 0:
                block = (code >> (j * 8)) & 0xFF
                hi ^= block & 0xFFFFFFFF
                lo ^= (block + 2) & 0xFFFFFFFF
                mo ^= (block + 4) & 0xFFFFFFFF
                va ^= (block + 6) & 0xFFFFFFFF
                j -= 1

            hi = (hi + (code & 0xFFFFFFFF)) & 0xFFFFFFFF
            lo = (lo + (code & 0xFFFFFFFF)) & 0xFFFFFFFF
            mo = (mo + (code & 0xFFFFFFFF)) & 0xFFFFFFFF
            va = (va + (code & 0xFFFFFFFF)) & 0xFFFFFFFF

            bitPos = (i * code + len(src)) % 32 

            if (hi & (1 << bitPos)):
                hi = ((hi << 5) | (hi >> 27)) & 0xFFFFFFFF
            else:
                hi = ((lo >> 5) | (lo << 27)) & 0xFFFFFFFF
                
            if (lo & (1 << bitPos)):
                lo = ((lo << 5) | (lo >> 27)) & 0xFFFFFFFF
            else:
                lo = ((hi << 27) | (lo >> 5)) & 0xFFFFFFFF
                
            if (mo & (1 << bitPos)):
                mo = ((mo << 5) | (mo >> 27)) & 0xFFFFFFFF
            else:
                mo = ((hi << 27) | (mo >> 5)) & 0xFFFFFFFF
            
            if (va & (1 << bitPos)):
                va = ((va << 5) | (va >> 27)) & 0xFFFFFFFF
            else:
                va = ((mo << 27) | (va >> 5)) & 0xFFFFFFFF

            hi ^= hi >> 16
            hi = imul(hi, 0x85ebca6b)
            hi ^= hi >> 13
            hi = imul(hi, 0xc2b2ae35)
            hi ^= hi >> 16

            lo ^= lo >> 16
            lo = imul(lo, 0x85ebca6b)
            lo ^= lo >> 13
            lo = imul(lo, 0xc2b2ae35)
            lo ^= lo >> 16
            
            mo ^= mo >> 17
            mo = imul(mo, 0x85ebca6b)
            mo ^= mo >> 12
            mo = imul(mo, 0xc2b2ae35)
            mo ^= mo >> 17
            
            va ^= va >> 18
            va = imul(va, 0x85ebca6b)
            va ^= va >> 13
            va = imul(va, 0xc2b2ae35)
            va ^= va >> 18
            

            hi = (~hi) & 0xFFFFFFFF
            lo = (~lo) & 0xFFFFFFFF
            mo = (~mo) & 0xFFFFFFFF
            va = (~va) & 0xFFFFFFFF

            i += 1
        t += 1

    return hex(hi)[2:].zfill(8) + hex(lo)[2:].zfill(8) + hex(mo)[2:].zfill(8) + hex(va)[2:].zfill(8)

