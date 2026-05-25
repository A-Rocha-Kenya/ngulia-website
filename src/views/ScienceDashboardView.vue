<template>
  <section class="page dashboard-page">
    <div class="section-label">Science / Dashboard</div>
    <h1 class="page-title">Dashboard</h1>

    <section class="dashboard-headline panel">
      <div class="panel-inner dashboard-headline__inner">
        <div>
          <p class="dashboard-context">{{ selectedSpecies ? selectedSpecies.name : 'All species' }}</p>
          <div class="dashboard-headline__number">{{ formatNumber(activeTotalBirds) }}</div>
          <div class="dashboard-headline__label">birds ringed</div>
        </div>
        <div class="dashboard-headline__metrics">
          <div v-for="metric in headlineMetrics" :key="metric.label" class="dashboard-headline__metric">
            <strong>{{ metric.value }}</strong>
            <span>{{ metric.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="dashboard-selector panel">
      <div class="panel-inner">
        <h2 class="panel-title">Species selection</h2>
        <div class="dashboard-selector__inner">
          <div class="species-sidebar">
            <label class="species-search">
              <span class="species-search__label">Species</span>
              <Multiselect
                v-model="selectedSpeciesId"
                class="species-multiselect"
                id="species-select"
                :options="speciesOptions"
                :classes="{
                  dropdown: 'multiselect-dropdown species-multiselect-dropdown',
                  options: 'multiselect-options species-multiselect-options',
                  option: 'multiselect-option species-multiselect-option',
                  noOptions: 'multiselect-no-options species-multiselect-empty',
                  noResults: 'multiselect-no-results species-multiselect-empty'
                }"
                value-prop="value"
                label="label"
                track-by="label"
                :searchable="true"
                :can-clear="true"
                :can-deselect="true"
                :close-on-select="true"
                :object="false"
                :max-height="320"
                :append-to-body="true"
                :close-on-scroll="true"
                open-direction="bottom"
                placeholder="Select or search a species"
              />
            </label>

            <div v-if="selectedSpecies" class="selected-species">
              <img v-if="selectedSpecies.photo" :src="selectedSpecies.photo" :alt="selectedSpecies.name" class="selected-species__image" />
              <div>
                <strong>{{ selectedSpecies.name }}</strong>
                <p class="muted"><em>{{ selectedSpecies.latin }}</em></p>
                <div v-if="selectedSpeciesExternalLinks.length" class="selected-species__chips">
                  <a
                    v-for="link in selectedSpeciesExternalLinks"
                    :key="link.key"
                    :href="link.url"
                    class="photo-chip selected-species__link"
                    target="_blank"
                    rel="noreferrer noopener"
                  >
                    {{ link.label }}
                  </a>
                </div>
              </div>
            </div>
          </div>

          <div class="species-treemap-panel">
            <div class="species-treemap-toolbar">
              <span class="species-search__label">Treemap scale</span>
              <div class="species-scale-switch" role="tablist" aria-label="Treemap scale">
                <button
                  type="button"
                  class="species-scale-switch__button"
                  :class="{ 'is-active': treemapScale === 'linear' }"
                  @click="treemapScale = 'linear'"
                >
                  Normal
                </button>
                <button
                  type="button"
                  class="species-scale-switch__button"
                  :class="{ 'is-active': treemapScale === 'log' }"
                  @click="treemapScale = 'log'"
                >
                  Log
                </button>
              </div>
            </div>
            <EChart :option="treemapOption" @chart-click="handleTreemapClick" />
          </div>
        </div>
      </div>
    </section>

    <section v-show="showRecoveriesSection" class="dashboard-grid dashboard-grid--recoveries">
      <article class="panel recovery-map-panel">
        <div class="panel-inner recovery-map-panel__inner">
          <div ref="mapShellRef" class="dashboard-map-shell">
            <div class="dashboard-map__header">
              <div class="dashboard-map__label">Recovery map</div>
              <div class="photo-chip dashboard-map__badge">{{ formatNumber(filteredRecoveries.length) }} rings · {{ formatNumber(filteredLocationsCount) }} locations</div>
            </div>
            <div class="map-controls">
              <button
                class="map-controls__button"
                type="button"
                :aria-label="isMapFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'"
                :title="isMapFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'"
                @click="toggleMapFullscreen"
              >
                <svg v-if="!isMapFullscreen" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />
                </svg>
                <svg v-else viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M9 4H4v5M15 4h5v5M9 20H4v-5M15 20h5v-5" />
                </svg>
                <span class="sr-only">{{ isMapFullscreen ? 'Exit fullscreen' : 'Enter fullscreen' }}</span>
              </button>
              <button
                class="map-controls__button"
                type="button"
                :aria-expanded="showMapSettings ? 'true' : 'false'"
                aria-controls="recovery-map-settings"
                aria-label="Map settings"
                title="Map settings"
                @click="showMapSettings = !showMapSettings"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M10.4 2.6h3.2l.55 2.25c.54.18 1.06.4 1.55.67l1.99-1.2 2.26 2.26-1.2 1.99c.27.49.49 1.01.67 1.55l2.25.55v3.2l-2.25.55c-.18.54-.4 1.06-.67 1.55l1.2 1.99-2.26 2.26-1.99-1.2c-.49.27-1.01.49-1.55.67l-.55 2.25h-3.2l-.55-2.25a8.14 8.14 0 0 1-1.55-.67l-1.99 1.2-2.26-2.26 1.2-1.99a8.14 8.14 0 0 1-.67-1.55L2.6 13.6v-3.2l2.25-.55c.18-.54.4-1.06.67-1.55l-1.2-1.99L6.58 4.05l1.99 1.2c.49-.27 1.01-.49 1.55-.67zM12 8.35A3.65 3.65 0 1 0 12 15.65 3.65 3.65 0 0 0 12 8.35z" />
                </svg>
                <span class="sr-only">Map settings</span>
              </button>
            </div>
            <div
              v-if="showMapSettings"
              id="recovery-map-settings"
              class="recovery-map-settings"
              aria-label="Recovery map settings"
            >
              <label>
                <span>Background</span>
                <select v-model="selectedMapStyle">
                  <option v-for="style in mapStyles" :key="style.value" :value="style.value">{{ style.label }}</option>
                </select>
              </label>
            </div>
            <div class="dashboard-map__legend">
              <span><i class="dashboard-map__swatch dashboard-map__swatch--ringed"></i>Ringed at Ngulia</span>
              <span><i class="dashboard-map__swatch dashboard-map__swatch--controlled"></i>Controlled at Ngulia</span>
              <span><i class="dashboard-map__swatch dashboard-map__swatch--mixed"></i>Mixed site</span>
              <span v-if="selectedSpeciesRangeMeta?.available" class="dashboard-map__legend-divider"></span>
              <span v-if="selectedSpeciesRangeMeta?.available"><i class="dashboard-map__swatch dashboard-map__swatch--wintering"></i>Wintering</span>
              <span v-if="selectedSpeciesRangeMeta?.available"><i class="dashboard-map__swatch dashboard-map__swatch--breeding"></i>Breeding</span>
            </div>
            <div ref="mapRef" class="dashboard-map"></div>
          </div>
        </div>
      </article>

      <article class="panel recovery-table-panel">
        <div class="panel-inner">
          <h2 class="panel-title">Recovery records</h2>
          <input v-model="recoverySearch" class="dashboard-input" placeholder="Search species, country, site, comment, or date" />
          <div ref="recoveryTableWrapRef" class="recovery-table-wrap">
            <table class="recovery-table">
              <thead>
                <tr>
                  <th>Location</th>
                  <th class="recovery-table__date">Ringed</th>
                  <th class="recovery-table__date">Controlled</th>
                  <th v-if="!selectedSpecies">Species</th>
                  <th>Comment</th>
                  <th>Duration</th>
                  <th>Distance</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in filteredRecoveries"
                  :key="item.id"
                  :data-recovery-id="item.id"
                  :class="{
                    'is-hovered': item.id === hoveredRecoveryId,
                    'is-selected': selectedRecoveryIds.has(item.id)
                  }"
                  @mouseenter="highlightRecovery(item)"
                  @mouseleave="clearRecoveryHighlight"
                  @click="focusRecovery(item)"
                >
                  <td>{{ formatLocation(item.recoverSite, item.recoverCountry) }}</td>
                  <td class="recovery-table__date">{{ recoveryTableRingDate(item) || 'n/a' }}</td>
                  <td class="recovery-table__date">{{ recoveryTableRecoverDate(item) || 'n/a' }}</td>
                  <td v-if="!selectedSpecies" class="recovery-table__species">{{ item.speciesName }}</td>
                  <td>{{ item.method || '' }}</td>
                  <td>{{ formatDurationDays(item.durationDays) }}</td>
                  <td>{{ item.distanceKm ? `${formatNumber(item.distanceKm)} km` : 'n/a' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p class="recovery-table__note">* indicates the ringing or control event happened at Ngulia.</p>
        </div>
      </article>
    </section>

    <section class="dashboard-grid dashboard-grid--charts">
      <article class="panel temporal-panel">
        <div class="panel-inner">
          <h2 class="panel-title">Annual totals</h2>
          <EChart :option="annualOption" />
        </div>
      </article>

      <article class="panel temporal-panel">
        <div class="panel-inner">
          <h2 class="panel-title">Seasonal phenology</h2>
          <EChart :option="phenologyOption" />
        </div>
      </article>
    </section>
  </section>
</template>

<script setup>
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import Multiselect from '@vueform/multiselect'
import '@vueform/multiselect/themes/default.css'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import EChart from '../components/EChart.vue'
import { getDashboardData, getRecoveriesData, getSpeciesRange, getSpeciesRangesIndex } from '../lib/generatedData.js'

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN || ''
const NGULIA_COORDS = [38.211134674309974, -3.0140288001023605]
const SPECIES_COLORS = ['#4ea7a0', '#f2c14e', '#c46a3a', '#9c9b4a', '#7093c6', '#ff7d7d', '#8ccf7e', '#cf93ff', '#65d0e8', '#f0a35d']
const EMPTY_FEATURE_COLLECTION = { type: 'FeatureCollection', features: [] }
const EMPTY_RECOVERY_GEOMETRY = {
  points: { type: 'FeatureCollection', features: [] },
  lines: { type: 'FeatureCollection', features: [] }
}
const BREEDING_RANGE_COLOR = '#ff2b8a'
const WINTERING_RANGE_COLOR = '#f7f3e8'
const MIXED_RECOVERY_COLOR = '#f2c14e'
const MIXED_RECOVERY_COLOR_KEY = '__mixed_location__'
const CONTROLLED_POINT_FILL = '#292929'
const MIXED_POINT_STROKE = '#6e7884'
const PHENOLOGY_BAR_THRESHOLD = 12
const PHENOLOGY_MARKER_THRESHOLD = 20
const RECOVERY_POINT_LAYER_IDS = [
  'dashboard-recovery-points-ringed',
  'dashboard-recovery-points-controlled',
  'dashboard-recovery-points-mixed'
]

const dashboard = ref({ summary: {}, yearly: [], topSpecies: [], speciesExplorer: [] })
const recoveriesData = ref({ summary: {}, items: [] })
const speciesRangesIndex = ref({ species: {} })
const selectedSpeciesRange = ref(EMPTY_FEATURE_COLLECTION)
const selectedSpeciesId = ref('')
const recoverySearch = ref('')
const hoveredRecoveryId = ref('')
const hoveredLocationKey = ref('')
const selectedLocationKey = ref('')
const mapRef = ref(null)
const mapShellRef = ref(null)
const recoveryTableWrapRef = ref(null)
const treemapScale = ref('linear')
const selectedMapStyle = ref('mapbox://styles/mapbox/dark-v11')
const showMapSettings = ref(false)
const isMapFullscreen = ref(false)

const mapStyles = [
  { label: 'Dark', value: 'mapbox://styles/mapbox/dark-v11' },
  { label: 'Satellite streets', value: 'mapbox://styles/mapbox/satellite-streets-v12' },
  { label: 'Satellite', value: 'mapbox://styles/mapbox/satellite-v9' },
  { label: 'Outdoors', value: 'mapbox://styles/mapbox/outdoors-v12' },
  { label: 'Light', value: 'mapbox://styles/mapbox/light-v11' }
]

let map
let popup
let resizeObserver
let interactionsBound = false
let rangeRequestId = 0

const summary = computed(() => dashboard.value.summary || {})
const speciesOptions = computed(() =>
  dashboard.value.speciesExplorer.map((species) => ({
    value: species.id,
    label: species.name
  }))
)
const selectedSpecies = computed(() =>
  dashboard.value.speciesExplorer.find((species) => species.id === selectedSpeciesId.value)
)
const selectedSpeciesExternalLinks = computed(() => {
  const links = selectedSpecies.value?.links || {}
  return [
    links.birdsOfTheWorld ? { key: 'botw', label: 'Birds of the World', url: links.birdsOfTheWorld } : null,
    links.eBird ? { key: 'ebird', label: 'eBird', url: links.eBird } : null,
    links.birdLifeFactsheet ? { key: 'birdlife', label: 'BirdLife factsheet', url: links.birdLifeFactsheet } : null,
    links.kenyaBirdTrends ? { key: 'kbt', label: 'Kenya Bird Trends', url: links.kenyaBirdTrends } : null,
    links.avibase ? { key: 'avibase', label: 'Avibase', url: links.avibase } : null,
    ...((links.kbm || []).map((entry) => ({ key: `kbm-${entry.id}`, label: `KBM ${entry.id}`, url: entry.url }))),
    ...((links.safring || []).map((entry) => ({ key: `safring-${entry.id}`, label: `SAFRING ${entry.id}`, url: entry.url })))
  ].filter(Boolean)
})
const selectedSpeciesRangeMeta = computed(() =>
  selectedSpecies.value ? speciesRangesIndex.value.species?.[selectedSpecies.value.id] || null : null
)
const selectedRecoveryCount = computed(() => speciesRecoveries.value.length)
const showRecoveriesSection = computed(() => !selectedSpecies.value || selectedRecoveryCount.value > 0)
const activeTotalBirds = computed(() => selectedSpecies.value?.total || summary.value.totalBirds || 0)

const speciesRecoveries = computed(() => {
  if (!selectedSpecies.value) return recoveriesData.value.items
  return recoveriesData.value.items.filter((item) => item.speciesId === selectedSpecies.value.id)
})
const filteredRecoveries = computed(() => {
  const query = recoverySearch.value.trim().toLowerCase()
  if (!query) return speciesRecoveries.value
  return speciesRecoveries.value.filter((item) =>
    [
      item.speciesName,
      item.speciesLatin,
      item.recoverCountry,
      item.recoverSite,
      item.recoverProvince,
      item.method,
      item.ringDate,
      item.recoverDate
    ]
      .filter(Boolean)
      .join(' ')
      .toLowerCase()
      .includes(query)
  )
})
const filteredCountriesCount = computed(
  () => new Set(filteredRecoveries.value.map((item) => item.recoverCountry).filter(Boolean)).size
)
const groupedRecoveries = computed(() => {
  const groups = new Map()
  for (const item of filteredRecoveries.value) {
    const key = locationKeyForItem(item)
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key).push(item)
  }
  return groups
})
const filteredLocationsCount = computed(() => groupedRecoveries.value.size)
const selectedRecoveryIds = computed(() => new Set((groupedRecoveries.value.get(selectedLocationKey.value) || []).map((item) => item.id)))
const headlineMetrics = computed(() => [
  { label: selectedSpecies.value ? 'recoveries for selected species' : 'recoveries', value: formatNumber(filteredRecoveries.value.length) },
  { label: 'recovery countries', value: formatNumber(filteredCountriesCount.value) },
  { label: 'species in dataset', value: formatNumber(summary.value.totalSpecies) },
  { label: 'year span', value: summary.value.yearStart && summary.value.yearEnd ? `${summary.value.yearStart}-${summary.value.yearEnd}` : '...' }
])
const annualYears = computed(() => dashboard.value.yearly.map((row) => row.year))
const annualTotals = computed(() => dashboard.value.yearly.map((row) => row.totalRings))
const annualSelectedData = computed(() => {
  if (!selectedSpecies.value) return annualTotals.value
  const counts = new Map(selectedSpecies.value.annual.map((row) => [row.year, row.count]))
  return annualYears.value.map((year) => counts.get(year) || 0)
})
const annualChartTotals = computed(() => annualTotals.value.map((value) => toAnnualScaleValue(value)))
const annualChartSelected = computed(() => annualSelectedData.value.map((value) => toAnnualScaleValue(value)))
const annualRatioData = computed(() =>
  annualSelectedData.value.map((value, index) => {
    const total = annualTotals.value[index] || 0
    return total ? (value / total) * 100 : 0
  })
)
const annualAverageRatio = computed(() => {
  if (!selectedSpecies.value) return null
  const ratios = annualRatioData.value.filter((value, index) => (annualTotals.value[index] || 0) > 0)
  if (!ratios.length) return null
  return ratios.reduce((sum, value) => sum + value, 0) / ratios.length
})
const annualAverageCount = computed(() => {
  if (!selectedSpecies.value) return null
  const counts = annualSelectedData.value.filter((_, index) => (annualTotals.value[index] || 0) > 0)
  if (!counts.length) return null
  return counts.reduce((sum, value) => sum + value, 0) / counts.length
})
const annualMaxCount = computed(() => Math.max(...annualTotals.value, ...annualSelectedData.value, 0))
const annualAxisTicks = computed(() => buildAnnualAxisTicks(annualMaxCount.value))
const annualAxisMax = computed(() => annualAxisTicks.value.at(-1)?.position ?? 1)
const activePhenologyRows = computed(() => selectedSpecies.value?.phenology || dashboard.value.phenology || [])
const phenologySeasonData = computed(() => toSeasonSeries(activePhenologyRows.value))
const phenologyEffortData = computed(() => toSeasonSeries(dashboard.value.phenology || []))
const phenologyTotalCount = computed(() => phenologySeasonData.value.reduce((sum, row) => sum + (row.count || 0), 0))
const usePhenologyBars = computed(() => selectedSpecies.value && phenologyTotalCount.value < PHENOLOGY_BAR_THRESHOLD)
const smoothedPhenologyData = computed(() => smoothSeries(phenologySeasonData.value, 'count', 7))
const phenologyMarkers = computed(() =>
  buildPhenologyMarkers(phenologySeasonData.value, {
    minTotalCount: PHENOLOGY_MARKER_THRESHOLD,
    disabled: usePhenologyBars.value
  })
)

const chartBase = {
  backgroundColor: 'transparent',
  textStyle: { color: '#f3efe6', fontFamily: 'Avenir Next, Avenir, Segoe UI, sans-serif' },
  tooltip: {
    trigger: 'item',
    backgroundColor: 'rgba(12, 18, 28, 0.96)',
    borderColor: 'rgba(243, 239, 230, 0.12)',
    textStyle: { color: '#f3efe6' }
  }
}

const treemapColorMap = computed(() =>
  Object.fromEntries(
    dashboard.value.speciesExplorer.map((species, index) => [species.id, dimColor(SPECIES_COLORS[index % SPECIES_COLORS.length], 0.58)])
  )
)
const speciesColorMap = computed(() =>
  Object.fromEntries(dashboard.value.speciesExplorer.map((species, index) => [species.id, SPECIES_COLORS[index % SPECIES_COLORS.length]]))
)
const activeChartColor = computed(() => (selectedSpecies.value ? speciesColorMap.value[selectedSpecies.value.id] || '#f2c14e' : '#f2c14e'))
const activeChartColorSoft = computed(() => dimColor(activeChartColor.value, 0.18))
const activeChartColorStrong = computed(() => dimColor(activeChartColor.value, 0.82))
const activeChartColorText = computed(() => dimColor(activeChartColor.value, 0.92))
const activeChartColorMid = computed(() => dimColor(activeChartColor.value, 0.72))

const treemapOption = computed(() => ({
  ...chartBase,
  grid: {
    top: 2,
    right: 2,
    bottom: 2,
    left: 2
  },
  tooltip: {
    ...chartBase.tooltip,
    formatter(params) {
      const data = params.data
      return `<strong>${data.name}</strong><br/>${new Intl.NumberFormat('en-US').format(data.rawTotal)} birds ringed`
    }
  },
  series: [
    {
      type: 'treemap',
      top: 0,
      right: 0,
      bottom: 0,
      left: 0,
      roam: false,
      nodeClick: false,
      breadcrumb: { show: false },
      label: {
        show: true,
        formatter(info) {
          return info.name
        },
        color: '#f3efe6',
        fontSize: 12,
        lineHeight: 14
      },
      upperLabel: { show: false },
      itemStyle: {
        gapWidth: 2,
        borderColor: 'rgba(243,239,230,0.18)',
        borderWidth: 1
      },
      levels: [
        {
          itemStyle: {
            borderRadius: 4,
            gapWidth: 2
          }
        }
      ],
      color: Object.values(treemapColorMap.value),
      data: dashboard.value.topSpecies.map((species) => ({
        id: species.id,
        name: species.name,
        value: treemapScale.value === 'log' ? Math.log10(species.total + 1) : species.total,
        rawTotal: species.total,
        itemStyle: {
          color: treemapColorMap.value[species.id],
          borderColor: species.id === selectedSpeciesId.value ? 'rgba(255,255,255,0.72)' : 'rgba(243,239,230,0.12)',
          borderWidth: species.id === selectedSpeciesId.value ? 2.4 : 0.8
        }
      }))
    }
  ]
}))

const annualOption = computed(() => ({
  ...chartBase,
  tooltip: {
    ...chartBase.tooltip,
    trigger: 'axis',
    formatter(params) {
      const rows = (Array.isArray(params) ? params : [params]).filter(Boolean)
      const lines = rows
        .map((item) => {
          const rawValue = item.data?.rawValue ?? fromAnnualScaleValue(item.value)
          if (item.seriesName === 'Total annual rings') return `${item.marker}${item.seriesName}: ${formatNumber(rawValue)} total rings`
          if (item.seriesName === 'Annual ratio') return `${item.marker}Ratio: ${item.value.toFixed(1)}% of annual total`
          return `${item.marker}${item.seriesName}: ${formatNumber(rawValue)} birds ringed`
        })
        .join('<br/>')
      const yearIndex = annualYears.value.findIndex((year) => String(year) === String(rows[0]?.axisValueLabel || rows[0]?.name))
      const ratio = selectedSpecies.value && yearIndex >= 0 ? annualRatioData.value[yearIndex] : null
      const ratioLine = ratio != null ? `<br/>Share of annual total: ${ratio.toFixed(1)}%` : ''
      return `<strong>${rows[0]?.axisValueLabel || rows[0]?.name || ''}</strong><br/>${lines}${ratioLine}`
    }
  },
  grid: { top: 24, right: 24, bottom: 42, left: 58 },
  xAxis: {
    type: 'category',
    data: annualYears.value,
    axisLabel: { color: '#a8b3c2', hideOverlap: true },
    axisLine: { lineStyle: { color: 'rgba(243,239,230,0.16)' } },
    splitLine: { show: false }
  },
  yAxis: {
    type: 'value',
    name: 'Birds ringed',
    nameLocation: 'middle',
    nameGap: 38,
    nameTextStyle: { color: activeChartColorText.value, fontWeight: 700 },
    min: 0,
    max: annualAxisMax.value,
    interval: 1,
    axisTick: { show: false },
    axisLabel: {
      color: '#a8b3c2',
      formatter(value) {
        return formatAnnualAxisLabel(value, annualAxisTicks.value)
      }
    },
    splitLine: { lineStyle: { color: 'rgba(243,239,230,0.08)' } }
  },
  series: [
    {
      name: 'Total annual rings',
      type: 'bar',
      barGap: '-100%',
      barCategoryGap: '28%',
      silent: true,
      itemStyle: { color: 'rgba(243, 239, 230, 0.12)', borderRadius: [6, 6, 0, 0] },
      emphasis: { disabled: true },
      data: annualTotals.value.map((value) => ({ value: toAnnualScaleValue(value), rawValue: value || 0 }))
    },
    {
      name: selectedSpecies.value ? selectedSpecies.value.name : 'Total annual rings',
      type: 'bar',
      barGap: '-100%',
      barCategoryGap: '28%',
      itemStyle: {
        color: activeChartColorStrong.value,
        borderRadius: [6, 6, 0, 0]
      },
      data: (selectedSpecies.value ? annualSelectedData.value : annualTotals.value).map((value) => ({
        value: toAnnualScaleValue(value),
        rawValue: value || 0
      })),
      markLine: selectedSpecies.value && annualAverageCount.value != null && annualAverageCount.value > 1 && annualAverageRatio.value != null
        ? {
            symbol: 'none',
            animation: false,
            silent: true,
            label: {
              show: true,
              position: 'insideEndTop',
              color: '#f3efe6',
              fontWeight: 700,
              formatter: `Average ${formatNumber(Math.round(annualAverageCount.value))} rings (${annualAverageRatio.value.toFixed(1)}%)`
            },
            lineStyle: {
              color: 'rgba(243, 239, 230, 0.82)',
              type: 'dotted',
              width: 1.4
            },
            data: [{ yAxis: toAnnualScaleValue(annualAverageCount.value) }]
          }
        : undefined
    }
  ]
}))

const phenologyOption = computed(() => ({
  ...chartBase,
  tooltip: {
    ...chartBase.tooltip,
    trigger: 'axis',
    axisPointer: { type: 'none' },
    formatter(params) {
      const rows = (Array.isArray(params) ? params : [params]).filter(Boolean)
      const point = phenologySeasonData.value.find((row) => row.seasonDay === rows[0]?.value?.[0])
      const effort = phenologyEffortData.value.find((row) => row.seasonDay === rows[0]?.value?.[0])
      const dateLabel = point?.seasonDay ? formatSeasonTick(point.seasonDay) : formatSeasonTick(rows[0]?.value?.[0])
      const lines = rows
        .map((item) => {
          if (item.seriesName === 'Ringing effort') {
            return `${item.marker}${item.seriesName}: ${formatNumber(item.value[1])} years with ringing`
          }
          return `${item.marker}${item.seriesName}: ${formatNumber(Math.round(item.value[1]))} birds ringed`
        })
        .join('<br/>')
      const extra = effort && !rows.some((item) => item.seriesName === 'Ringing effort')
        ? `<br/>Ringing effort: ${formatNumber(effort.effortYears)} years with ringing`
        : ''
      return `<strong>${dateLabel}</strong><br/>${lines}${extra}`
    }
  },
  grid: { top: 24, right: 42, bottom: 42, left: 58 },
  xAxis: {
    type: 'value',
    min: 295,
    max: 369,
    interval: 15,
    axisLabel: {
      color: '#a8b3c2',
      formatter(value) {
        return formatSeasonTick(value)
      }
    },
    splitLine: { show: false },
    axisLine: { lineStyle: { color: 'rgba(243,239,230,0.16)' } }
  },
  yAxis: [
    {
      type: 'value',
      name: 'Birds ringed',
      nameLocation: 'middle',
      nameGap: 38,
      nameTextStyle: { color: activeChartColorText.value, fontWeight: 700 },
      axisLabel: {
        color: activeChartColorText.value,
        formatter(value) {
          return value >= 1000 ? `${Math.round(value / 1000)}k` : value
        }
      },
      splitLine: { lineStyle: { color: 'rgba(243,239,230,0.08)' } }
    },
    {
      type: 'value',
      position: 'right',
      name: 'Years with ringing',
      nameLocation: 'middle',
      nameGap: 48,
      nameTextStyle: { color: 'rgba(243, 239, 230, 0.56)', fontWeight: 700 },
      minInterval: 1,
      axisLabel: {
        color: 'rgba(243, 239, 230, 0.56)'
      },
      splitLine: { show: false }
    }
  ],
  series: [
    {
      name: 'Ringing effort',
      type: 'bar',
      yAxisIndex: 1,
      silent: true,
      barWidth: 6,
      itemStyle: { color: 'rgba(243, 239, 230, 0.12)', borderRadius: [4, 4, 0, 0] },
      emphasis: { disabled: true },
      data: phenologyEffortData.value.map((row) => [row.seasonDay, row.effortYears])
    },
    {
      name: selectedSpecies.value ? selectedSpecies.value.name : 'Total phenology',
      type: usePhenologyBars.value ? 'bar' : 'line',
      smooth: usePhenologyBars.value ? false : 0.35,
      symbol: 'none',
      barWidth: usePhenologyBars.value ? 8 : undefined,
      itemStyle: usePhenologyBars.value
        ? { color: activeChartColorStrong.value, borderRadius: [4, 4, 0, 0] }
        : undefined,
      lineStyle: usePhenologyBars.value ? undefined : { color: activeChartColor.value, width: 3 },
      areaStyle: usePhenologyBars.value ? undefined : { color: activeChartColorSoft.value },
      data: usePhenologyBars.value
        ? phenologySeasonData.value.map((row) => [row.seasonDay, row.count || 0])
        : smoothedPhenologyData.value.map((row) => [row.seasonDay, row.smoothedCount]),
      markLine: phenologyMarkers.value.length
        ? {
            symbol: 'none',
            animation: false,
            label: {
              show: true,
              position: 'insideEndTop',
              distance: 8,
              color: '#f3efe6',
              fontSize: 11,
              formatter(params) {
                return params.data?.labelText || ''
              }
            },
            lineStyle: {
              width: 1.2,
              type: 'dashed'
            },
            data: phenologyMarkers.value
          }
        : undefined
    }
  ]
}))

function formatNumber(value) {
  return new Intl.NumberFormat('en-US').format(value || 0)
}

function updateMapFullscreenState() {
  isMapFullscreen.value = !!document.fullscreenElement && document.fullscreenElement === mapShellRef.value
  window.setTimeout(() => map?.resize(), 0)
}

async function toggleMapFullscreen() {
  const container = mapShellRef.value
  if (!container) return
  if (document.fullscreenElement === container) {
    await document.exitFullscreen()
    return
  }
  await container.requestFullscreen()
}

function formatLocation(site, country) {
  if (site && country) return `${site}, ${country}`
  return site || country || 'n/a'
}

function formatDurationDays(value) {
  const totalDays = Math.round(Number(value || 0))
  if (totalDays <= 0) return ''
  const years = Math.floor(totalDays / 365)
  const days = totalDays % 365
  if (years && days) return `${years}y ${days}d`
  if (years) return `${years}y`
  return `${days}d`
}

function recoveryTableRingDate(item) {
  return item.status === 'ringed' && item.ringDate ? `${item.ringDate}*` : item.ringDate || ''
}

function recoveryTableRecoverDate(item) {
  return item.status === 'controlled' && item.recoverDate ? `${item.recoverDate}*` : item.recoverDate || ''
}

function recoveryLocationStatus(items) {
  const statuses = [...new Set(items.map((item) => item.status).filter(Boolean))]
  if (statuses.length <= 1) return statuses[0] || 'ringed'
  return 'mixed'
}

function recoveryLocationColorKey(items, fallbackSpeciesId = '') {
  const speciesIds = [...new Set(items.map((item) => item.speciesId).filter(Boolean))]
  if (speciesIds.length <= 1) return speciesIds[0] || fallbackSpeciesId
  return MIXED_RECOVERY_COLOR_KEY
}

function recoveryPointRadiusExpression(kind = 'default', status = 'ringed') {
  const stops = kind === 'highlight'
    ? [1, 7.2, 2, 9.8, 4, 12.2, 8, 15.4]
    : [1, 4.8, 2, 7.2, 4, 9.4, 8, 12.5]
  const base = ['interpolate', ['linear'], ['get', 'recoveriesCount'], ...stops]
  const offset = kind === 'highlight'
    ? { ringed: 0, controlled: -0.6, mixed: -0.45 }[status] ?? 0
    : { ringed: 0, controlled: -0.5, mixed: -0.4 }[status] ?? 0
  return offset ? ['+', base, offset] : base
}

function dimColor(hex, alpha = 0.6) {
  const value = hex.replace('#', '')
  const normalized = value.length === 3 ? value.split('').map((char) => char + char).join('') : value
  const red = Number.parseInt(normalized.slice(0, 2), 16)
  const green = Number.parseInt(normalized.slice(2, 4), 16)
  const blue = Number.parseInt(normalized.slice(4, 6), 16)
  return `rgba(${red}, ${green}, ${blue}, ${alpha})`
}

function toSeasonSeries(rows) {
  return rows
    .map((row) => ({
      ...row,
      seasonDay: row.dayOfYear < 120 ? row.dayOfYear + 365 : row.dayOfYear
    }))
    .sort((a, b) => a.seasonDay - b.seasonDay)
}

function toAnnualScaleValue(value) {
  const numericValue = Number(value || 0)
  if (numericValue <= 0) return 0
  return 1 + Math.log10(numericValue)
}

function fromAnnualScaleValue(value) {
  const numericValue = Number(value || 0)
  if (numericValue <= 0) return 0
  return Math.max(1, Math.round(10 ** (numericValue - 1)))
}

function buildAnnualAxisTicks(maxCount) {
  const maxExponent = Math.max(0, Math.ceil(Math.log10(Math.max(maxCount, 1))))
  const ticks = [{ rawValue: 0, position: 0 }]
  for (let exponent = 0; exponent <= maxExponent; exponent += 1) {
    const rawValue = 10 ** exponent
    ticks.push({ rawValue, position: exponent + 1 })
  }
  return ticks
}

function formatAnnualAxisLabel(value, ticks) {
  const match = ticks.find((tick) => Math.abs(tick.position - value) < 0.001)
  if (!match) return ''
  if (match.rawValue === 0) return '0'
  if (match.rawValue >= 1000) return `${Math.round(match.rawValue / 1000)}k`
  return String(match.rawValue)
}

function smoothSeries(rows, key, windowSize = 7) {
  const halfWindow = Math.floor(windowSize / 2)
  return rows.map((row, index) => {
    const start = Math.max(0, index - halfWindow)
    const end = Math.min(rows.length - 1, index + halfWindow)
    const subset = rows.slice(start, end + 1)
    const total = subset.reduce((sum, item) => sum + (item[key] || 0), 0)
    return { ...row, smoothedCount: total / subset.length }
  })
}

function seasonDayToMonthDay(seasonDay) {
  const dayOfYear = seasonDay > 365 ? seasonDay - 365 : seasonDay
  const date = new Date(Date.UTC(2021, 0, 1))
  date.setUTCDate(dayOfYear)
  return {
    day: date.getUTCDate(),
    monthShort: date.toLocaleString('en-US', { month: 'short', timeZone: 'UTC' })
  }
}

function formatSeasonTick(seasonDay) {
  const { day, monthShort } = seasonDayToMonthDay(seasonDay)
  return `${day} ${monthShort}`
}

function weightedSeasonQuantile(rows, quantile) {
  const total = rows.reduce((sum, row) => sum + (row.count || 0), 0)
  if (!total) return null
  const target = total * quantile
  let cumulative = 0
  for (const row of rows) {
    cumulative += row.count || 0
    if (cumulative >= target) return row.seasonDay
  }
  return rows.at(-1)?.seasonDay ?? null
}

function buildPhenologyMarkers(rows, { minTotalCount = 0, disabled = false } = {}) {
  const total = rows.reduce((sum, row) => sum + (row.count || 0), 0)
  if (disabled || total < minTotalCount) return []
  const markerDefs = [
    { key: '10%', quantile: 0.1, color: 'rgba(243, 239, 230, 0.28)' },
    { key: 'Median', quantile: 0.5, color: 'rgba(242, 193, 78, 0.7)' },
    { key: '90%', quantile: 0.9, color: 'rgba(243, 239, 230, 0.28)' }
  ]

  return markerDefs
    .map((marker) => {
      const seasonDay = weightedSeasonQuantile(rows, marker.quantile)
      if (!seasonDay) return null
      return {
        name: marker.key,
        xAxis: seasonDay,
        labelText: `${marker.key} ${formatSeasonTick(seasonDay)}`,
        lineStyle: { color: marker.color }
      }
    })
    .filter(Boolean)
}

function selectSpecies(id) {
  if (!id) {
    selectedSpeciesId.value = ''
    return
  }
  const match = dashboard.value.speciesExplorer.find((species) => species.id === id)
  if (!match) return
  selectedSpeciesId.value = match.id
}

function handleTreemapClick(params) {
  if (params?.data?.id) selectSpecies(params.data.id)
}

function toMatchExpression(defaultColor = '#ffd978', property = 'speciesId') {
  const entries = Object.entries(speciesColorMap.value).flatMap(([id, color]) => [id, color])
  return ['match', ['get', property], MIXED_RECOVERY_COLOR_KEY, MIXED_RECOVERY_COLOR, ...entries, defaultColor]
}

function locationKeyFromCoordinates(longitude, latitude) {
  return `${Number(longitude).toFixed(5)}|${Number(latitude).toFixed(5)}`
}

function locationKeyForItem(item) {
  return locationKeyFromCoordinates(item.longitude, item.latitude)
}

function getActiveLocationKey() {
  return hoveredLocationKey.value || selectedLocationKey.value
}

function popupLocationTitle(item) {
  return [item.recoverCountry || null, item.recoverProvince || null, item.recoverSite || null].filter(Boolean).join(', ')
}

function recoveryDateLabel(item) {
  const duration = formatDurationDays(item.durationDays)
  const parts = []
  if (item.status === 'controlled') {
    const start = item.ringDate || ''
    const end = recoveryTableRecoverDate(item) || ''
    if (start && end) parts.push(`${start} &rarr; ${end}`)
    else if (start || end) parts.push(start || end)
  } else {
    const start = recoveryTableRingDate(item) || ''
    const end = item.recoverDate || ''
    if (start && end) parts.push(`${start} &rarr; ${end}`)
    else if (start || end) parts.push(start || end)
  }
  if (duration) parts.push(duration)
  if (item.method) parts.push(item.method)
  return parts.join(' &middot; ')
}

function recoveryPopupHtml(items) {
  if (!items.length) return ''
  const first = items[0]
  const siteLabel = popupLocationTitle(first) || 'n/a'
  const distanceValues = items.map((item) => item.distanceKm).filter(Boolean)
  const distanceText = distanceValues.length
    ? `${formatNumber(Math.round(distanceValues.reduce((sum, value) => sum + value, 0) / distanceValues.length))} km`
    : ''
  const groupedItems = Array.from(
    items.slice(0, 7).reduce((groups, item) => {
      const key = item.speciesName || 'Unknown species'
      if (!groups.has(key)) groups.set(key, [])
      groups.get(key).push(item)
      return groups
    }, new Map())
  )
  const groupsHtml = groupedItems
    .map(([speciesName, speciesItems]) => {
      const rows = speciesItems
        .map((item) => {
          const dates = recoveryDateLabel(item)
          return `<li>${dates ? `<div class="map-popup__item-sub">${dates}</div>` : ''}</li>`
        })
        .join('')
      return `
        <section class="map-popup__group">
          <div class="map-popup__species">${speciesName}</div>
          <ul class="map-popup__bullets">${rows}</ul>
        </section>
      `
    })
    .join('')
  const moreCount = items.length - 7
  const meta = [`${items.length} recover${items.length > 1 ? 'ies' : 'y'}`, distanceText].filter(Boolean).join(' · ')
  return `
    <div class="map-popup">
      <div class="map-popup__site">${siteLabel}</div>
      <div class="map-popup__meta">${meta}</div>
      <div class="map-popup__list">${groupsHtml}${moreCount > 0 ? `<div class="map-popup__more">+${moreCount} more</div>` : ''}</div>
    </div>
  `
}

function buildGeoJson(items) {
  return {
    ngulia: {
      type: 'FeatureCollection',
      features: [
        {
          type: 'Feature',
          properties: { name: 'Ngulia' },
          geometry: { type: 'Point', coordinates: NGULIA_COORDS }
        }
      ]
    },
    points: {
      type: 'FeatureCollection',
      features: Array.from(new Map(items.map((item) => [locationKeyForItem(item), item])).values()).map((item) => {
        const locationKey = locationKeyForItem(item)
        const locationItems = groupedRecoveries.value.get(locationKey) || []
        const colorKey = recoveryLocationColorKey(locationItems, item.speciesId)
        return {
          type: 'Feature',
          id: locationKey,
          properties: {
            locationKey,
            recoveriesCount: locationItems.length,
            locationStatus: recoveryLocationStatus(locationItems),
            colorKey,
            speciesId: item.speciesId,
            speciesName: item.speciesName
          },
          geometry: { type: 'Point', coordinates: [item.longitude, item.latitude] }
        }
      })
    },
    lines: {
      type: 'FeatureCollection',
      features: items.map((item) => {
        const locationItems = groupedRecoveries.value.get(locationKeyForItem(item)) || [item]
        return {
          type: 'Feature',
          id: item.id,
          properties: { ...item, colorKey: recoveryLocationColorKey(locationItems, item.speciesId) },
          geometry: { type: 'LineString', coordinates: [NGULIA_COORDS, [item.longitude, item.latitude]] }
        }
      })
    }
  }
}

function setSourceData(name, data) {
  const source = map?.getSource(name)
  if (source) source.setData(data)
}

function cloneGeoJson(data) {
  return JSON.parse(JSON.stringify(data))
}

function updateSpeciesRangeData() {
  if (!map?.getSource('dashboard-species-ranges')) return
  setSourceData('dashboard-species-ranges', EMPTY_FEATURE_COLLECTION)
  setSourceData('dashboard-species-ranges', cloneGeoJson(selectedSpeciesRange.value))
  map.triggerRepaint()
}

function updateMapData() {
  if (!map?.getSource('dashboard-recovery-lines') || !map?.getSource('dashboard-recovery-points')) return
  const data = buildGeoJson(filteredRecoveries.value)
  updateSpeciesRangeData()
  setSourceData('dashboard-recovery-lines', EMPTY_RECOVERY_GEOMETRY.lines)
  setSourceData('dashboard-recovery-points', EMPTY_RECOVERY_GEOMETRY.points)
  setSourceData('dashboard-recovery-lines', data.lines)
  setSourceData('dashboard-recovery-points', data.points)

  if (map.getLayer('dashboard-recovery-lines')) {
    map.setPaintProperty('dashboard-recovery-lines', 'line-color', toMatchExpression('#f2c14e', 'colorKey'))
  }
  if (map.getLayer('dashboard-highlight-lines')) {
    map.setPaintProperty('dashboard-highlight-lines', 'line-color', toMatchExpression('#f2c14e', 'colorKey'))
  }
  for (const layerId of ['dashboard-recovery-points-ringed', 'dashboard-recovery-points-controlled', 'dashboard-recovery-points-mixed']) {
    if (map.getLayer(layerId)) {
      map.setPaintProperty(
        layerId,
        'circle-color',
        layerId === 'dashboard-recovery-points-controlled' ? CONTROLLED_POINT_FILL : toMatchExpression('#ffd978', 'colorKey')
      )
      map.setPaintProperty(
        layerId,
        'circle-stroke-color',
        layerId === 'dashboard-recovery-points-ringed'
          ? '#0b0f14'
          : layerId === 'dashboard-recovery-points-controlled'
            ? toMatchExpression('#ffd978', 'colorKey')
            : MIXED_POINT_STROKE
      )
    }
  }
  for (const layerId of ['dashboard-highlight-points-ringed', 'dashboard-highlight-points-controlled', 'dashboard-highlight-points-mixed']) {
    if (map.getLayer(layerId)) {
      map.setPaintProperty(
        layerId,
        'circle-color',
        layerId === 'dashboard-highlight-points-controlled' ? CONTROLLED_POINT_FILL : toMatchExpression('#ffd978', 'colorKey')
      )
      map.setPaintProperty(
        layerId,
        'circle-stroke-color',
        layerId === 'dashboard-highlight-points-ringed'
          ? '#0b0f14'
          : layerId === 'dashboard-highlight-points-controlled'
            ? toMatchExpression('#ffd978', 'colorKey')
            : MIXED_POINT_STROKE
      )
    }
  }
  map.triggerRepaint()
  syncActiveLocationState()
}

function addMapLayers() {
  const data = buildGeoJson(filteredRecoveries.value)

  map.addSource('dashboard-species-ranges', { type: 'geojson', data: selectedSpeciesRange.value })
  map.addSource('dashboard-recovery-lines', { type: 'geojson', data: data.lines })
  map.addSource('dashboard-recovery-points', { type: 'geojson', data: data.points })
  map.addSource('dashboard-highlight-lines', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } })
  map.addSource('dashboard-highlight-points', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } })
  map.addSource('dashboard-ngulia-point', { type: 'geojson', data: data.ngulia })

  map.addLayer({
    id: 'dashboard-species-range-wintering-fill',
    type: 'fill',
    source: 'dashboard-species-ranges',
    filter: ['==', ['get', 'rangeType'], 'wintering'],
    paint: { 'fill-color': WINTERING_RANGE_COLOR, 'fill-opacity': 0.11 }
  })

  map.addLayer({
    id: 'dashboard-species-range-breeding-fill',
    type: 'fill',
    source: 'dashboard-species-ranges',
    filter: ['==', ['get', 'rangeType'], 'breeding'],
    paint: { 'fill-color': BREEDING_RANGE_COLOR, 'fill-opacity': 0.11 }
  })

  map.addLayer({
    id: 'dashboard-species-range-wintering-line',
    type: 'line',
    source: 'dashboard-species-ranges',
    filter: ['==', ['get', 'rangeType'], 'wintering'],
    paint: { 'line-color': WINTERING_RANGE_COLOR, 'line-opacity': 0.24, 'line-width': 0.8 }
  })

  map.addLayer({
    id: 'dashboard-species-range-breeding-line',
    type: 'line',
    source: 'dashboard-species-ranges',
    filter: ['==', ['get', 'rangeType'], 'breeding'],
    paint: { 'line-color': BREEDING_RANGE_COLOR, 'line-opacity': 0.24, 'line-width': 0.8 }
  })

  map.addLayer({
    id: 'dashboard-recovery-lines',
    type: 'line',
    source: 'dashboard-recovery-lines',
    paint: { 'line-color': toMatchExpression('#f2c14e', 'colorKey'), 'line-opacity': 0.34, 'line-width': 1.35 }
  })

  map.addLayer({
    id: 'dashboard-highlight-lines',
    type: 'line',
    source: 'dashboard-highlight-lines',
    paint: { 'line-color': toMatchExpression('#f2c14e', 'colorKey'), 'line-opacity': 0.88, 'line-width': 3.1 }
  })

  map.addLayer({
    id: 'dashboard-recovery-points-ringed',
    type: 'circle',
    source: 'dashboard-recovery-points',
    filter: ['==', ['get', 'locationStatus'], 'ringed'],
    paint: {
      'circle-radius': recoveryPointRadiusExpression('default', 'ringed'),
      'circle-color': toMatchExpression('#ffd978', 'colorKey'),
      'circle-stroke-width': 1.2,
      'circle-stroke-color': '#0b0f14',
      'circle-opacity': 0.9
    }
  })

  map.addLayer({
    id: 'dashboard-recovery-points-controlled',
    type: 'circle',
    source: 'dashboard-recovery-points',
    filter: ['==', ['get', 'locationStatus'], 'controlled'],
    paint: {
      'circle-radius': recoveryPointRadiusExpression('default', 'controlled'),
      'circle-color': CONTROLLED_POINT_FILL,
      'circle-stroke-width': 2.2,
      'circle-stroke-color': toMatchExpression('#ffd978', 'colorKey'),
      'circle-opacity': 0.96
    }
  })

  map.addLayer({
    id: 'dashboard-recovery-points-mixed',
    type: 'circle',
    source: 'dashboard-recovery-points',
    filter: ['==', ['get', 'locationStatus'], 'mixed'],
    paint: {
      'circle-radius': recoveryPointRadiusExpression('default', 'mixed'),
      'circle-color': toMatchExpression('#ffd978', 'colorKey'),
      'circle-stroke-width': 2,
      'circle-stroke-color': MIXED_POINT_STROKE,
      'circle-opacity': 0.88
    }
  })

  map.addLayer({
    id: 'dashboard-highlight-points-ringed',
    type: 'circle',
    source: 'dashboard-highlight-points',
    filter: ['==', ['get', 'locationStatus'], 'ringed'],
    paint: {
      'circle-radius': recoveryPointRadiusExpression('highlight', 'ringed'),
      'circle-color': toMatchExpression('#ffd978', 'colorKey'),
      'circle-stroke-width': 1.6,
      'circle-stroke-color': '#0b0f14',
      'circle-opacity': 1
    }
  })

  map.addLayer({
    id: 'dashboard-highlight-points-controlled',
    type: 'circle',
    source: 'dashboard-highlight-points',
    filter: ['==', ['get', 'locationStatus'], 'controlled'],
    paint: {
      'circle-radius': recoveryPointRadiusExpression('highlight', 'controlled'),
      'circle-color': CONTROLLED_POINT_FILL,
      'circle-stroke-width': 2.8,
      'circle-stroke-color': toMatchExpression('#ffd978', 'colorKey'),
      'circle-opacity': 1
    }
  })

  map.addLayer({
    id: 'dashboard-highlight-points-mixed',
    type: 'circle',
    source: 'dashboard-highlight-points',
    filter: ['==', ['get', 'locationStatus'], 'mixed'],
    paint: {
      'circle-radius': recoveryPointRadiusExpression('highlight', 'mixed'),
      'circle-color': toMatchExpression('#ffd978', 'colorKey'),
      'circle-stroke-width': 2.5,
      'circle-stroke-color': MIXED_POINT_STROKE,
      'circle-opacity': 1
    }
  })

  map.addLayer({
    id: 'dashboard-ngulia-point',
    type: 'circle',
    source: 'dashboard-ngulia-point',
    paint: {
      'circle-radius': 7,
      'circle-color': '#ff6b6b',
      'circle-stroke-width': 2,
      'circle-stroke-color': '#ffffff',
      'circle-opacity': 1
    }
  })

  bindMapInteractions()
}

