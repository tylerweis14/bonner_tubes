Bonner Sphere Template
c
c Updated  7/12/17 by John Boyington 
c 
c ****************************************************************************** 
c                               CELL CARDS 
c ******************************************************************************
c
c                          -----Beam Port------
1 0         11 -15 -13      IMP:N=1  $ BP Inner Region
2 1 -2.699  11 -12  13 -14  IMP:N=1  $ BP Tube
3 0         (-11):(16):(31 11 -12):(13 12 -16)     IMP:N=0
4 1 -2.699  15 -16 18 -13       IMP:N=1 $ Al Tube
5 5 -7.310  25 -24 -26          IMP:N=1 $ Foil
6 4 -1.300  (15 -25 -18):(25 -24 26 -18) IMP:N=1 $ Filter

c ****************************************************************************** 
c                               SURFACE CARDS 
c ****************************************************************************** 
11 PX     0.0     $ BP Inner
12 PX    50.0     $ BP Outer
13 CX    0.9525   $ BP Inner Diameter
14 CX    1.27     $ BP Outer Diameter
15 PX    15.0     $ Tube Inner
16 PX    55.0     $ Tube Outer
18 CX    0.79375       $ Tube Diameter
19 PX    49.0     $ Disk Outer
24 PX    17.54    $ First filter
25 PX    17.44    $ Cavity
26 CX    0.5      $ Foil Diameter
31 CX    10.16    $ Poly Outer Diameter   
32 PX    17.70

c ****************************************************************************** 
c                               DATA CARDS 
c ******************************************************************************
SDEF   POS=1 0 0 AXS=1 0 0 EXT=0 VEC=1 0 0 ERG=D1 RAD=D2 PAR=1 
si1 0.5 1
sp1 0 1
si2 0 0.9525
sp2 -21 1
c
NPS 1E6
c
c  -----------------------------------------------------------------------------
c                                                          MATERIAL CARDS
c  -----------------------------------------------------------------------------
c  -----------------------------------------------------------------------------
c  MATERIAL 1:      Al    
c  ---------------------------(density 2.699 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M1  13027.70c   -1
c
c  -----------------------------------------------------------------------------
c  MATERIAL 2:      HDPE    
c  ---------------------------(density 0.950 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M2     1001     -0.143
       6000     -0.857
MT2    poly.10t
c  -----------------------------------------------------------------------------
c  MATERIAL 3:      ABS    
c  ---------------------------(density 1.070 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M3     1001     -0.0811
       6000     -0.85260563
       7014     -0.0662911
c  -----------------------------------------------------------------------------
c  MATERIAL 4:      Poly    
c  ---------------------------(density 1.300 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M4     1001     -0.05595
       6000     -0.5035887
       8000     -0.4404612
c  -----------------------------------------------------------------------------
c  MATERIAL 5:      In  
c  ---------------------------(density 7.310 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M5    49000     -1
c
c  -----------------------------------------------------------------------------
c  MATERIAL 6:      Borated Poly  
c  ---------------------------(density 1.000 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M6    1001       -0.125355
      5010.70c   -.100000
      6000       -.774645  
c
c  MATERIAL 7:      Cadmium 
c  ---------------------------(density 8.65 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M7    48000     -1
c
c  MATERIAL 8:      Gad  
c  ---------------------------(density 7.90 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M8   64000      -1
c
c  MATERIAL 9:      Au  
c  ---------------------------(density 19.30 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M9   79000      -1
c
c  MATERIAL 10:      Moly  
c  ---------------------------(density 10.28 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M10   42000      -1
c
c  -----------------------------------------------------------------------------
c  -----------------------------------------------------------------------------
c                                                             TALLY CARDS       
c  -----------------------------------------------------------------------------
c
c  -----------------------------------------------------------------------------
c  TALLY 1:         That disk.
c  -----------------------------------------------------------------------------
F4:N 7
c
c ****************************************************************************** 
c                             END OF INPUT FILE
c ******************************************************************************

