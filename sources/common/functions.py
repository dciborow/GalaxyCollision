import numpy as np
import matplotlib.pyplot as plt


def gravitationalConstant():
    return 4.302e-3  # pc(M_solar)^-1 (km/s)^2


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
    masses = np.random.random((nbStars,)) * mass
    for i in range(nbStars):
        mask = distances > distances[i]
        internalMass = np.sum(masses[mask])
        velNorm = np.sqrt(gravityCst * internalMass / distances[i])
        velocities[i, 0] = velNorm * np.cos(angles[i])
        velocities[i, 0] = velNorm * np.sin(angles[i])
    return positions, velocities, masses


def generateArms2D(nbStars, nbArms, radius, armOffset, mass, rotFactor, gravityCst, seed=None):
    np.random.seed(seed)
    armSeparationDistance = 2 * np.pi / nbArms
    distances = np.random.random((nbStars,)) ** 2
    angles = np.random.random((nbStars,)) * 2 * np.pi

    # Calculating arm offsets
    armOffsets = np.random.random((nbStars,)) * armOffset
    armOffsets = armOffsets - armOffset / 2
    armOffsets = armOffsets / distances
    squaredArmOffsets = armOffsets ** 2
    mask = armOffsets < 0
    squaredArmOffsets[mask] = -1 * squaredArmOffsets[mask]
    armOffsets = squaredArmOffsets

    # Rotation angles
    rotations = distances * rotFactor
    angles = ((angles / armSeparationDistance) * armSeparationDistance + armOffsets + rotations)
    for i in range(nbStars):
        angles[i] = int(angles[i])

    # Calculating positions
    positions = np.zeros(shape=(nbStars, 2))
    positions[:, 0] = np.cos(angles) * distances
    positions[:, 1] = np.sin(angles) * distances

    # Calculating speeds
    velocities = np.zeros(shape=(nbStars, 2))
    masses = np.random.random((nbStars,)) * mass
    for i in range(nbStars):
        mask = distances > distances[i]
        internalMass = np.sum(masses[mask])
        velNorm = np.sqrt(gravityCst * internalMass / distances[i])
        velocities[i, 0] = velNorm * np.cos(angles[i])
        velocities[i, 0] = velNorm * np.sin(angles[i])
    return positions, velocities, masses


def plotGalaxyDisk2D(nbStars=1000):
    fig = plt.figure(figsize=(10, 10))
    fig.patch.set_facecolor('xkcd:black')  # Changing figure to black
    ax = fig.add_subplot(111)
    ax.set_facecolor('xkcd:black')  # Changing background to black
    G = gravitationalConstant()
    positions, velocities, masses = generateDisk2D(nbStars, 1, 3, G)
    X = positions[:, 0]
    Y = positions[:, 1]
    ax.scatter(X, Y, s=5)
    plt.show()


def plotGalaxyArms2D(nbStars=1000):
    fig = plt.figure(figsize=(10, 10))
    fig.patch.set_facecolor('xkcd:black')  # Changing figure to black
    ax = fig.add_subplot(111)
    ax.set_facecolor('xkcd:black')  # Changing background to black
    G = gravitationalConstant()
    positions, velocities, masses = generateArms2D(nbStars, 5, 1, 0.5, 3, 5, G)
    X = positions[:, 0]
    Y = positions[:, 1]
    ax.scatter(X, Y, s=5)
    plt.show()


plotGalaxyArms2D(1000)
