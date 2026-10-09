# Research

## Overview
This document outlines the research needed to develop and validate Gradient Relativity, including theoretical foundations, required citations, key quantum physics topics to study, and practical formulas for calculating electromagnetic fields at gravitational equilibria in rotating galactic systems.

The [current manuscript](RoughDraftImproved.md) records the clarified spatial pressure,
contraction, transport, and center-restart account. The calculations below are provisional
research templates, not a derived conserved field theory or validated electron model.

### Clarified mechanism and additional derivation targets

- The highest proposed space/EM state is between masses: 100% oscillation/expansion,
  normalized to 1. Positive pressure drives space into both masses; condensation is
  proposed to contract their intervening space rather than repel them.
- Define pressure, conversion rate, matter response, and an operational distance prediction.
  Distinguish the spatial label from the internal cycle fraction and measured speed.
- Specify the incoming-photon energy budget and source/receiver coupling. The recorded
  galactic Larmor estimate does not validate that separate driver.
- Derive the infinite-path transport interpretation, interference and causal response.
  The proposed central majority-electron population is an assumption requiring constraints.
- At the proposed center, 0% applies to space/EM activity, not total energy. Define the
  slow/stopped variable, stored mass state, hit/no-hit response and conserved restart.
  This is not an observed atomic level or an outgoing escape path through a GR horizon.

See [the falsification roadmap](Todo/electron_cycle_falsification.md), especially R13,
and [retrieved Markdown context](../Reseach/README.md).

## 1. Research Still Needed

### Theoretical Development
- Derive the full Lagrangian for the Planck field interacting with fermions under Gradient Relativity.
- Compute the electron self‑energy from the whirlpool internal oscillation and compare to the measured electron mass.
- Extend the model to include nucleons (protons, neutrons) and verify mass ratios.
- Formulate a covariant version of Gradient Relativity that reduces to General Relativity in the low‑energy limit.
- Analyze the stress‑energy tensor of the Planck field and its conservation properties.
- Investigate the relationship between the space‑energy gradient and the cosmological constant (dark energy).

### Experimental Signatures
- Predict deviations in the electron anomalous magnetic moment (g‑2) due to internal whirlpool dynamics.
- Calculate expected shifts in atomic spectra (Lamb‑like) from a varying local speed of light.
- Determine gravitational wave emission spectra from binary systems where centripetal acceleration alters the equilibrium point.
- Study the behavior of electrons in Penning traps under strong magnetic fields; look for anomalies tied to the local space‑energy gradient.
- Examine cosmic microwave background (CMB) polarization for imprints of a primordial Planck‑field gradient.

### Computational Simulations
- Develop a numerical solver for the Planck field equations in 3+1 dimensions.
- Simulate the whirlpool motion of an electron in a rotating binary‑star gravitational equilibrium.
- Model galaxy‑scale space‑energy gradients and their effect on stellar orbital velocities (alternative to dark matter).
- Implement a Manim‑based visualizer for the electron whirlpool and photon emission/absorption.

## 2. Required Citations

### Foundational Papers
1. Albert Einstein, "Die Grundlage der allgemeinen Relativitätstheorie," Annalen der Physik, 1916. (General Relativity)
2. Max Planck, "Zur Theorie des Gesetzes der Energieverteilung im Normalspektrum," Annalen der Physik, 1901. (Quantum theory)
3. Hendrik Casimir, "On the Attraction Between Two Perfectly Conducting Plates," Proc. Kon. Ned. Acad. Wet., 1948. (Vacuum fluctuations)
4. Willis Lamb, "Fine Structure of the Hydrogen Atom," Phys. Rev., 1947. (Lamb shift)
5. Gerald Gabrielse et al., "New Determination of the Fine Structure Constant from the Electron g Value and QED," Phys. Rev. Lett., 2006. (Electron g‑2)
6. LIGO Scientific Collaboration and Virgo Collaboration, "Observation of Gravitational Waves from a Binary Black Hole Merger," Phys. Rev. Lett., 2016. (Gravitational waves)

### Gradient Relativity Specific
- Cale McCollough, private notes on Gradient Relativity, 2022‑2026. (Primary source)
- (To be filled) Papers on emergent gravity, entropic gravity, and analogue models (e.g., Verlinde, 2011; Barcelo et al., 2005).