function bindMapInteractions() {
  if (interactionsBound) return

  for (const layerId of RECOVERY_POINT_LAYER_IDS) {
    map.on('mouseenter', layerId, (event) => {
      map.getCanvas().style.cursor = 'pointer'
      const feature = event.features?.[0]
      if (!feature) return
      const locationKey = feature.properties?.locationKey || ''
      hoveredLocationKey.value = locationKey
      hoveredRecoveryId.value = (groupedRecoveries.value.get(locationKey) || [])[0]?.id || ''
      syncActiveLocationState()
    })

    map.on('mouseleave', layerId, () => {
      map.getCanvas().style.cursor = ''
      hoveredLocationKey.value = ''
      hoveredRecoveryId.value = ''
      syncActiveLocationState()
    })

    map.on('click', layerId, (event) => {
      const feature = event.features?.[0]
      if (!feature) return
      selectedLocationKey.value = feature.properties?.locationKey || ''
      syncActiveLocationState()
    })
  }

  map.on('click', (event) => {
    if (!map) return
    const features = map.queryRenderedFeatures(event.point, { layers: RECOVERY_POINT_LAYER_IDS })
    if (features.length) return
    selectedLocationKey.value = ''
    hoveredLocationKey.value = ''
    hoveredRecoveryId.value = ''
    syncActiveLocationState()
  })

  interactionsBound = true
}

