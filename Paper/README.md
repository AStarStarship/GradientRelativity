# Gradient Relativity research paper

Read [On the Electrodynamics of Gravitational Equilibriums](RoughDraftImproved.md), the current
working manuscript. [RoughDraft.md](RoughDraft.md) is preserved as historical notes; its
unaudited equations and earlier interpretations are not current results.

## Current account

The proposed highest space/EM-energy state lies between masses, at 100% oscillation and
maximum expansion normalized to 1. Pressure drives space into both masses. Condensation is
proposed to contract the intervening space and reduce separation, not repel the masses.

The manuscript also covers the proposed internal two-turn electron cycle, source/receiver
transport through possible paths, and a black-hole center with slow internal motion,
stored mass energy, and incoming-interaction restart. The proposed 0% endpoint applies to
the space/EM component, not total energy. A central majority-electron population is an
assumption, and the center is distinct from the horizon.

These are postulates. The animations do not solve the pressure law, conserved dynamics,
operational geometry, electron structure, or path integral. The two speed-law candidates
remain unresolved; candidate experiments are not numerical predictions.

## Supporting sections

1. [Abstract](Abstract/README.md)
2. [Summary](Summary/README.md)
3. [Theoretical overview](TheoreticalOverview/README.md)
4. [Mathematical foundations](MathmaticalFoundations/README.md)
   - [Special relativity review](MathmaticalFoundations/README.md#special-relativity-review)
   - [Gradient Relativity fundamentals](MathmaticalFoundations/README.md#gradient-relativity-fundamentals)
   - [Hairy ball theory](MathmaticalFoundations/README.md#hairy-ball-theory)
5. [Core equations](CoreEquations/README.md)
   - [Energy-momentum relation](CoreEquations/README.md#energy-momentum-relation)
   - [Planck-scale relations](CoreEquations/README.md#planck-scale-relations)
   - [Driven harmonic oscillator](CoreEquations/README.md#driven-harmonic-oscillator)
6. [Physical interpretations](PhysicalInterpretations/README.md)
   - [Electromagnetic waves and gravity](PhysicalInterpretations/README.md#electromagnetic-waves-and-gravity)
   - [Space-to-mass conversion](PhysicalInterpretations/README.md#space-to-mass-conversion)
   - [Black-hole dynamics](PhysicalInterpretations/README.md#black-hole-dynamics)
   - [Dark-matter hypothesis](PhysicalInterpretations/README.md#dark-matter-hypothesis)
7. [Cosmological implications](CosmologicalImplications/README.md)
   - [Universal expansion and heat death](CosmologicalImplications/README.md#universal-expansion-and-heat-death)
   - [Big Bang and multiverse scenarios](CosmologicalImplications/README.md#big-bang-and-multiverse-scenarios)
8. [Experimental considerations](ExperimentalConsiderations/README.md)
   - [Photon nature](ExperimentalConsiderations/README.md#photon-nature)
   - [Electron measurement techniques](ExperimentalConsiderations/README.md#electron-measurement-techniques)
   - [Conducting surface phenomena](ExperimentalConsiderations/README.md#conducting-surface-phenomena)
   - [Double-slit experiment insights](ExperimentalConsiderations/README.md#double-slit-experiment-insights)
9. [Discussion](Discussion/README.md)
   - [Speed of light invariance](Discussion/README.md#speed-of-light-invariance)
   - [Conservation laws](Discussion/README.md#conservation-laws)
10. [Conclusion](Conclusion/README.md)
11. [Research plan](Research.md) and [equation audit](EquationAudit.md)
12. [Task list](Todo/README.md) and [falsification roadmap](Todo/electron_cycle_falsification.md)
13. [Retrieved Markdown context](../Reseach/README.md), separate from the existing `Research` directory

## Build a readable preview

This README is an index, not the assembled manuscript. From the repository root:

    mkdir -p Paper/artifacts
    pandoc Paper/RoughDraftImproved.md --from=markdown+tex_math_single_backslash \
      --standalone --mathml --embed-resources --resource-path=Paper \
      --output=Paper/artifacts/gradient_relativity.html

The standalone HTML contains native MathML and an embedded overview image. A PDF build
requires a compatible PDF engine; an HTML export is not evidence that PDF typesetting has
passed. The source-linked manuscript declares which relations are references, postulates,
illustrations, or recorded approximations.