### Quantum Field Theory & Condensed Matter
1. Franz Schwabl, *Advanced Quantum Mechanics*, Springer, 2008.
2. Michael Peskin & Daniel Schroeder, *An Introduction to Quantum Field Theory*, Addison‑Wesley, 1995.
3. John Cardy, *Scaling and Renormalization in Statistical Physics*, Cambridge University Press, 1996.
4. Subir Sachdev, *Quantum Phase Transitions*, Cambridge University Press, 2nd ed., 2011.
5. Xiao‑Gang Wen, *Quantum Field Theory of Many‑Body Systems*, Oxford University Press, 2004.

## 3. Quantum Physics Theories to Study
- **Quantum Electrodynamics (QED):** Renormalization, Lamb shift, electron g‑2, vacuum polarization.
- **Quantum Field Theory in Curved Spacetime:** Particle creation in expanding universes, Hawking radiation, Unruh effect.
- **Bose‑Einstein Condensates & Superfluidity:** Macroscopic wavefunctions, quantized vortices, phonon‑roton spectrum.
- **Fractional Quantum Hall Effect:** Anyonic statistics, Chern‑Simons theory, topological order.
- **AdS/CFT Correspondence:** Holographic duality, entanglement entropy, Ryu‑Takayanagi formula.
- **Quantum Information & Entanglement:** Bell inequalities, teleportation, quantum error correction.
- **Topological Insulators & Superconductors:** Bulk‑boundary correspondence, Majorana fermions, Z₂ invariants.
- **Many‑Body Localization:** Ergodicity breaking, local integrals of motion.
- **Quantum Gravity Approaches:** Loop quantum gravity, spin foams, causal sets, asymptotically safe gravity.

## 4. Formulas & Instructions: EM Field at Gravitational Equilibrium with Galactic Rotation

### 4.1 Gravitational Equilibrium Point
For two masses \(M_1\) and \(M_2\) separated by distance \(r\), the equilibrium distance from \(M_1\) is
\[
d_1 = \frac{r}{1 + \sqrt{M_2/M_1}}.
\]

### 4.2 Centripetal Acceleration due to Galactic Orbit
Let the galactic angular speed be \(\Omega_G\) (≈ \(2\pi / (200\,\text{Myr})\)). The equilibrium point at galactocentric radius \(R_G\) experiences
\[
\mathbf{a}_c = -\Omega_G^2 R_G \,\hat{\mathbf{R}}_G,
\]
directed toward the galactic center. In the local inertial frame of the equilibrium point, this appears as a time‑varying gravitational potential.

### 4.3 Electromagnetic Field from Accelerating Electron (Larmor Formula)
The power radiated by a non‑relativistic accelerating charge is
\[
P = \frac{q^2 a^2}{6\pi\epsilon_0 c^3},
\]
Here the older approximation substitutes \(a=|\mathbf{a}_c|\). Galactic coordinate
acceleration alone does not establish the force or proper acceleration of a radiating
charge; specify the frame and radiation boundary conditions. Keep the calculation in SI
with reference \(c_0\), or convert every quantity consistently to a declared unit system.
Substituting the literal number 1 for \(c\) while retaining SI inputs is not a unit conversion.

### 4.4 Space‑Energy Gradient & Local Speed of Light
Define the space‑energy fraction \(\sigma \in [0,1]\) such that
\[
E_{\text{space}} = \sigma E_0,
\quad
E_{\text{mass}} = (1-\sigma) E_0,
\]
with \(E_0\) the total energy density constant.

**Two distinct candidate laws (unresolved; current manuscript section 4):**

- **P1, dimensionless:** \(u^2=E_{\text{space}}/E_{\text{mass}}=\sigma/(1-\sigma)\).
- **Bounded prototype:** \(u(\sigma)=2\sqrt{\sigma(1-\sigma)}\).

Here \(u=c_{\mathrm{model}}/c_0\) is a declared speed ratio, not an SI speed. Both give
1 at \(\sigma=1/2\) and tend to 0 as \(\sigma\to0\). P1 diverges as \(\sigma\to1\),
while the bounded form tends to 0. They are not interchangeable parameterizations under
the same fraction definition. The spatial 100% endpoint is not silently the half-fraction
point of this internal bookkeeping. Their relationship remains to be derived.