function highlightRecovery(item) {
  hoveredRecoveryId.value = item.id
  hoveredLocationKey.value = locationKeyForItem(item)
  syncActiveLocationState()
}

function focusRecovery(item) {
  if (!map) return
  selectedLocationKey.value = locationKeyForItem(item)
  hoveredLocationKey.value = ''
  hoveredRecoveryId.value = ''
  syncActiveLocationState()
  map.flyTo({
    center: [item.longitude, item.latitude],
    zoom: Math.max(map.getZoom(), 3.2),
    speed: 0.8,
    curve: 1.2,
    essential: true
  })
}

function clearRecoveryHighlight() {
  hoveredRecoveryId.value = ''
  hoveredLocationKey.value = ''
  syncActiveLocationState()
}

function syncActiveLocationState() {
  if (!map) return
  const activeKey = getActiveLocationKey()
  const activeItems = activeKey ? groupedRecoveries.value.get(activeKey) || [] : []
  const activeData = buildGeoJson(activeItems)
  setSourceData('dashboard-highlight-lines', activeData.lines)
  setSourceData('dashboard-highlight-points', activeData.points)
  popup?.remove()
  if (!activeItems.length) {
    popup = null
    return
  }
  popup = new mapboxgl.Popup({ closeButton: false, offset: 12, className: 'dashboard-map-popup' })
    .setLngLat([activeItems[0].longitude, activeItems[0].latitude])
    .setHTML(recoveryPopupHtml(activeItems))
    .addTo(map)
}

