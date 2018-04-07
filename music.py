#pip install cffi
#pip install sounddevice

import sounddevice as sd
import numpy as np 


def play(func, duration=10, fs=8000, type_=np.uint8):
    arr = []
    for t in range(0, fs * duration):
        arr.append(func(t)[0])

    buf = np.array(arr, dtype=type_)
    sd.play(buf, fs)
    sd.wait()

# musics
def music1(t):
    return (t>>6^t>>8|t>>11|t&63) , 8000

music_kox_x = 1
music_kox_y = 1
def music_kox(t):  #32kHz
    global music_kox_x
    global music_kox_y

    music_kox_y = int(t&16383 if t&16383 != 0 else 1)
    music_kox_x = int(t * (ord("6689"[t>>16&3])&15) / (24&127)  * music_kox_y / 4e4)
    return (((int)(3e3/(music_kox_y))&1)*35) + music_kox_x +((t>>8^t>>10|t>>14|music_kox_x)&63), 32000


def chaos(t):
    w=t>>9
    k=32
    m=2048
    a=int(1-t/m%1 )
    d=int((14*t*t^t)%m*a)
    p=int(int(w/k)&3)
    y=[3,3,4.7,2][p]*t/4 
    h=ord("IQNNNN!!]]!Q!IW]WQNN??!!W]WQNNN?"[int(w/2)&15|int(p/3)<<4])/33*t-t
    s=int(y*.98%80+y%80+(w>>7 and a*((5*t%m*a&128)*(0x53232323>>int(w/4)&1)+ 
        (d&127)*(0xa444c444>>int(w/4)&1)*1.5+(d*w&1) + 
        (h%k+h*1.99%k+h*.49%k+h*.97%k-64)*(4-a-a))))
    s= s* 127 if s>>14 else s
    return s, 8000

def jumpy(t):  ## 41khz
    return (int((t*(ord("36364689"[t>>13&7])&15))/12)&128)+((int((((t>>12)^(t>>12)-2)%11*t)/4)|t>>13)&127), 41000

def bad_beats(t):
    return t*((0xbadbea75>>((t>>12)&30)&3)*0.25*(0x5afe5>>((t>>16)&28)&3)), 8000

def music2(t):
    return ((t&((t>>5)))+(t|((t>>7))))&(t>>6)|(t>>5)&(t*(t>>7)), 8000



foo = music2

play(
    foo
    , fs=foo(1)[1]
    , duration=20
)
