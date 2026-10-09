import torch
import math

# -----------------------------
# 1. Basic setup and parameters
# -----------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"

# 1D lattice = toy "space"
num_sites = 128
x = torch.arange(num_sites, device=device)

# Time steps
num_steps = 1000
dt = 0.01

# Electron phases φ(x, t): start random or localized
phi = torch.zeros(num_sites, device=device)
phi[num_sites // 2] = math.pi / 4  # one electron in the middle

# Oscillation frequency (can be learned later with PyTorch optim)
omega = torch.tensor(5.0, device=device, requires_grad=True)

# Energy levels for the two phases
rho_space = torch.tensor(1.0, device=device, requires_grad=True)  # "100% space energy"
rho_mass  = torch.tensor(10.0, device=device, requires_grad=True) # "100% mass energy"

# Coupling constant: curvature ~ 8πG * energy density (toy)
kappa = torch.tensor(1.0, device=device, requires_grad=True)

# -----------------------------
# 2. Electron oscillation model
# -----------------------------
# φ(t) evolves as a simple harmonic oscillator:
#   φ(t+dt) = φ(t) + ω dt
# Local energy density ρ(φ) oscillates between rho_space and rho_mass.
# Use a smooth mapping: ρ(φ) = rho_space + (rho_mass - rho_space) * sin^2(φ)

def update_phase(phi, omega, dt):
    return phi + omega * dt

def energy_density(phi, rho_space, rho_mass):
    # sin^2 maps [0, 2π] to [0, 1], giving a clean 2-phase oscillation
    s2 = torch.sin(phi) ** 2
    return rho_space + (rho_mass - rho_space) * s2

# -----------------------------
# 3. GR-like curvature relation
# -----------------------------
# Toy Einstein equation:
#   curvature(x) = kappa * ρ_eff(x)
# Here ρ_eff is just ρ(φ); later you could average over time or electrons.

def curvature_from_density(rho, kappa):
    return kappa * rho

# -----------------------------
# 4. Hypergraph interpretation
# -----------------------------
# Interpret curvature as "update density" in a hypergraph-like model:
#   u(x) ~ curvature(x)
# In a real Wolfram-style model, u(x) would control rewrite frequency.

def update_density_from_curvature(curv):
    # For now, identity; could be nonlinear later
    return curv

# -----------------------------
# 5. Law of sines proxy for curvature gradient
# -----------------------------
# Take three neighboring sites (i-1, i, i+1) and treat their curvatures
# as sides of a triangle. Use the law of sines to define an "angle"
# that encodes how sharply curvature changes around site i.
#
# Law of sines: a/sin(A) = b/sin(B) = c/sin(C) = 2R
# We'll define an effective angle at site i using:
#   sin(θ_i) ∝ |curv_{i+1} - curv_{i-1}| / (2 * curv_i + ε)
# This is not literal geometry, but a geometric *analogy*:
# larger curvature contrast → larger "angle" → stronger gradient.

eps = 1e-6

def curvature_angle_law_of_sines(curv):
    # pad for boundaries
    c_left  = torch.roll(curv, 1)
    c_right = torch.roll(curv, -1)
    c_mid   = curv

    # "opposite side" ~ difference of neighbors
    opp = torch.abs(c_right - c_left)
    base = 2.0 * c_mid + eps

    # clamp argument of arcsin to [-1, 1]
    sin_theta = torch.clamp(opp / (base + eps), -1.0, 1.0)
    theta = torch.arcsin(sin_theta)  # effective "curvature angle"

    return theta

# -----------------------------
# 6. Time evolution loop (toy)
# -----------------------------

phi_history = []
rho_history = []
curv_history = []
angle_history = []

phi_t = phi.clone()

for t in range(num_steps):
    # Update phase (electron oscillation)
    phi_t = update_phase(phi_t, omega, dt)

    # Local energy density from phase
    rho_t = energy_density(phi_t, rho_space, rho_mass)

    # Curvature from density (Einstein-like)
    curv_t = curvature_from_density(rho_t, kappa)

    # Hypergraph update density
    u_t = update_density_from_curvature(curv_t)

    # Law-of-sines-based curvature angle (gradient proxy)
    theta_t = curvature_angle_law_of_sines(curv_t)

    # Store for analysis/visualization
    phi_history.append(phi_t.detach().cpu().clone())
    rho_history.append(rho_t.detach().cpu().clone())
    curv_history.append(curv_t.detach().cpu().clone())
    angle_history.append(theta_t.detach().cpu().clone())

# At this point you can:
# - Plot rho_history as the oscillating source term T_{00}(x, t)
# - Plot curv_history as the induced curvature G_{00}(x, t)
# - Plot angle_history as a geometric proxy for curvature gradients
# - Use PyTorch optim to fit omega, rho_space, rho_mass, kappa to any target behavior