async function scrollToSelectedRecoveryRow() {
  if (!selectedLocationKey.value) return
  await nextTick()
  const tableWrap = recoveryTableWrapRef.value
  const firstSelectedId = filteredRecoveries.value.find((item) => selectedRecoveryIds.value.has(item.id))?.id
  if (!tableWrap || !firstSelectedId) return
  const row = tableWrap.querySelector(`[data-recovery-id="${firstSelectedId}"]`)
  if (!(row instanceof HTMLElement)) return
  const top = row.offsetTop - tableWrap.clientHeight * 0.25
  tableWrap.scrollTo({ top: Math.max(0, top), behavior: 'smooth' })
}

onMounted(async () => {
  const [dashboardPayload, recoveriesPayload, rangesIndexPayload] = await Promise.all([
    getDashboardData(),
    getRecoveriesData(),
    getSpeciesRangesIndex()
  ])
  dashboard.value = dashboardPayload
  recoveriesData.value = recoveriesPayload
  speciesRangesIndex.value = rangesIndexPayload

  await nextTick()
  map = new mapboxgl.Map({
    container: mapRef.value,
    style: selectedMapStyle.value,
    center: [26, 15],
    zoom: 1.45,
    pitch: 18,
    projection: 'globe',
    attributionControl: false
  })

  map.on('style.load', () => {
    if (selectedMapStyle.value.includes('dark')) {
      map.setFog({
        color: 'rgba(8, 14, 21, 0.92)',
        'high-color': 'rgba(40, 70, 110, 0.35)',
        'space-color': 'rgba(2, 4, 8, 1)',
        'horizon-blend': 0.12
      })
    }
    addMapLayers()
  })

  document.addEventListener('fullscreenchange', updateMapFullscreenState)
  resizeObserver = new ResizeObserver(() => {
    if (map) map.resize()
  })
  resizeObserver.observe(mapRef.value)
})

