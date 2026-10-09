# Gradient Relativity — Equation Audit & Corrections
**Author:** Cale McCollough
**Date:** 2026-09-05
**Purpose:** Track every equation in the Rough Draft, flag errors, provide corrections, and note what needs proper derivation.

Current interpretation: see [the revised manuscript](RoughDraftImproved.md). Audit history
and a corrected template do not establish a self-sustaining electron or conserved field
dynamics. The spatial 100% endpoint is not a demonstrated local light-speed maximum.

---

## E1. Vacuum Permittivity (Line 22 / Quora)

### Original
```
ε₀ = 1 / (μ₀ · C³)
```

### Error
Wrong power on C. Dimensional analysis:
- ε₀ has units F/m = C²·s²/(kg·m³)
- μ₀ has units N/A² = kg·m/(C²)
- C has units m/s
- μ₀·C² → (kg·m/C²)·(m²/s²) = kg·m³/(C²·s²)
- 1/(μ₀·C²) → C²·s²/(kg·m³) = F/m ✓

C³ gives wrong dimensions.

### Correction
```
ε₀ = 1 / (μ₀ · c²)
```
or equivalently:
```
c = 1 / √(ε₀ · μ₀)
```

---

## E2. Gravitational Equilibrium (Line 18 / Quora)

### Original
```
(E − pv) / M = q · ε_c · sin(π/2)
```

### Error
Dimensional mismatch:
- Left side: (J − kg·m/s · m/s) / kg = (J − J) / kg = J/kg = m²/s² (energy per unit mass)
- Right side: q·ε_c = C · F/m = C²/(N·m) = C²·s²/(kg·m²)
- sin(π/2) = 1 (dimensionless)
- Right side units: C²·s²/(kg·m²) ≠ m²/s²

No physical basis for equating energy-per-mass to charge times permittivity.

### Correction
This equation appears to be an **original claim** of Gradient Relativity, not a derived result from established physics. It should be rewritten as a **definition/ansatz** rather than presented as an equality derived from known laws.

Suggested rewrite (as a postulate):
```
Postulate: The space-energy gradient at gravitational equilibrium satisfies
    (E − p·c) / M = Φ₀
where Φ₀ is a fundamental field potential with units of specific energy (J/kg = m²/s²),
and Φ₀ relates to the local permittivity through the Planck field constant.
```

---

## E3. q·ε₀·sin(π/2) = C² (Line 28 / Quora)

### Original
```
q · ε₀ · sin(π/2) = C²
```

### Error
Dimensional analysis:
- q·ε₀ = C · F/m = C²/(N·m) = C²·s²/(kg·m²)
- C² = (m/s)² = m²/s²
- C²·s²/(kg·m²) ≠ m²/s²

These quantities have completely different dimensions. This is false.

### Correction
This equation has no basis in physics. The closest legitimate relation is:
```
c = 1 / √(ε₀ · μ₀)
```
which relates c to electromagnetic constants, not to charge.

If the intent is to define a **normalized** relation in natural units where c=1, then:
```
In natural units (c = ℏ = ε₀ = 1):
    q² / (4π) = α ≈ 1/137  (fine structure constant)
```
But this doesn't give C² = q·ε₀.

---

## E4. Harmonic Oscillator Taylor Series (Line 30 / Quora)

### Original
```
Ma = −M·ω_R²·x − q·ε₀ · Σ[k=0 to ∞] [(-1)^(2k+1) / (2k+1)!] · (α + ωt)^(2k+1)
```

### Status: DIMENSIONAL TEMPLATE, NOT A VALIDATED DRIVER
The current manuscript uses m_e·ẍ + k_eff·x = F_drive(t), with
ω₀ = √(k_eff/m_e). A Compton reference-frequency identification is not an
electron-structure derivation. The earlier m_e·a_c substitution and recorded numerical
displacement remain a classical approximation; constant forcing gives a displaced
equilibrium, not an automatic persistent internal mode. Galactic coordinate acceleration
alone does not establish radiating proper acceleration. The incoming-photon mechanism
requires its own coupling and energy budget.

