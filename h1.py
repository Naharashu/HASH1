import string
import secrets
import math
import itertools

def imul(a, b):
    return (a * b) & 0xFFFFFFFFFFFFFFFF




def hash320(src):
    if isinstance(src, bytes):
        src = src.decode('utf-8')
    
    hi = 0xABCDEF0123456789 ^ (len(src) * 2)
    lo = 0x123456789ABCDEF0 ^ (len(src) * 4)
    mo = 0xABCDEF0123456789 ^ (len(src) * 8)
    va = 0xDEADBEEFCAFEBABE ^ (len(src) * 16)
    la = 0x9876543210FEDCBA ^ (len(src) * 32)
    
    if len(src) % 2 == 0:
        src = src[::-1]

    for t in range(2):
        i = 0
        while i < len(src):
            nextChar = ord(src[i + 1]) if (i + 1 < len(src)) else 0
            code = ((ord(src[i]) << 16) | nextChar) & 0xFFFFFFFFFFFFFFFF

            hi ^= code
            lo ^= (code + 3) & 0xFFFFFFFFFFFFFFFF
            mo ^= (code + 5) & 0xFFFFFFFFFFFFFFFF
            va ^= (code + 7) & 0xFFFFFFFFFFFFFFFF
            la ^= (code + 11) & 0xFFFFFFFFFFFFFFFF
            
            j = 4
            while j >= 0:
                block = (code >> (j * 8)) & 0xFF
                hi ^= block
                lo ^= (block + 2)
                mo ^= (block + 4)
                va ^= (block + 6)
                la ^= (block + 8)
                
                j-=1
            hi = (hi + code) & 0xFFFFFFFFFFFFFFFF
            lo = (lo + code) & 0xFFFFFFFFFFFFFFFF
            mo = (mo + code) & 0xFFFFFFFFFFFFFFFF
            va = (va + code) & 0xFFFFFFFFFFFFFFFF
            la = (la + code) & 0xFFFFFFFFFFFFFFFF

            bitPos = (i * code + len(src)) % 64

            if (hi & (1 << bitPos)):
                hi = ((hi << 5) | (hi >> 59)) & 0xFFFFFFFFFFFFFFFF
            else:
                hi = ((lo >> 5) | (lo << 59)) & 0xFFFFFFFFFFFFFFFF

            if (lo & (1 << bitPos)):
                lo = ((lo << 5) | (lo >> 59)) & 0xFFFFFFFFFFFFFFFF
            else:
                lo = ((hi << 59) | (lo >> 5)) & 0xFFFFFFFFFFFFFFFF

            if (mo & (1 << bitPos)):
                mo = ((mo << 5) | (mo >> 59)) & 0xFFFFFFFFFFFFFFFF
            else:
                mo = ((hi << 59) | (mo >> 5)) & 0xFFFFFFFFFFFFFFFF

            if (va & (1 << bitPos)):
                va = ((va << 5) | (va >> 59)) & 0xFFFFFFFFFFFFFFFF
            else:
                va = ((mo << 59) | (va >> 5)) & 0xFFFFFFFFFFFFFFFF
                
            if (la & (1 << bitPos)):
                la = ((la << 5) | (la >> 49)) & 0xFFFFFFFFFFFFFFFF
            else:
                la = ((hi << 49) | (va >> 5)) & 0xFFFFFFFFFFFFFFFF   

            mo ^= imul(hi, lo)
            lo ^= imul(va, mo)
            hi ^= imul(va, lo)
            va ^= imul(mo, va)
            la ^= imul(hi, va)

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
            
            la ^= la >> 16
            la = imul(la, 0x85ebca6b)
            la ^= la >> 13
            la = imul(la, 0xc2b2ae35)
            la ^= la >> 16

            hi = (~hi) & 0xFFFFFFFFFFFFFFFF
            lo = (~lo) & 0xFFFFFFFFFFFFFFFF
            mo = (~mo) & 0xFFFFFFFFFFFFFFFF
            va = (~va) & 0xFFFFFFFFFFFFFFFF
            la = (~la) & 0xFFFFFFFFFFFFFFFF

            i += 1

    return f"{hi:016x}{lo:016x}{mo:016x}{va:016x}{la:016x}"