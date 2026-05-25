const cache = new Map()

function cloneJson(data) {
  if (typeof structuredClone === 'function') return structuredClone(data)
  return JSON.parse(JSON.stringify(data))
}

async function loadJson(name) {
  return loadGeneratedFile(`${name}.json`)
}

async function loadGeneratedFile(path) {
  if (cache.has(path)) return cache.get(path)
  const promise = fetch(`${import.meta.env.BASE_URL}generated/${path}`)
    .then(async (response) => {
      if (!response.ok) {
        throw new Error(`Failed to load ${path}`)
      }
      const contentType = response.headers.get('content-type') || ''
      if (!contentType.includes('json') && !contentType.includes('geo+json')) {
        throw new Error(`Unexpected response for ${path}: ${contentType || 'unknown content type'}`)
      }
      return response.json()
    })
    .catch((error) => {
      cache.delete(path)
      throw error
    })
  cache.set(path, promise)
  return promise
}

export function getDashboardData() {
  return loadJson('dashboard')
}

export function getRecoveriesData() {
  return loadJson('recoveries')
}

export function getSpeciesRangesIndex() {
  return loadJson('species-ranges-index')
}

export function getSpeciesRange(path) {
  return loadGeneratedFile(path).then((data) => cloneJson(data))
}

export function getMigrationProbabilitiesData() {
  return loadJson('migration-probabilities')
}

export function getPublicationsData() {
  return loadJson('publications')
}
