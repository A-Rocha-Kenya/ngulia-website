import { PathLayer, ScatterplotLayer } from '@deck.gl/layers'

function smoothstep(edge0, edge1, value) {
  const t = Math.max(0, Math.min(1, (value - edge0) / (edge1 - edge0)))
  return t * t * (3 - 2 * t)
}

function interpolate(a, b, t) {
  return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]
}

function cubicPoint(a, b, c, d, t) {
  const mt = 1 - t
  return [
    mt ** 3 * a[0] + 3 * mt ** 2 * t * b[0] + 3 * mt * t ** 2 * c[0] + t ** 3 * d[0],
    mt ** 3 * a[1] + 3 * mt ** 2 * t * b[1] + 3 * mt * t ** 2 * c[1] + t ** 3 * d[1],
  ]
}

function buildSampler(surface, probabilities) {
  const bounds = probabilities.bounds
  const { width, height } = probabilities.grid
  const dx = (bounds.east - bounds.west) / width
  const dy = (bounds.north - bounds.south) / height
  const cdf = []
  let total = 0

  for (const value of surface.values) {
    total += value
    cdf.push(total)
  }

  return () => {
    const target = Math.random() * total
    let low = 0
    let high = cdf.length - 1
    while (low < high) {
      const mid = Math.floor((low + high) / 2)
      if (cdf[mid] < target) low = mid + 1
      else high = mid
    }
    const x = low % width
    const y = Math.floor(low / width)
    return [
      bounds.west + (x + 0.5) * dx,
      bounds.south + (y + 0.5) * dy,
    ]
  }
}

function activeSurfaces(probabilities) {
  return {
    departure: probabilities.departure,
    landing: probabilities.landing,
  }
}

function offsetAlongPerpendicular(a, b, scale) {
  const dx = b[0] - a[0]
  const dy = b[1] - a[1]
  const length = Math.hypot(dx, dy) || 1
  return [(-dy / length) * scale, (dx / length) * scale]
}

function buildTrajectory(origin, destination, site, pull) {
  const sitePull = Math.max(0, Math.min(0.95, pull + (Math.random() - 0.5) * 0.08))
  const firstSwing = (Math.random() - 0.5) * 7.2
  const secondSwing = (Math.random() - 0.5) * 7.2
  const p1 = offsetAlongPerpendicular(origin, destination, firstSwing)
  const p2 = offsetAlongPerpendicular(origin, destination, secondSwing)
  const firstBase = interpolate(origin, destination, 0.32)
  const secondBase = interpolate(origin, destination, 0.68)
  const firstControl = interpolate(firstBase, site, sitePull)
  const secondControl = interpolate(secondBase, site, sitePull)
  const curve = [
    origin,
    [firstControl[0] + p1[0], firstControl[1] + p1[1]],
    [secondControl[0] + p2[0], secondControl[1] + p2[1]],
    destination,
  ]
  const path = []

  for (let i = 0; i <= 58; i += 1) path.push(cubicPoint(...curve, i / 58))
  return path
}

function pointAt(path, progress) {
  const position = Math.max(0, Math.min(path.length - 1.001, progress * (path.length - 1)))
  const index = Math.floor(position)
  return interpolate(path[index], path[index + 1] || path[index], position - index)
}

function makeParticle(id, samplers, probabilities, controls, progress = Math.random()) {
  const site = [probabilities.metadata.site.longitude, probabilities.metadata.site.latitude]
  const origin = samplers.origin()
  const destination = samplers.destination()

  return {
    id,
    path: buildTrajectory(origin, destination, site, controls.pull),
    progress,
    speed: 0.045 + Math.random() * 0.035,
    radius: 9000 + Math.random() * 9000,
  }
}

export function createMigrationParticles(probabilities, controls) {
  const { departure, landing } = activeSurfaces(probabilities)
  const samplers = {
    origin: buildSampler(departure, probabilities),
    destination: buildSampler(landing, probabilities),
  }
  return Array.from({ length: controls.count }, (_, index) => makeParticle(index, samplers, probabilities, controls))
}

export function syncParticleCount(particles, probabilities, controls) {
  if (particles.length > controls.count) return particles.slice(0, controls.count)
  if (particles.length === controls.count) return particles

  const added = createMigrationParticles(probabilities, { ...controls, count: controls.count - particles.length })
  return [...particles, ...added.map((particle, index) => ({ ...particle, id: particles.length + index }))]
}

export function advanceParticles(particles, probabilities, controls, deltaMs) {
  let samplers

  return particles.map((particle) => {
    const progress = particle.progress + particle.speed * controls.speed * (deltaMs / 1000)
    if (progress < 1) return { ...particle, progress }

    if (!samplers) {
      const { departure, landing } = activeSurfaces(probabilities)
      samplers = {
        origin: buildSampler(departure, probabilities),
        destination: buildSampler(landing, probabilities),
      }
    }

    return makeParticle(particle.id, samplers, probabilities, controls, 0)
  })
}

export function migrationDeckLayers(particles, controls) {
  const site = controls.site || [38.211134674309974, -3.0140288001023605]
  const fade = Math.max(0.16, controls.fade)
  const points = particles.map((particle) => {
    const alpha = Math.min(smoothstep(0, fade, particle.progress), 1 - smoothstep(1 - fade, 1, particle.progress))
    return {
      position: pointAt(particle.path, particle.progress),
      radius: particle.radius,
      alpha: Math.max(0, alpha),
    }
  })
  const tails = particles.map((particle) => {
    const start = Math.max(0, particle.progress - controls.trail)
    const steps = 8
    const path = []
    for (let i = 0; i <= steps; i += 1) path.push(pointAt(particle.path, start + (particle.progress - start) * (i / steps)))
    const alpha = Math.min(smoothstep(0, fade, particle.progress), 1 - smoothstep(1 - fade, 1, particle.progress))
    return { path, alpha: Math.max(0, alpha) }
  })

  return [
    new PathLayer({
      id: 'migration-particle-trails',
      data: tails,
      getPath: (item) => item.path,
      getColor: (item) => [255, 217, 120, Math.round(80 * item.alpha)],
      getWidth: 1.35,
      widthUnits: 'pixels',
      jointRounded: true,
      capRounded: true,
      parameters: { depthTest: false },
    }),
    new ScatterplotLayer({
      id: 'migration-particles',
      data: points,
      getPosition: (item) => item.position,
      getRadius: (item) => item.radius,
      getFillColor: (item) => [245, 238, 206, Math.round(210 * item.alpha)],
      radiusUnits: 'meters',
      stroked: false,
      parameters: { depthTest: false },
    }),
    new ScatterplotLayer({
      id: 'ngulia-site-marker-top',
      data: [{ position: site }],
      getPosition: (item) => item.position,
      getRadius: 26000,
      radiusUnits: 'meters',
      getFillColor: [227, 75, 75, 245],
      getLineColor: [255, 255, 255, 245],
      lineWidthUnits: 'pixels',
      getLineWidth: 2.5,
      stroked: true,
      parameters: { depthTest: false },
    }),
  ]
}
