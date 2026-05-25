import mapboxgl from 'mapbox-gl'
import MapboxWorker from 'mapbox-gl/dist/mapbox-gl-csp-worker?worker'

mapboxgl.workerClass = MapboxWorker
mapboxgl.accessToken = (import.meta.env.VITE_MAPBOX_TOKEN || '').trim()

export default mapboxgl