### Error (kept for reference)
The Taylor series Σ [(-1)^(2k+1) / (2k+1)!] · θ^(2k+1) = −sin(θ).
So the right side is: −M·ω_R²·x + q·ε₀·sin(α + ωt)

But the driving term should be force, not charge·permittivity.
- q·ε₀ has units C²·s²/(kg·m²)
- Force has units kg·m/s²

These don't match. The driving force should be q·E(t) where E(t) is the electric field.

### Correction
```
m·a = −m·ω_R²·x + q·E₀·sin(ωt + α)
```
where E₀ is the amplitude of the driving electric field.

The ε₀ in the original was a confusion between permittivity and field strength.

---

## E5. Mass from Energy (Line 33 / Quora)

### Original
```
m_C = (E − pv) / (q · ε₀)
```

### Error
- Numerator: J − J = J (energy)
- Denominator: C²·s²/(kg·m²) (from E2 analysis)
- Result: J / (C²·s²/(kg·m²)) = kg·m²/s² · kg·m²/(C²·s²) = kg²·m⁴/(C²·s⁴)

This is not mass (kg). Dimensionally wrong.

### Correction
If the claim is that mass = condensed space with E = mc²:
```
m = E / c²
```
This is standard. The division by q·ε₀ has no physical basis.

---

## E6. Planck Length (Line 39 / Quora)

### Original
```
l_plank = √(ħ · G_Space / 1³) ≈ 0
```

### Error
Standard Planck length:
```
l_P = √(ħ·G / c³)
```
Setting c = 1 gives l_P = √(ħ·G), which is NOT ≈ 0.
l_P ≈ 1.616 × 10⁻³⁵ m (a very small but non-zero number).

The claim that l_plank ≈ 0 at gravitational equilibrium is incorrect.
The current spatial 100% label is not a measured maximum of local vacuum light speed.
The reference formula uses c₀; a hypothetical variable-speed substitution and a claim
about its extrema need a separate derivation.

### Correction
```
l_P = √(ħ·G / c³) ≈ 1.616 × 10⁻³⁵ m   (in vacuum, c = c₀)
```
If proposing a **variable** Planck length due to variable c:
```
l_P(x) = √(ħ·G / c(x)³)
```
where c(x) is the local speed of light at position x.

---

## E7. Angular Frequency (Line 41 / Quora)

### Original
```
ω_R = √(−q·ε₀ / (M·x))
```

### Error
- q·ε₀/(M·x) has units: [C²·s²/(kg·m²)] / [kg·m] = C²·s²/(kg²·m³)
- This is not 1/s² (frequency squared)
- The negative sign under the square root gives an imaginary number

The imaginary result indicates the equation is not describing a real oscillation frequency
but rather an instability or an invalid parameter regime.

### Correction
For a driven harmonic oscillator, the natural frequency is:
```
ω₀ = √(k_eff / m)
```
where k_eff is the effective spring constant.

If the "Planck spring constant" is k_P, then:
```
ω₀ = √(k_P / m_e)
```
with k_P having units N/m = kg/s².

---

## E8. Planck Energy (Line 43 / Quora)

### Original
```
E_plank = q·ε₀ · √(sin²(ω_plank + α) + cos²(ω_plank + α))
```

### Error
The expression √(sin²(θ) + cos²(θ)) = √(1) = 1 for all θ.
So this simplifies to: E_plank = q·ε₀

But q·ε₀ is not an energy (wrong dimensions, see E2).

The trigonometric identity sin² + cos² = 1 is being used as if it's a meaningful
physical result, but it's a tautology.

### Correction
Standard Planck energy:
```
E_P = √(ħ·c⁵ / G) ≈ 1.956 × 10⁹ J ≈ 1.22 × 10¹⁹ GeV
```

If the intent is to express energy as an oscillating quantity:
```
E(t) = E₀ · sin²(ωt + α)  or  E(t) = E₀ · |sin(ωt + α)|²
```
But this needs a proper derivation from a Lagrangian.

---

## E9. Speed of Light Normalization (Line 46 / Quora)