watch([filteredRecoveries, selectedSpeciesId], () => updateMapData())
watch(selectedLocationKey, () => {
  scrollToSelectedRecoveryRow()
})
watch(selectedSpeciesId, async (speciesId) => {
  const requestId = ++rangeRequestId
  selectedLocationKey.value = ''
  hoveredLocationKey.value = ''
  hoveredRecoveryId.value = ''
  popup?.remove()
  selectedSpeciesRange.value = EMPTY_FEATURE_COLLECTION
  updateSpeciesRangeData()
  updateMapData()

  if (!speciesId) {
    return
  }

  const rangeMeta = speciesRangesIndex.value.species?.[speciesId]
  if (!rangeMeta?.available || !rangeMeta.path) {
    return
  }

  try {
    const rangePayload = await getSpeciesRange(rangeMeta.path)
    if (requestId !== rangeRequestId || selectedSpeciesId.value !== speciesId) return
    selectedSpeciesRange.value = rangePayload
    updateSpeciesRangeData()
  } catch (error) {
    if (requestId !== rangeRequestId || selectedSpeciesId.value !== speciesId) return
    selectedSpeciesRange.value = EMPTY_FEATURE_COLLECTION
    updateSpeciesRangeData()
    if (import.meta.env.DEV) {
      console.warn(`Failed to load species range for ${speciesId}`, error)
    }
  }
})
watch(selectedMapStyle, (style) => {
  showMapSettings.value = false
  if (map) map.setStyle(style)
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  popup?.remove()
  document.removeEventListener('fullscreenchange', updateMapFullscreenState)
  if (map) map.remove()
})
</script>

