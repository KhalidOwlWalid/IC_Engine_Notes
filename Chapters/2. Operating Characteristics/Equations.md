
## Engine Operating Characteristics
### A. Engine Parameters
<img src="Pasted image 20260701001408.png" style="display: block; margin: 0 auto;" width="800">

#### Stroke Length,S
$$
S = 2a \tag{A1}
$$
where:
- a = crank offset

#### Average Piston Speed, $U_p$
$$
U_p = 2SN \tag{A2}
$$
^A2
where:
 - S = stroke length
 - N = engine speed

#### Distance, s between crank axis and wrist pin axis
$$
s = a \cdot cos (\theta) + \sqrt{r^2 - a^2 \cdot sin^2(\theta)} \tag{A3}
$$
^A3

where:
- a = crankshaft offset
- r = connecting rod length
- $\theta$ = crank angle, which is measured from the cylinder centerline and is zero when the piston is at TDC

#### Ratio of instantaneous piston speed
$$
\frac{U_p}{\bar{U_p}} = (\frac{\pi}{2}\sin{\theta}) \cdot [1 + (\frac{\cos(\theta)}{\sqrt(R^2 - \sin^2{\theta})})] \tag{A4}
$$
where:
- R = ratio of connecting rod length to crank offset, r/a
- $\theta$ = crank angle

#### Displacement volume
- Volume displaced by the piston as it travels from BDC to TDC
$$
V_d = V_{BDC} - V_{TDC} \tag{A5}
$$
where:
- $V_d$ = Displacement volume
- BDC = Bottom dead center
- TDC = Top dead center

$$
V_d = N_c (\frac{\pi}{4})B^2S \tag{A6}
$$
where:
- $N_c$ = Number of engine cylinders
- B = cylinder bore
- S = stroke

Notes:
$$
1 L  = 10^{-3} m^3 = 10^3cm^3
$$
#### Clearance Volume
Minimum cylinder volume when the piston is at TDC
$$
V_c = V_{TDC} \tag{A7}
$$
$$
V_{BDC} = V_c + V_d \tag{A8}
$$
where:
- $V_c$ = clearance volume
- $V_d$ = Volume displacement 

#### Compression ratio
$$
r_c = V_{BDC}/V_{TDC} = \frac{V_c + V_d}{V_c} \tag{A9}
$$
where:
- $r_c$ = compression ratio
- BDC = Bottom dead center
- TDC = Top dead center
- $V_c$ = Clearance Volume
- $V_d$ = Volume displacement

#### Cylinder volume at any crank angle
$$
V = V_c + \frac{\pi B^2}{4}(r+ a - s) \tag{A10}
$$
where:
- $V_c$ = clearance volume
- B = Cylinder bore
- r = connecting rod length
- a = crank offset, distance between the crank axis and the rod axis
- s = piston position

It's non-dimensional form is given by:
$$
\frac{V}{V_c} = 1 + \frac{1}{2}(r_c - 1) \cdot [\quad R + 1 \cos{\theta} - \sqrt{R^2 - \sin^2{\theta}} \quad ] \tag{A11}
$$
where:
- $r_c$ = compression ratio
- R = r/a
- $\theta$ = crank angle
- $V_c$ = Clearance volume

#### Surface Area
Surface area of a flat-topped piston:
$$
A_p = (\frac{\pi}{4})B^2 \tag{A12}
$$
where:
- $A_p$ = Surface area of flat-topped piston
- B = Cylinder bore

Combustion chamber surface area:
$$
A = A_{ch} + A_p + \pi B(r+a-s) \tag{A13}
$$
- $A_ch$ = Cylinder head surface area
- r = connecting rod length
- a = crank offset, distance between the crankshaft axis and connecting rod axis
- s = Distance between crank axis and the wrist pin axis on the piston head

### B. Work

#### Work
Work is the result of a force acting through a distance. In terms of pressure, this can be defined as a force due to gas pressure on the surface area of the piston:
$$
W = \int F dx = \int PA_p \quad dx
$$
where:
- W = work output of the engine
- P = Pressure in the combustion chamber
- $A_p$ = surface area of the piston
- x = distance the piston moves

We know that:
$$
A_p \cdot dx = dV
$$
Hence:
$$
W = \int P \quad dV
$$
where:
- V = volume

#### Specific work
Engines are often multicylinder, hence it is convenient to analyze engine cycles per unit mass of gas m within the cylinder:
$$
w = \frac{W}{m} = \int P \quad dv
$$where:
- w = work per unit mass
- v  = volume per unit mass