### Original
```
ε_c = 1 / ε₀
```

### Error
If ε_c is the "normalized" permittivity in units where c=1:
```
c = 1/√(ε_c·μ_c) = 1
```
Then ε_c·μ_c = 1, and μ_c = 1/ε_c.

But ε_c ≠ 1/ε₀. In natural units, ε₀ = 1 (dimensionless).
The relation should be:
```
ε_c = ε₀ (in SI: ε₀ ≈ 8.854 × 10⁻¹² F/m)
μ_c = μ₀ (in SI: μ₀ = 4π × 10⁻⁷ N/A²)
```
In natural units, both are set to 1.

---

## E10. Time Dilation (Line 52 / Quora)

### Original
```
1 = (dx/dt)² + (dτ/dt)² = 1/√(μ_c·ε_c) = C₁
```

### Error
The GR time dilation formula is:
```
dτ = dt · √(1 − v²/c²)
```
or equivalently:
```
(dτ/dt)² = 1 − (v/c)² = 1 − (dx/dt)²/c²
```
Rearranging:
```
(c·dτ/dt)² + (dx/dt)² = c²
```
If c = 1 (natural units):
```
(dτ/dt)² + (dx/dt)² = 1
```
This is **correct in form** but the original writes (dx/dt)² + (dτ/dt)² = 1
which is the same thing (addition is commutative).

However, equating this to 1/√(μ_c·ε_c) = c is only valid when c = 1.
The chain of equalities is misleading.

### Correction
```
In natural units (c = 1):
    (dτ/dt)² + (dx/dt)² = 1
    where dx/dt = v (proper velocity normalized to c)
    and dτ/dt = 1/γ (time dilation factor)

In SI units:
    c²·(dτ/dt)² + (dx/dt)² = c²
```

---

## E11. Energy-Momentum Relation (Line 85 / Quora)

### Original
```
E² = (MC²)² + (pc)²
```
and the claim: "when you plug in p for the momentum you get E = MC²"

### Error
- E² = (mc²)² + (pc)² is the **correct** relativistic energy-momentum relation.
- For a massive particle at rest (p = 0): E = mc² ✓
- For a photon (m = 0): E = pc ✓
- The claim "plug in p for momentum you get E = MC²" is wrong.
  If m = 0, E = pc, NOT E = mc².

### Correction
```
E² = (mc²)² + (pc)²
    m = 0  →  E = pc  (photon)
    p = 0  →  E = mc²  (rest mass)
```

---

## E12. C² = E/M (Line 85 / Quora)

### Original
```
C² = E/M
```

### Error
From E = mc²: c² = E/m for a particle at rest.
But E/M without specifying rest energy is ambiguous.

In the context of the space-energy gradient:
```
c² = E_space / E_mass  ??
```
This is a **proposal**, not a derived result. It should be stated as an ansatz.

### Correction (dimensionless postulate; still unresolved)
```
Gradient Relativity Postulate:
    u²(x) = E_space(x) / E_mass(x),  u = c_model/c₀
where both energies (or both energy densities) have the same dimensions.
```

The ratio is dimensionless, so it cannot equal an SI speed squared without a reference
speed factor. Under the same internal fraction definition this P1 law is not equivalent
to the bounded prototype u = 2√(σ(1−σ)); their pure-space limits disagree. Neither law
derives the author's spatial 100% endpoint, pressure, or operational contraction.

---

## E13. Driven Harmonic Oscillator (Line 107 / Quora)

### Original
```
Ma = −M·ω_R²·x − q·ε₀·sin(ωt)
```

### Error
Same as E4. The driving force should be q·E(t), not q·ε₀·sin(ωt).
- q·ε₀ has wrong dimensions for force
- The electric field E(t) = E₀·sin(ωt) has units V/m = N/C

### Correction
```
m·(d²x/dt²) = −m·ω₀²·x + q·E₀·sin(ωt)
```

---

## E14. Schwarzschild Metric (Line 134 / Quora)

### Original
```
ds² = (1 − R_s/r)dt² + (1/(1 − R_s/r))dr² + r²dΩ²
```