<style scoped>
.dashboard-page {
  padding-bottom: 5rem;
}

.dashboard-headline {
  margin-top: 2rem;
}

.dashboard-context {
  color: var(--accent-soft);
  font-size: 0.95rem;
  letter-spacing: 0.08em;
  margin: 0 0 0.8rem;
  text-transform: uppercase;
}

.dashboard-headline__inner {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(320px, 0.8fr);
  gap: 1.4rem;
  align-items: end;
}

.dashboard-headline__number {
  color: var(--accent-soft);
  font-size: clamp(4.4rem, 12vw, 8rem);
  font-weight: 800;
  line-height: 0.85;
}

.dashboard-headline__label {
  color: var(--text-soft);
  font-size: 1.08rem;
  margin-top: 0.5rem;
}

.dashboard-headline__metrics {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.8rem;
}

.dashboard-headline__metric {
  border-top: 1px solid var(--border);
  padding-top: 0.8rem;
}

.dashboard-headline__metric strong {
  display: block;
  color: var(--text);
  font-size: 1.8rem;
  line-height: 1;
}

.dashboard-headline__metric span {
  display: block;
  color: var(--text-soft);
  margin-top: 0.35rem;
}

.dashboard-selector {
  margin-top: 1rem;
}

.dashboard-selector__inner {
  display: grid;
  grid-template-columns: minmax(240px, 0.9fr) minmax(0, 2.1fr);
  gap: 1rem;
  align-items: stretch;
}