The FDTD prototype uses the bounded form as a numerical choice. Label its results with
that choice rather than promoting them to consequences of P1 or the new spatial mechanism.

### 4.5 Planck Field Equation of Motion
The following sections preserve a provisional solver outline. A scalar template does not
by itself provide electromagnetic vector fields, a fermion, or the pressure/conversion law.
Source dimensions, tensor type, units and operators still need a consistent action before
these equations can be treated as physical model instructions.

The Planck field \(\phi(x,t)\) obeys a wave equation with a space‑dependent speed:
\[
\partial_t^2 \phi - C^2(\sigma) \nabla^2 \phi + m_\phi^2 \phi = 0,
\]
where \(m_\phi\) is the Planck mass (inverse Planck length). The source term from an accelerating electron is
\[
J(x,t) = q \int d\tau\, \dot{x}^\mu(\tau) \delta^{(4)}(x - x(\tau)),
\]
leading to an inhomogeneous equation:
\[
\partial_t^2 \phi - C^2 \nabla^2 \phi = -\frac{J}{\epsilon_0}.
\]

### 4.6 Numerical Procedure to Compute EM Field
1. **Set up grid:** Define a 3D Cartesian domain centered on the equilibrium point, with spacing \(\Delta x\) smaller than the Planck length.
2. **Initialize fields:** \(\phi = 0\), \(\partial_t \phi = 0\).
3. **Define trajectory:** \(x_e(t) = R_G [\cos(\Omega_G t), \sin(\Omega_G t), 0]\) (circular orbit) plus small oscillation due to internal whirlpool (to be solved self‑consistently).
4. **Compute acceleration:** \(a_e(t) = -\Omega_G^2 x_e(t)\).
5. **Update source:** At each time step, compute \(J\) from the electron’s velocity and position.
6. **Evolve field:** Use a finite‑difference time‑domain (FDTD) scheme:
   \[
   \phi^{n+1}_{i,j,k} = 2\phi^{n}_{i,j,k} - \phi^{n-1}_{i,j,k}
   + (C\Delta t)^2 \left[
   \frac{\phi^{n}_{i+1,j,k} - 2\phi^{n}_{i,j,k} + \phi^{n}_{i-1,j,k}}{\Delta x^2}
   + \text{(y,z terms)}
   \right]
   - (m_\phi C\Delta t)^2 \phi^{n}_{i,j,k}
   + \frac{\Delta t^2}{\epsilon_0} J^{n}_{i,j,k}.
   \]
7. **Extract EM fields:** Identify the electric component as \(E = -\partial_t \phi\) and magnetic as \(B = \nabla \times \mathbf{A}\) (if using vector potential) or directly from \(\phi\) if a scalar representation suffices.
8. **Analyze output:** Compute the Poynting vector, spectrum, and look for whirlpool signatures (rotating phase patterns).

### 4.7 Analytical Approximation (Far‑Field)
For distances \(r \gg\) Planck length, the retarded potential yields
\[
\mathbf{E}(\mathbf{r},t) \approx \frac{q}{4\pi\epsilon_0}
\left[
\frac{\mathbf{n} \times [(\mathbf{n} - \boldsymbol{\beta}) \times \dot{\boldsymbol{\beta}}]}
{(1 - \mathbf{n}\cdot\boldsymbol{\beta})^3 r}
\right]_{\text{ret}},
\]
where \(\boldsymbol{\beta} = \mathbf{v}/c\), \(\mathbf{n}\) is the unit vector from source to field point, and all quantities evaluated at retarded time \(t_r = t - r/c\). Insert \(\mathbf{v} = \boldsymbol{\Omega}_G \times \mathbf{r}_e\) and \(\dot{\boldsymbol{\beta}} = \dot{\boldsymbol{\Omega}}_G \times \mathbf{r}_e + \boldsymbol{\Omega}_G \times \mathbf{v}\) (with \(\dot{\boldsymbol{\Omega}}_G\approx 0\) for steady galactic rotation).

## 5. Deliverables
- A concise technical report summarizing derived formulas and simulation procedures.
- A GitHub repository containing:
  - LaTeX source for the paper.
  - Python/Julia scripts implementing the FDTD solver.
  - Manim animation scenes illustrating the electron whirlpool and photon emission.
  - Audio narration script (`Script.md`) for a YouTube video explaining the theory step‑by‑step.