### Indicated Work
<img src="Pasted image 20260722084438.png" style="display: block; margin: 0 auto;" width="800">
This is the area under the P-v diagram.
$$
w_b = w_i - w_t \tag{B1}
$$
^B1

where:
- $w_i$ = indicated specific work generated inside combustion chamber
- $w_t$ = specific work lost due to friction and parasitic loads

#### Net indicated work
$$
w_{net} = w_{gross} + w_{pump}
$$
where:
- $w_{pump}$ = Pump work, absorbs work from the engine
$$
W_{net} = (Area \space A) + (Area \space B)
$$

It should be noted that there is a difference between gross work and net work:
- gross work = output of the engine with fan and exhaust system removed
- net work = output of an engine with all components

#### Mechanical efficiency
$$
\eta_m = \frac{w_b}{w_i} = \frac{W_b}{W_i}
$$
where:
- $w_b, \space W_b$ = is specific brake work, Brake work
- $w_i, \space W_i$ = specific indicated work, indicated work

#### Mean effective Pressure
This is the average mean effective pressure where the pressure in the cylinder of an engine is continuously changing during the cycle
$$
w = (mep)\Delta v
$$
$$
mep = \frac{w}{\Delta v} = \frac{W}{V_d}
$$
$$
\Delta v = v_{BDC} - v_{TDC}
$$
where:
- W = work of one cycle
- w = specific work of one cycle
- $V_d$ = displacement volume

### All definitions of mean effective pressure (mep)
$$
bmep = \frac{w_b}{\Delta v}
$$
$$
imep = \frac{w_i}{\Delta v}
$$
$$
(imep)_{gross} = (w_i)_{gross} / \Delta v
$$
$$
(imep)_{net} = (w_i)_{net} / \Delta v
$$
$$
pmep = w_{pump}/\Delta v
$$
$$
fmep = w_f/\Delta v
$$
$$
nmep = gmep + pmep
$$
$$
bmep = nmep - fmep
$$
$$
bmep = \eta_{m} \cdot imep
$$
$$
bmep = imep - fmep
$$

where:
- bmep = brake mean effective pressure
- imep = indicated mean effective pressure where it can be divided into gross and net
- pmep = pump mean effective pressure (can have negative values)
- fmep = friction mean effective pressure
- $\eta_{m}$ = mechanical efficiency of the engine

### Torque
$$
2 \pi \tau = W_b = \frac{(bmep)\cdot V_d}{n}
$$
where:
- $W_b$ = brake work of one revolution
- $V_d$ = displacement volume
- n = number of revolutions per cycle (e.g. n = 4, four-stroke cycle)
- $\tau$ = torque measured off the output of the crankshaft

### Power
$$
\dot{W} = \frac{WN}{n}
$$
$$
\dot{W} = 2 \pi N \tau
$$
$$
\dot{W} = (1/2\pi)(mep)A_p \bar{U_p}
$$
$$
\dot{W} = \frac{(mep)A_p \bar{U_p}}{n}
$$
where:
- $\dot{W}$ = power
- W = work per cycle
- n = number of revolutions per cycle (e.g. n = 2, two-stroke cycle)
- N = engine speed
- mep = mean effective pressure
- $A_p$ = piston face area of all pistons
- $\bar{U_p}$ = piston average speed
- $\tau$ = torque

Depending upon which definition of work or mep is used as defined above, power can be defined as brake power, net indicated power etc.

$$
\dot{W_b} = \eta_{m} \dot{W_i}
$$
$$
(\dot{W_i})_{net}= (\dot{W_i})_{gross} - (\dot{W_i})_{pump}
$$
$$
\dot{W_b} = \dot{W_i} - \dot{W_f}
$$
where:
- $\eta_m$ = mechanical efficiency of the engine
- For each prefix:
	- b = brake
	- i = indicated
	- f = friction

$$
1 \space hp = 0.7457 \space kW
$$
$$
1 \space kW = 1.341 \space hp
$$
where:
- hp = horsepower

$$
SP = \frac{W_b}{A_p}
$$
$$
OPD = \frac{W_b}{V_d}
$$
$$
SV = \frac{V_d}{W_b}
$$
$$
SW = \frac{m_{engine}}{W_b}
$$
where:
- $W_b$ = brake power
- $A_p$ = piston face area of all pistons
- $V_d$ = displacement volume
- $m_{engine}$ = mass of the engine
- SP = specific power
- OPD = output per displacement
- SV = specific volume
- SW = specific weight