.species-search {
  display: grid;
  gap: 0.65rem;
  align-content: start;
}

.species-sidebar {
  display: grid;
  gap: 1rem;
  align-content: start;
}

.species-treemap-panel {
  display: grid;
  gap: 0.45rem;
  min-width: 0;
}

.species-treemap-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.species-scale-switch {
  display: inline-flex;
  gap: 0.2rem;
  padding: 0.2rem;
  border: 1px solid rgba(243, 239, 230, 0.08);
  border-radius: 999px;
  background: rgba(13, 22, 34, 0.72);
}

.species-scale-switch__button {
  border: 0;
  background: transparent;
  color: var(--text-soft);
  border-radius: 999px;
  padding: 0.45rem 0.8rem;
}

.species-scale-switch__button.is-active {
  background: rgba(242, 193, 78, 0.16);
  color: var(--text);
}

.species-search__label {
  color: var(--accent-soft);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.species-multiselect {
  margin-top: 0.1rem;
  --ms-bg: rgba(13, 22, 34, 0.92);
  --ms-border-color: rgba(243, 239, 230, 0.08);
  --ms-border-color-active: rgba(242, 193, 78, 0.28);
  --ms-ring-color: transparent;
  --ms-radius: 999px;
  --ms-dropdown-radius: 1.1rem;
  --ms-dropdown-bg: rgba(10, 18, 28, 0.98);
  --ms-dropdown-border-color: var(--border);
  --ms-max-height: 320px;
  --ms-placeholder-color: var(--text-soft);
  --ms-caret-color: var(--text-soft);
  --ms-clear-color: var(--text-soft);
  --ms-clear-color-hover: var(--text);
  --ms-option-bg-pointed: rgba(255, 255, 255, 0.06);
  --ms-option-color-pointed: var(--text);
  --ms-option-bg-selected: rgba(242, 193, 78, 0.16);
  --ms-option-color-selected: var(--text);
  --ms-option-bg-selected-pointed: rgba(242, 193, 78, 0.22);
  --ms-option-color-selected-pointed: var(--text);
  --ms-empty-color: var(--text-soft);
}

.dashboard-input {
  width: 100%;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text);
  border-radius: 0.8rem;
  padding: 0.75rem 0.85rem;
}

.dashboard-grid {
  display: grid;
  gap: 1rem;
  margin-top: 1rem;
}

.dashboard-grid--charts,
.dashboard-grid--recoveries {
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
}

.selected-species {
  display: grid;
  grid-template-columns: 84px minmax(0, 1fr);
  gap: 0.85rem;
  align-items: start;
  padding: 0.9rem;
  border: 1px solid rgba(243, 239, 230, 0.08);
  border-radius: 1.1rem;
  background: rgba(255, 255, 255, 0.03);
}

.selected-species__image {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 1rem;
  border: 1px solid var(--border);
}

.selected-species__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.65rem;
}

.selected-species__link {
  text-decoration: none;
}

.selected-species__link:hover {
  background: rgba(78, 167, 160, 0.18);
}

.dashboard-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 1rem;
  margin-bottom: 0.8rem;
}

.recovery-map-panel,
.recovery-table-panel {
  min-height: 640px;
}

.recovery-map-panel {
  overflow: hidden;
}

.recovery-map-panel__inner {
  height: 100%;
  padding: 0;
}

.dashboard-selector :deep(.chart-wrap) {
  min-height: 420px;
}

.species-treemap-panel :deep(.chart-wrap) {
  min-height: 360px;
}

.temporal-panel :deep(.chart-wrap) {
  min-height: 320px;
}

.dashboard-map-shell {
  position: relative;
  height: 100%;
  min-height: 640px;
}

.dashboard-map {
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: 1.5rem;
}

.dashboard-map__header {
  position: absolute;
  top: 1rem;
  left: 1rem;
  z-index: 3;
  display: grid;
  gap: 0.45rem;
  justify-items: start;
}

.dashboard-map__label {
  color: var(--text);
  font-size: 1.15rem;
  font-weight: 700;
  text-shadow: 0 2px 16px rgba(0, 0, 0, 0.45);
}

.dashboard-map__badge {
  align-self: start;
}

.dashboard-map__legend {
  position: absolute;
  z-index: 2;
  right: 1rem;
  bottom: 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.9rem;
  padding: 0.65rem 0.8rem;
  max-width: min(34rem, calc(100% - 2rem));
  border: 1px solid rgba(243, 239, 230, 0.12);
  border-radius: 1rem;
  background: rgba(8, 14, 21, 0.72);
  backdrop-filter: blur(12px);
  color: var(--text);
  font-size: 0.82rem;
}

.dashboard-map__legend span {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
}

.dashboard-map-shell :deep(.mapboxgl-ctrl-bottom-left) {
  left: 1rem;
  bottom: 0.6rem;
}

.dashboard-map-shell :deep(.mapboxgl-ctrl-bottom-right) {
  right: 1rem;
  bottom: 0.6rem;
}

.dashboard-map__swatch {
  width: 0.72rem;
  height: 0.72rem;
  border-radius: 999px;
  display: inline-block;
  box-sizing: border-box;
}

.dashboard-map__legend-divider {
  width: 1px;
  min-height: 0.9rem;
  background: rgba(243, 239, 230, 0.18);
}

.dashboard-map__swatch--wintering {
  background: #f7f3e8;
}

.dashboard-map__swatch--breeding {
  background: #ff2b8a;
}

.dashboard-map__swatch--ringed {
  background: #f2c14e;
  border: 1.4px solid #0b0f14;
}

.dashboard-map__swatch--controlled {
  background: #d8d3c5;
  border: 2px solid #f2c14e;
}

.dashboard-map__swatch--mixed {
  background: #f2c14e;
  border: 2px solid #6e7884;
}

.map-controls {
  position: absolute;
  top: 0.9rem;
  right: 0.9rem;
  z-index: 5;
  display: grid;
  gap: 0.55rem;
}

.map-controls__button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.35rem;
  min-height: 2.35rem;
  padding: 0;
  border: 1px solid rgba(243, 239, 230, 0.16);
  border-radius: 0.65rem;
  background:
    linear-gradient(180deg, rgba(17, 24, 34, 0.95), rgba(8, 13, 19, 0.88)),
    rgba(7, 12, 18, 0.82);
  color: var(--text);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22), inset 0 0 0 1px rgba(255, 217, 120, 0.04);
  backdrop-filter: blur(12px);
  transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
}

.map-controls__button:hover {
  transform: translateY(-1px);
  border-color: rgba(255, 217, 120, 0.36);
  background:
    linear-gradient(180deg, rgba(25, 34, 47, 0.97), rgba(10, 16, 24, 0.92)),
    rgba(7, 12, 18, 0.9);
}

.map-controls__button:focus-visible {
  outline: 2px solid rgba(255, 217, 120, 0.65);
  outline-offset: 2px;
}