### Error
Missing the c² factor in the time component.

### Correction
```
ds² = −(1 − R_s/r)·c²·dt² + (1 − R_s/r)⁻¹·dr² + r²·dΩ²
```
where R_s = 2GM/c² is the Schwarzschild radius.

In natural units (c = 1):
```
ds² = −(1 − R_s/r)·dt² + (1 − R_s/r)⁻¹·dr² + r²·dΩ²
```

---

## E15. Mass-Energy Inverse (Line 74 / Quora)

### Original
```
m = C² / E
```

### Error
From E = mc²: m = E/c², NOT m = c²/E.
The original has it inverted.

### Correction
```
m = E / c²
```

---

## Summary of Corrections Needed

| # | Original | Status | Action |
|---|----------|--------|--------|
| E1 | ε₀ = 1/(μ₀·C³) | WRONG | Fix to C² |
| E2 | (E−pv)/M = q·ε_c·sin(π/2) | WRONG DIMS | Convert to postulate |
| E3 | q·ε₀·sin(π/2) = C² | WRONG DIMS | Remove or reframe |
| E4 | Ma = −Mω_R²x − q·ε₀·sin(ωt) | WRONG DIMS | Use q·E₀ instead |
| E5 | m_C = (E−pv)/(q·ε₀) | WRONG DIMS | Use m = E/c² |
| E6 | l_plank = √(ħ·G/1³) ≈ 0 | WRONG VALUE | l_P ≈ 1.6×10⁻³⁵ m |
| E7 | ω_R = √(−q·ε₀/Mx) | WRONG DIMS | Use ω₀ = √(k/m) |
| E8 | E_plank = q·ε₀·√(sin²+cos²) | TAUTOLOGY | Use standard E_P |
| E9 | ε_c = 1/ε₀ | WRONG | ε_c = ε₀ (natural units: 1) |
| E10 | 1 = (dx/dt)² + (dτ/dt)² | FORM OK, MISLEADING | Clarify units |
| E11 | E²=(MC²)²+(pc)², then "E=MC²" | PARTIAL | Correct the photon case |
| E12 | C² = E/M | AMBIGUOUS | State as postulate |
| E13 | Ma = −Mω_R²x − q·ε₀·sin(ωt) | WRONG DIMS | Use q·E₀ |
| E14 | ds² = (1−Rs/r)dt² + ... | MISSING c² | Add c² factor |
| E15 | m = C²/E | INVERTED | Use m = E/c² |

---

## Equations That Are Actually Correct

1. **E = mc²** (standard, correct)
2. **E² = (mc²)² + (pc)²** (standard, correct)
3. **c = 1/√(ε₀·μ₀)** (standard, correct — if written with c² not c³)
4. **h = 6.62607015 × 10⁻³⁴ J·s** (correct value)
5. **ħ = h/(2π)** (correct definition)
6. **Planck length formula form** l_P = √(ħ·G/c³) — correct FORM, wrong evaluation
7. **Time dilation form** (dτ/dt)² + (dx/dt)² = 1 — correct in natural units
8. **Schwarzschild radius** form (1 − R_s/r) — correct structure

---

## Priority Corrections for the Paper

### MUST FIX (dimensionally wrong):
1. E1: ε₀ = 1/(μ₀·c²) not c³
2. E4/E13: Replace q·ε₀ with q·E₀ in harmonic oscillator
3. E5: m = E/c², not (E−pv)/(q·ε₀)
4. E8: Remove tautological sin²+cos² = 1 as physical result
5. E9: ε_c = ε₀, not 1/ε₀
6. E15: m = E/c², not c²/E

### SHOULD REFRAME (original claims, not derived):
1. E2: Present as postulate, not derived equality
2. E3: Remove entirely or reframe as definition of a new constant
3. E7: Derive ω₀ from a proper spring constant model
4. E12: State as Gradient Relativity postulate

### MINOR FIXES:
1. E6: Correct Planck length value and interpretation
2. E10: Clarify unit conventions throughout
3. E14: Add c² to Schwarzschild metric
