from sources.common.gravitation import *
from sources.galaxies import *


class MasslessGalaxy(ObjectCluster2D):
    def __init__(self, positions, velocities, centralMass, haloRadius):
        super(MasslessGalaxy, self).__init__(positions, velocities)
        self.centerPosition = None
        self.centerVelocity = None
        self.centralMass = centralMass
        self.haloRadius = haloRadius
        self.haloVelocity = 2 * np.sqrt(self.gravitationCst * self.centralMass / self.haloRadius)

    def initialState(self, xc, vc):
        if isinstance(xc, list):
            xc = np.array([xc])
            xc = xc.reshape(2, )
        if isinstance(vc, list):
            vc = np.array([vc])
            vc = vc.reshape(2, )
        self.positions += xc
        self.velocities += vc
        self.centerPosition = xc
        self.centerVelocity = vc
        self.initialized = True

    def interiorMass(self, radii):
        indices = radii < self.haloRadius
        masses = np.zeros_like(radii)
        if masses[indices].shape != (0,):
            masses[indices] = self.haloVelocity ** 2 * radii[indices] ** 3 / \
                              (self.gravitationCst * (radii[indices] + self.haloRadius) ** 2)
        if masses[~indices].shape != (0,):
            masses[~indices] = self.centralMass
        return masses

    def density(self, radii):
        radii_in = 0.99 * radii
        radii_out = 1.01 * radii
        M_in = self.interiorMass(radii_in)
        M_out = self.interiorMass(radii_out)
        dM = M_out - M_in
        dV = (4 / 3) * np.pi * (radii_out ** 3 - radii_in ** 3)
        return dM / dV

    def dynamicFriction(self, radii, velocities, centralVelocity, mass):
        rho = self.density(radii)
        velocityVec = velocities - centralVelocity
        velocities = np.linalg.norm(velocityVec)
        return -4 * np.pi * self.gravitationCst ** 2 * 3 * mass * rho * velocityVec / (1 + velocities) ** 3


class RingsMasslessGalaxy(MasslessGalaxy):
    def __init__(self, radii, particles, centralMass, haloRadius):
        assert len(radii) == len(
            particles
        ), f"len(radii): {len(radii)} not equal to len(particles): {len(particles)}"

        G = gravitationalConstant()
        positions = []
        velocities = []
        for i in range(len(particles)):
            X, V = particleRing(particles[i], radii[i], G, centralMass)
            positions.append(X)
            velocities.append(V)
        positions = np.concatenate(positions)
        velocities = np.concatenate(velocities)
        super(RingsMasslessGalaxy, self).__init__(positions, velocities, centralMass, haloRadius)
