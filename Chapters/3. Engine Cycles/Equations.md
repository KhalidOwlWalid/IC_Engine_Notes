## Ideal gas relationships

$$
Pv = RT \tag{3A.1}
$$
$$
PV = mRT \tag{3A.2}
$$
$$
P = \rho R T \tag{3A.3}
$$
$$
dh = c_p \space dT \tag{3A.4}
$$
$$
du = c_v \space dT
$$
$$
Pv^k = constant \tag{3A.5} \qquad isentropic \space process
$$
$$
Tv^{k-1} = constant \tag{3A.6} \qquad isentropic \space process
$$
$$
TP^{(1-k)/k} = constant \tag{3A.7} \qquad isentropic \space process
$$
$$
w_{1-2} = \frac{P_2v_2 - P_1v_1}{1-k} \tag{3A.8} \qquad isentropic \space work \space in \space closed \space system
$$
$$
w_{1-2} = \frac{R(T_2 - T_1)}{1 - k} \tag{3A.9}
$$
$$
c = \sqrt{kRT} \tag{3A.10} \qquad speed \space of \space sound
$$
where:
- P = gas pressure in cylinder
- V = volume in cylinder
- v = specific volume of gas
- R = gas constant of air
- T = temperature
- m = mass of gas in cylinder
- $\rho$ = density
- h = specific enthalpy
- u = specific internal energy
- $c_p$  = specific heat of pressure
- $c_v$ = specific heat of volume
- k = $c_p/c_v$
- w = specific work
- c = speed of sound

## Gas cycle computation
$$
Q_{in} = m_f \cdot q_{c} = m\cdot q_{in}
$$
where:
- $Q_{in}$ =  head addition (kJ)
- $m_f$ = mass of fuel injected into the cylinder (kg)
- m = mass of the fuel-air gas mixture (kJ/ $kg_{fuel}$ )
- $q_c$ = heat of combustion (kJ/ $kg_{fuel}$ )
- $q_{in}$ = heat addition per unit mass of fuel air mixutre ( $kJ/kg_{mix}$)

## Otto Cycles
#### Compression Stroke
$$
\frac{P_2}{P_1} = r^{\gamma} \qquad \frac{T_2}{T_1} = r^{\gamma - 1}
$$
#### Constant Volume Heat Addition
$$
Q_{in} = mc_v(T_3 - T_2)
$$
$$
\frac{T_3}{T_2} = (\gamma - 1) \frac{Q_{in}}{P_1 V_1} r^{\gamma - 1} + 1
$$
$$
\frac{P_3}{P_2} = \frac{T_3}{T_2}
$$
#### Expansion Stroke
