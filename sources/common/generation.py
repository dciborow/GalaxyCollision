import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rv_continuous

from sources.common.gravitation import *


def particleRing(nb, radius, gravityCst, mass):
    particles = []
    velocities = []
    theta = 0
    arcLength = (2 * np.pi) / nb
    v = np.sqrt(gravityCst * mass / radius)
    while len(particles) < nb:
        angle = theta * arcLength
        beta = angle + np.pi / 2
        theta += 1
        particles.append([radius * np.cos(angle), radius * np.sin(angle)])
        velocities.append([v * np.cos(beta), v * np.sin(beta)])
    return np.array(particles), np.array(velocities)


def generateDisk2D(nbStars, radius, mass, gravityCst, seed=None):
    np.random.seed(seed)

    # Calculating positions
    positions = np.zeros(shape=(nbStars, 2))
    distances = np.random.random((nbStars,)) * radius
    angles = np.random.random((nbStars,)) * 2 * np.pi
    positions[:, 0] = np.cos(angles) * distances
    positions[:, 1] = np.sin(angles) * distances

    # Calculating speeds
    velocities = np.zeros(shape=(nbStars, 2))
    masses = np.random.random((nbStars,))
    masses = masses * mass / np.sum(masses)
    for i in range(nbStars):
        mask = distances < distances[i]
        internalMass = np.sum(masses[mask])
        escVelocityNorm = np.sqrt(gravityCst * internalMass / distances[i])
        velocities[i, 0] = escVelocityNorm * np.cos(angles[i] + np.pi / 2)
        velocities[i, 1] = escVelocityNorm * np.sin(angles[i] + np.pi / 2)
    return positions, velocities, masses


def generateDisk3D(nbStars, radius, mass, zOffsetMax, gravityCst, seed=None):
    np.random.seed(seed)

    # Calculating positions
    positions = np.zeros(shape=(nbStars, 3))
    distances = np.random.random((nbStars,))
    zOffsets = (np.random.random((nbStars,)) - 0.5) * 2 * zOffsetMax * (np.ones_like(distances) - np.sqrt(distances))
    distances = distances * radius
    angles = np.random.random((nbStars,)) * 2 * np.pi
    positions[:, 0] = np.cos(angles) * distances
    positions[:, 1] = np.sin(angles) * distances
    positions[:, 2] = zOffsets

    # Calculating speeds
    velocities = np.zeros(shape=(nbStars, 3))
    masses = np.random.random((nbStars,))
    masses = masses * mass / np.sum(masses)
    for i in range(nbStars):
        mask = distances > distances[i]
        internalMass = np.sum(masses[mask])
        velNorm = np.sqrt(gravityCst * internalMass / distances[i]) / 2
        velocities[i, 0] = velNorm * np.cos(angles[i] + np.pi / 2)
        velocities[i, 1] = velNorm * np.sin(angles[i] + np.pi / 2)
        velocities[i, 2] = np.zeros_like(velocities[i, 2])
    return positions, velocities, masses


def generateUniformSphere(nbStars=1000, radius=1, mass=1, gravityCst=1,  seed=None):
    """https://stackoverflow.com/questions/5408276/sampling-uniformly-distributed-
    random-points-inside-a-spherical-volume"""
    rng = np.random.default_rng(seed)
    positions = rng.normal(size=(nbStars, 3))
    normalize_radii = np.linalg.norm(positions, axis=1)[:, np.newaxis]
    positions /= normalize_radii
    uniform_points = rng.uniform(size=nbStars)[:, np.newaxis]
    new_radii = np.power(uniform_points, 1 / 3)
    positions *= new_radii
    positions = positions * radius

    # Calculating masses
    masses = np.random.random((nbStars,))
    masses = masses * mass / np.sum(masses)

    # Calculating velocities
    velocities = np.zeros(shape=(nbStars, 3))
    distances = np.sqrt(positions[:, 0] ** 2 + positions[:, 1] ** 2 + positions[:, 2] ** 2)
    return positions, velocities, masses


#################### DISTRIBUTIONS ####################

def uniformSphereDistribution(r, r0=1, M=1):
    exteriorMask = r > r0
    density = 3 * M / (4 * np.pi * r0 ** 3)
    density[exteriorMask] = 0
    return density


def isothermalSphereDistribution(r, p0=1, r0=1):
    return p0 * (r / r0) ** (-2)


def sphericalPlummerDistribution(r, r0=1, M=1):
    return (3 * M) / (4 * np.pi) * (r0 ** 2) / (r0 ** 2 + r ** 2) ** (3 / 2)


def sphericalHernquistDistribution(r, r0=1, M=1):
    return M / (2 * np.pi) * r0 / (r * (r0 + r) ** 3)


def sphericalJaffeDistribution(r, r0=1, M=1):
    return M / (4 * np.pi) * r0 / (r ** 2 * (r0 + r) ** 2)
