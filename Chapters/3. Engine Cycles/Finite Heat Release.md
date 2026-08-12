The finite heat release allows us to predict the indicated mean effective pressure (imep) of our engine. There are also a few states that are obtained with the finite heat release which allows us to better understand the behaviour of a given engine.

The Pressure, P is given by the equation:
$$
\frac{d\tilde{P}}{d\theta} = -\gamma\frac{\tilde{P}}{\tilde{V}}\frac{d\tilde{V}}{d\theta} + (\gamma  - 1) \frac{\tilde{Q}}{\tilde{V}} \frac{dx}{d\theta}
$$
Note that:
$$
\tilde{P} = \frac{P}{P_1} \qquad \tilde{V} = \frac{V}{V_1} \qquad \tilde{Q} = \frac{Q_{in}}{P_1V_1}
$$
where:
- P = instantaneous pressure in the combustion chamber
- V = instantaneous volume in the combustion chamber
- $Q_{in}$ = Heat added into the system
- $\theta$ = current crank angle
- $\gamma$ = specific heat capacity
- x = fraction of energy release from the combustion process

In order to solve for pressure and temperature profiles given an engine, you would need to follow the given steps:

### Parameters required
- $P_1$ = pressure at bottom dead center (BDC)
- $V_1$ = volume at BDC
- r = compression ratio
- $Q_{in}$ = total heat added through the combustion process

Please note that these steps are done iteratively with increasing $\theta$ 
1. Solve for the combustion's burn rate, $dx/d\theta$ 
2. Solve for $d\tilde{V}/d\theta$ 
3. Solve for $\tilde{V_n}$ by multiplying $d\theta$ to $d\tilde{V}/d\theta$
4. Solve for $V_n$ by multiplying $\tilde{V}$ with $V_1$ (volume at BDC)
5. Similar to step 2, now solve for $d\tilde{P}/d\theta$
	- Notice that in order to solve for this, for the first iteration, you'd be required to plug in the initial pressure, $P_o$
6. Solve for $P_{n+1}$
$$
P_{n+1} = P_n + \frac{d\tilde{P}}{d\theta} P_1 \cdot d\theta
$$
	- The above formula is basically performing a forward euler. We are essentially dealing with numerical integration. In this case, you could also use Runge Kutta method, to gain better accuracy, if real-time is not the concern. For the purpose of this note, I will not be discussing in depth regarding choosing numerical solver.
7. Compute useful work, $\tilde{W}$ (work done by the engine)
8. Compute imep (indicative mean effective pressure)

#### Things to note
Please note that from Wiebe function, the start of the energy release determined when the combustion will happen and the duration will entail for how long the combustion is going to occur.

For example:
- $\theta_s$ = $-20^{\circ}$, $\theta_{d}$ = $60^{\circ}$ 
The combustion will occur when the crank angle is at $-20^{\circ}$ until $40^{\circ}$ . Throughout this duration, the cumulative energy release will gradually increase given by the Wiebe function