.map-controls__button svg {
  width: 1rem;
  height: 1rem;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.recovery-map-settings {
  position: absolute;
  top: 0.9rem;
  right: 4rem;
  width: min(15rem, calc(100% - 6rem));
  z-index: 5;
  display: grid;
  gap: 0.62rem;
  padding: 0.85rem;
  border: 1px solid rgba(243, 239, 230, 0.14);
  border-radius: 0.8rem;
  background: rgba(7, 12, 18, 0.76);
  backdrop-filter: blur(12px);
}

.recovery-map-settings label {
  display: grid;
  gap: 0.32rem;
  min-width: 0;
  color: var(--text-soft);
  font-size: 0.76rem;
}

.recovery-map-settings span {
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.recovery-map-settings select {
  width: 100%;
}

.dashboard-map-shell:fullscreen {
  min-height: 100vh;
  background: #05080d;
}

.dashboard-map-shell:fullscreen .dashboard-map {
  border-radius: 0;
}

.recovery-table-wrap {
  margin-top: 1rem;
  max-height: 520px;
  overflow: auto;
  border: 1px solid var(--border);
  border-radius: 1rem;
}

.recovery-table {
  width: 100%;
  min-width: 42rem;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.recovery-table th,
.recovery-table td {
  padding: 0.75rem 0.8rem;
  border-bottom: 1px solid rgba(243, 239, 230, 0.08);
  text-align: left;
  vertical-align: top;
}

.recovery-table th {
  position: sticky;
  top: 0;
  z-index: 1;
  background: rgba(10, 18, 28, 0.98);
  color: var(--accent-soft);
  font-size: 0.74rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.recovery-table tr {
  transition: background 120ms ease;
}

.recovery-table tbody tr:hover,
.recovery-table tbody tr.is-hovered {
  background: rgba(242, 193, 78, 0.12);
}

.recovery-table tbody tr.is-selected {
  background: rgba(242, 193, 78, 0.2);
}

.recovery-table__date {
  white-space: nowrap;
}

.recovery-table__species {
  white-space: nowrap;
}

.recovery-table__note {
  margin: 0.65rem 0 0;
  color: var(--text-soft);
  font-size: 0.78rem;
}

:deep(.dashboard-map-popup .mapboxgl-popup-content) {
  padding: 0;
  overflow: hidden;
  border: 1px solid rgba(243, 239, 230, 0.16);
  border-radius: 1rem;
  background: rgba(10, 18, 28, 0.98);
  color: var(--text);
  box-shadow: var(--shadow);
}

:deep(.dashboard-map-popup .mapboxgl-popup-tip) {
  border-top-color: rgba(10, 18, 28, 0.98);
  border-bottom-color: rgba(10, 18, 28, 0.98);
}

:deep(.species-multiselect .multiselect) {
  width: 100%;
  min-height: 54px;
  border: 1px solid rgba(243, 239, 230, 0.08);
  border-radius: 999px;
  background:
    linear-gradient(180deg, rgba(24, 35, 50, 0.9), rgba(13, 22, 34, 0.96));
  box-shadow: none;
  margin: 0;
  overflow: hidden;
  transition: border-color 140ms ease, background 140ms ease, transform 140ms ease;
}

:deep(.species-multiselect .multiselect.is-active),
:deep(.species-multiselect .multiselect.is-open) {
  border-color: rgba(242, 193, 78, 0.28);
  background:
    linear-gradient(180deg, rgba(28, 40, 56, 0.96), rgba(16, 26, 38, 0.98));
  box-shadow: 0 14px 32px rgba(0, 0, 0, 0.22);
  transform: translateY(-1px);
}

:deep(.species-multiselect .multiselect-wrapper) {
  width: 100%;
  min-height: 54px;
  margin: 0;
  justify-content: flex-start;
  position: relative;
}

:deep(.species-multiselect .multiselect-single-label),
:deep(.species-multiselect .multiselect-placeholder),
:deep(.species-multiselect .multiselect-search) {
  color: var(--text);
  background: transparent;
  font-size: 1rem;
}

:deep(.species-multiselect .multiselect-placeholder) {
  color: var(--text-soft);
  opacity: 0.82;
}

:deep(.species-multiselect .multiselect-search) {
  width: 100%;
  padding-left: 1.15rem;
  padding-right: 4.6rem;
}

:deep(.species-multiselect .multiselect-single-label) {
  padding-left: 1.15rem;
  padding-right: 4.6rem;
}

:deep(.species-multiselect .multiselect-single-label-text) {
  letter-spacing: 0.01em;
}

:deep(.species-multiselect .multiselect-caret),
:deep(.species-multiselect .multiselect-clear) {
  color: var(--text-soft);
  opacity: 0.88;
  position: absolute;
  top: 50%;
  z-index: 12;
  transform: translateY(-50%);
}

:deep(.species-multiselect .multiselect-caret) {
  right: 1rem;
  margin: 0;
}

:deep(.species-multiselect .multiselect-clear) {
  right: 2.6rem;
  padding: 0;
  margin: 0;
}

:deep(.species-multiselect .multiselect-dropdown) {
  margin-top: 0.5rem;
  border: 1px solid var(--border);
  border-radius: 1.1rem;
  background: rgba(10, 18, 28, 0.98);
  box-shadow: var(--shadow);
  overflow-x: hidden;
  overflow-y: auto;
  max-height: 320px;
  scrollbar-width: thin;
  scrollbar-color: rgba(242, 193, 78, 0.45) rgba(255, 255, 255, 0.04);
}

:deep(.species-multiselect .multiselect-options) {
  padding: 0.4rem;
}

:deep(.species-multiselect .multiselect-dropdown::-webkit-scrollbar) {
  width: 10px;
}

:deep(.species-multiselect .multiselect-dropdown::-webkit-scrollbar-track) {
  background: rgba(255, 255, 255, 0.04);
}

:deep(.species-multiselect .multiselect-dropdown::-webkit-scrollbar-thumb) {
  border: 2px solid rgba(10, 18, 28, 0.98);
  border-radius: 999px;
  background: rgba(242, 193, 78, 0.45);
}

:deep(.species-multiselect .multiselect-option) {
  border-radius: 0.8rem;
  color: var(--text-soft);
  padding: 0.78rem 0.9rem;
}

:deep(.species-multiselect .multiselect-option.is-pointed) {
  background: rgba(255, 255, 255, 0.06);
  color: var(--text);
}

:deep(.species-multiselect .multiselect-option.is-selected) {
  background: rgba(242, 193, 78, 0.14);
  color: var(--text);
}

:deep(.species-multiselect .multiselect-option.is-selected.is-pointed) {
  background: rgba(242, 193, 78, 0.2);
  color: var(--text);
}

:deep(.species-multiselect .multiselect-no-options),
:deep(.species-multiselect .multiselect-no-results) {
  color: var(--text-soft);
  background: transparent;
  padding: 0.8rem;
}

:deep(.map-popup) {
  min-width: 200px;
  padding: 0.6rem 0.7rem;
}

:deep(.map-popup__site) {
  color: var(--text);
  font-weight: 700;
  line-height: 1.1;
  font-size: 0.88rem;
}

:deep(.map-popup__meta) {
  color: var(--text-soft);
  margin-top: 0.22rem;
  font-size: 0.78rem;
}

:deep(.map-popup__list) {
  margin-top: 0.45rem;
  display: grid;
  gap: 0.55rem;
  font-size: 0.77rem;
  color: var(--text-soft);
}

:deep(.map-popup__group) {
  display: grid;
  gap: 0.22rem;
}

:deep(.map-popup__species) {
  color: var(--text);
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

:deep(.map-popup__bullets) {
  margin: 0;
  padding-left: 1rem;
  display: grid;
  gap: 0.3rem;
}

:deep(.map-popup__bullets li) {
  margin: 0;
}

:deep(.map-popup__item-main) {
  color: var(--text-soft);
}

:deep(.map-popup__item-sub) {
  color: rgba(243, 239, 230, 0.68);
  font-size: 0.72rem;
}

:deep(.map-popup__more) {
  color: rgba(243, 239, 230, 0.68);
}

@media (max-width: 980px) {
  .dashboard-headline__inner,
  .dashboard-selector__inner,
  .dashboard-grid--charts,
  .dashboard-grid--recoveries {
    grid-template-columns: 1fr;
  }

  .recovery-map-panel,
  .recovery-table-panel {
    min-height: auto;
  }

  .dashboard-map__badge {
    top: 4rem;
  }
}

@media (max-width: 640px) {
  .species-treemap-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .species-scale-switch {
    width: 100%;
  }

  .species-scale-switch__button {
    flex: 1 1 0;
  }

  .dashboard-headline__metrics {
    grid-template-columns: 1fr;
  }

  .dashboard-headline__number {
    font-size: 4rem;
  }

  .selected-species {
    grid-template-columns: 1fr;
  }

  .dashboard-map-shell,
  .dashboard-map {
    min-height: 34rem;
  }

  .dashboard-map__header {
    top: 0.55rem;
    left: 0.55rem;
    right: 4rem;
    gap: 0.35rem;
  }

  .dashboard-map__label {
    font-size: 1rem;
  }

  .dashboard-map__legend {
    left: 0.55rem;
    right: 0.55rem;
    bottom: 0.55rem;
    gap: 0.5rem 0.8rem;
    padding: 0.55rem 0.65rem;
    max-width: none;
    font-size: 0.75rem;
  }

  .map-controls {
    top: 0.55rem;
    right: 0.55rem;
  }

  .recovery-map-settings {
    top: 3.7rem;
    left: 0.55rem;
    right: 0.55rem;
    width: auto;
  }

  .dashboard-selector :deep(.chart-wrap) {
    min-height: 340px;
  }

  .temporal-panel :deep(.chart-wrap) {
    min-height: 280px;
  }

  .recovery-table {
    min-width: 36rem;
  }

  .recovery-table__date,
  .recovery-table__species {
    white-space: normal;
  }
}
</style>
