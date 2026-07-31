## Wide-Open Throttle
![[Pasted image 20260730003017.png | center |617]]
![[Pasted image 20260731120656.png|550]]
The above shows the P-v diagram of the Otto-cycle which is using an air-standard analysis. In this diagram, it basically shows you the P-v cycles that the cylinder goes through every 2 revolutions of the crankshaft.

- 6->1 (Air intake): Exhaust valve closes, Intake valve opens. As the piston moves towards BDC, the cylinder volume increases, creating a pressure differential between the intake manifold and the cylinder. Air is then pushed into the cylinder.
- 1->2 (Compression): Intake valve closed. Piston head moves from BDC to TDC, compressing the air inside the cylinder.
- 2->3 (Combustion): The fuel injector fires up a spark, to burn the fuel + air mixture inside the cylinder, causing a huge pressure spike and temperature spike.
- 3->4 (Power stroke): The combustion has caused the cylinder to move towards BDC. The air in the cylinder now experiences expansion cooling as the piston moves towards BDC, pressure decreases, causing the air particles to lose kinetic energy, hence reduction in temperature.
- 4->5 (Exhaust blowdown): Once the piston almost arrive at the bottom dead center, the exhaust valve slowly opened. Due to the high pressure differential between the air inside the combustion chamber against the exhaust valve, naturally, the air inside the cylinder escapes through the exhaust valve, this is a process called exhaust blowdown.
- 5->6: Piston moves to TDC to repeat the cycle to push all of the air out of the cylinder chamber into the exhaust manifold. Afterwards, the cycle repeats itself.

## Real-air fuel engine cycles

Major differences between the air-standard Otto cycle analysis against the actual cycle of a real internal combustion engine includes:
1. Real engines operate on an open cycle with changing composition.
	- Original assumption: Engine operates in closed cycle, air does not escape through crevices etc.
	- Consequences: Changed the amount of gas composition during the cycle
	- Physical evidence: 
2. Inlet flow may be all air or it can be mixed with fuel
	- Original assumptions: Inlet flow is all air and air is assumed to be ideal gas
	- Consequences: Introduces some errors in the modeling process. Specific heats of a gas have strong dependency on temperature. For standard-air cycles, we assumed the specific heat is constant throughout.
3. There are heat losses in a real engine cycle
	- Original assumptions: We have assumed isentropic process during the cycle (adiabatic and reversible)
	- Consequences: Heat loss during combustion lowers peak temperature and pressure. This leads to decreased work output by the engine.
4. Heat addition is not instantaneous
	- Original assumption: Heat addition is instantaneous as shown in the T-s diagram
	- Consequences: Unlike the heat addition happening when the piston is at TDC, it happened before TDC instead, not at constant volume when the piston is at TDC. This will produce less work output as the piston will have to force through the combustion while still heading to TDC. This creates negative work in that stroke.
5. Blowdown process requires a finite real time and a finite cycle time
	- Original assumptions: Blowdown (exhaust) happens at constant volume in air-standard analysis.
	- Consequences: Exhaust valve is opened $40^{\circ}$ to $60^\circ$ before BDC. Output work during when the exhaust valve is opened is lost.
6. Intake valve is not closed until after BDC at the end of the intake stroke.
	- Original assumptions: Intake valve closes at BDC during intake stroke
	- Reason: Volumetric efficiency would be lower if the intake valve closes at BDC as air would still be entering the cylinder at BDC.
	- Conseqeunces: Compression will only happen once the intake valve is closed
7. Engine valve requires finite time to actuate
	- Original assumptions: Engine valve would immediately opened during its stroke
	- Reason: The cam profiles must allow for smooth interaction with the cam follower.
	- Consequences: Because of this, there will be some overlapping period where both the intake stroke and the exhaust stroke opening at the same time causing a deviation from the ideal cycle
	![[Pasted image 20260731115245.png|379]]
Due to this, the real air-fuel engine cycle will deviate from the Otto cycle. However, the indicated thermal efficiency of an actual SI four-stroke cycle engine can be approximated by:
$$
(\eta_t)_{actual} = 0.85 \cdot \eta_{otto}
$$
where:

## Part throttle
![[Pasted image 20260731120803.png|743]]

Some distinction you would see from the part throttle P-v diagram:
- 6 - 6a - 1 (Intake stroke): During the intake stroke, since this is part throttle, there is some flow restrictions due to the throttle plate, which causes the pressure to be less than $P_o$ (atmospheric pressure). This produces negative pump work.
	- The more closed the throttle position, the lower will be the pressure during the intake stroke and the greater the negative pump work.

Factors contributing to the reduced net work at part throttle:
1. Lower pressure at the start of compression, results in lower pressure throughout the rest of the cycle which lowers the mep and net work.
2. Less thermal energy from the combustion in the cylinders and less resulting workout.
	- This is due to the fact that when less air is ingested, the duel input by the injectors or carburators is proportionally reduced.
	- This allows the temperature between 2-3 to remain the same for part throttle and wide open throttle.

## Turbocharged P-v diagram
![[Pasted image 20260731122108.png | 685]]
- For an engine equipped with turbocharger/supercharger:
	- Intake pressure will be higher than standard atmospheric pressure due to the charged pressure coming from the turbo
	- This results in more air and fuel in the combustion chamber during the cycle, and producing higher net indicated work.
	- Higher intake pressure increases all pressures throughout the cycle, and increased air and fuel gives greater $Q_{in}$ in process 2-3



> [!Warning] 
> Due to the higher manifold pressure thanks to the charge pressure. When air is compressed during the compression stroke, the temperature is also increased due to compressive heating. This can cause self ignition and knocking problems in the latter part of the combustion or during combustion, potentially harming the engine.
> This is why a lot of turbocharged system comes equipped with an aftercooler to lower the compressed incoming air temperature.
