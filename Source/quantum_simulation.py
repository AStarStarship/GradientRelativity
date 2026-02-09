#!/usr/bin/env python3
"""
Quantum physics simulation to estimate the 'space' associated with an electron
transition that emits radiation at a given RF frequency.

The model:
1. An electron drops from a higher energy state to a lower one, emitting a photon
   with frequency f (Hz). The photon's energy is E = h * f.
2. The wavelength of the emitted radiation is λ = c / f.
3. Approximate the spatial extent of the emitted photon as a sphere whose
   diameter is λ. The volume of this sphere represents a crude estimate of the
   'space stored' in the transition.
4. The volume V = 4/3 * π * (λ/2)^3.

This script can be used to compute the space for any given energy difference
(or directly for a frequency).
"""

import math

# Physical constants
PLANCK_CONSTANT_J_S = 6.62607015e-34          # h
SPEED_OF_LIGHT_M_S = 299_792_458             # c
ELECTRON_MASS_KG = 9.10938356e-31             # m_e
EV_TO_JOULE = 1.602176634e-19                # conversion factor

def frequency_from_energy_diff_ev(energy_diff_ev: float) -> float:
    """
    Convert an energy difference in electronvolts to an equivalent frequency.
    
    Parameters
    ----------
    energy_diff_ev : float
        Energy difference in electronvolts (eV).
    
    Returns
    -------
    float
        Frequency in hertz (Hz).
    """
    energy_joules = energy_diff_ev * EV_TO_JOULE
    return energy_joules / PLANCK_CONSTANT_J_S

def wavelength_from_frequency(frequency: float) -> float:
    """
    Compute the wavelength of electromagnetic radiation.
    
    Parameters
    ----------
    frequency : float
        Frequency in hertz (Hz).
    
    Returns
    -------
    float
        Wavelength in meters (m).
    """
    return SPEED_OF_LIGHT_M_S / frequency

def space_volume_from_energy_diff_ev(energy_diff_ev: float) -> float:
    """
    Estimate the 'space' (as a volume) associated with an electron transition
    that emits radiation corresponding to the given energy difference.
    
    Parameters
    ----------
    energy_diff_ev : float
        Energy difference in electronvolts (eV).
    
    Returns
    -------
    float
        Volume in cubic meters (m^3) representing the estimated space.
    """
    f = frequency_from_energy_diff_ev(energy_diff_ev)
    wavelength = wavelength_from_frequency(f)
    radius = wavelength / 2.0  # Using diameter = wavelength
    volume = (4.0 / 3.0) * math.pi * (radius ** 3)
    return volume

def space_volume_from_frequency(frequency: float) -> float:
    """
    Estimate the 'space' associated with a given frequency directly.
    
    Parameters
    ----------
    frequency : float
        Frequency in hertz (Hz).
    
    Returns
    -------
    float
        Volume in cubic meters (m^3).
    """
    wavelength = wavelength_from_frequency(frequency)
    radius = wavelength / 2.0
    return (4.0 / 3.0) * math.pi * (radius ** 3)

if __name__ == "__main__":
    # Example usage:
    # 1. Transition with energy difference of 1 microelectronvolt (μeV)
    energy_ev = 1e-6  # 1 μeV
    vol = space_volume_from_energy_diff_ev(energy_ev)
    print(f"Energy difference: {energy_ev:.2e} eV")
    print(f"Estimated space volume: {vol:.2e} m³")

    # 2. Directly using an RF frequency, e.g., 1 GHz
    freq_example = 1e9  # 1 GHz
    vol2 = space_volume_from_frequency(freq_example)
    print(f"\nFrequency: {freq_example:.2e} Hz")
    print(f"Estimated space volume: {vol2:.2e} m³")