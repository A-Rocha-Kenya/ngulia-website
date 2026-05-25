<template>
  <div class="home-view">
    <div class="home-background" aria-hidden="true" :style="heroBackgroundStyle">
      <BirdSky :settings="heroAnimationControls" />
      <div class="home-background__beam"></div>
      <div class="home-background__veil"></div>
    </div>

    <section class="home-hero">
      <div class="page home-hero__content">
        <div class="hero-controls">
          <button
            class="map-controls__button"
            type="button"
            :aria-expanded="showHeroSettings ? 'true' : 'false'"
            aria-controls="hero-settings-panel"
            aria-label="Hero animation settings"
            title="Hero animation settings"
            @click="showHeroSettings = !showHeroSettings"
          >
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path
                d="M10.4 2.6h3.2l.55 2.25c.54.18 1.06.4 1.55.67l1.99-1.2 2.26 2.26-1.2 1.99c.27.49.49 1.01.67 1.55l2.25.55v3.2l-2.25.55c-.18.54-.4 1.06-.67 1.55l1.2 1.99-2.26 2.26-1.99-1.2c-.49.27-1.01.49-1.55.67l-.55 2.25h-3.2l-.55-2.25a8.14 8.14 0 0 1-1.55-.67l-1.99 1.2-2.26-2.26 1.2-1.99a8.14 8.14 0 0 1-.67-1.55L2.6 13.6v-3.2l2.25-.55c.18-.54.4-1.06.67-1.55l-1.2-1.99L6.58 4.05l1.99 1.2c.49-.27 1.01-.49 1.55-.67zM12 8.35A3.65 3.65 0 1 0 12 15.65 3.65 3.65 0 0 0 12 8.35z"
              />
            </svg>
            <span class="sr-only">Hero settings</span>
          </button>
        </div>
        <div
          v-if="showHeroSettings"
          id="hero-settings-panel"
          class="migration-controls hero-settings"
          aria-label="Hero animation settings"
        >
          <div class="hero-settings__section">
            <div class="hero-settings__title">Birds</div>
            <div class="migration-controls__row">
              <label>
                <span>Base min delay {{ heroAnimationControls.baseDelayMin }} ms</span>
                <input
                  v-model.number="heroAnimationControls.baseDelayMin"
                  type="range"
                  min="300"
                  max="1800"
                  step="50"
                />
              </label>
              <label>
                <span>Base max delay {{ heroAnimationControls.baseDelayMax }} ms</span>
                <input
                  v-model.number="heroAnimationControls.baseDelayMax"
                  type="range"
                  min="800"
                  max="3200"
                  step="50"
                />
              </label>
            </div>
            <div class="migration-controls__row">
              <label>
                <span>Burst min birds {{ heroAnimationControls.burstMinCount }}</span>
                <input
                  v-model.number="heroAnimationControls.burstMinCount"
                  type="range"
                  min="2"
                  max="10"
                  step="1"
                />
              </label>
              <label>
                <span>Burst max birds {{ heroAnimationControls.burstMaxCount }}</span>
                <input
                  v-model.number="heroAnimationControls.burstMaxCount"
                  type="range"
                  min="3"
                  max="12"
                  step="1"
                />
              </label>
            </div>
            <div class="migration-controls__row">
              <label>
                <span>Start jitter {{ heroAnimationControls.startJitter.toFixed(1) }}</span>
                <input
                  v-model.number="heroAnimationControls.startJitter"
                  type="range"
                  min="0"
                  max="5"
                  step="0.1"
                />
              </label>
              <label>
                <span>End jitter {{ heroAnimationControls.endJitter.toFixed(1) }}</span>
                <input
                  v-model.number="heroAnimationControls.endJitter"
                  type="range"
                  min="0"
                  max="6"
                  step="0.1"
                />
              </label>
            </div>
          </div>

          <div class="hero-settings__section">
            <div class="hero-settings__title">Light</div>
            <div class="migration-controls__row">
              <label>
                <span>Beam width {{ heroSceneControls.beamWidth }} rem</span>
                <input
                  v-model.number="heroSceneControls.beamWidth"
                  type="range"
                  min="48"
                  max="110"
                  step="1"
                />
              </label>
              <label>
                <span>Beam height {{ heroSceneControls.beamHeight }} rem</span>
                <input
                  v-model.number="heroSceneControls.beamHeight"
                  type="range"
                  min="56"
                  max="110"
                  step="1"
                />
              </label>
            </div>
            <div class="migration-controls__row">
              <label>
                <span>Beam blur {{ heroSceneControls.beamBlur }} px</span>
                <input
                  v-model.number="heroSceneControls.beamBlur"
                  type="range"
                  min="12"
                  max="60"
                  step="1"
                />
              </label>
              <label>
                <span>Beam strength {{ heroSceneControls.beamStrength.toFixed(2) }}</span>
                <input
                  v-model.number="heroSceneControls.beamStrength"
                  type="range"
                  min="0.5"
                  max="1.4"
                  step="0.02"
                />
              </label>
            </div>
          </div>

          <div class="hero-settings__section">
            <div class="hero-settings__title">Mist</div>
            <div class="migration-controls__row">
              <label>
                <span>Lower mist {{ heroSceneControls.lowerMist.toFixed(2) }}</span>
                <input
                  v-model.number="heroSceneControls.lowerMist"
                  type="range"
                  min="0"
                  max="1"
                  step="0.02"
                />
              </label>
              <label>
                <span>Veil blur {{ heroSceneControls.veilBlur.toFixed(1) }} px</span>
                <input
                  v-model.number="heroSceneControls.veilBlur"
                  type="range"
                  min="0"
                  max="8"
                  step="0.2"
                />
              </label>
            </div>
            <div class="migration-controls__row">
              <label>
                <span>Bird fade start {{ heroAnimationControls.lowerFadeStart }}%</span>
                <input
                  v-model.number="heroAnimationControls.lowerFadeStart"
                  type="range"
                  min="45"
                  max="85"
                  step="1"
                />
              </label>
              <label>
                <span>Bird fade end {{ heroAnimationControls.lowerFadeEnd }}%</span>
                <input
                  v-model.number="heroAnimationControls.lowerFadeEnd"
                  type="range"
                  min="80"
                  max="100"
                  step="1"
                />
              </label>
            </div>
          </div>
        </div>
        <div class="home-hero__copy">
          <h1 class="home-hero__title">Ringing science in light, mist, and migration.</h1>
          <p class="home-hero__intro">
            For more than fifty years, the Ngulia Bird Migration Project has documented one of
            Africa’s most remarkable migration phenomena, when mist and the lodge lights attract
            thousands of nocturnal bird migrants down.
          </p>
        </div>
        <div class="home-hero__scroll-cue">Scroll to continue</div>
      </div>
    </section>

    <section class="home-map-section">
      <article class="panel home-map-section__panel">
        <div class="panel-inner home-map-section__inner">
          <div ref="mapContentRef" class="home-map-section__content">
            <div class="home-map-section__intro">
              <div class="section-label">Migration In Motion</div>
              <h2 class="home-map-section__title">
                Ngulai at the center of the East african Flyway
              </h2>
              <p class="home-map-section__text">
                During November and December, long-distance Afro-Palearctic migrants moving from
                Europe and Asia toward southern Africa pass in large numbers across the Tsavo region
                of southeastern Kenya.
              </p>
              <p class="home-map-section__note">
                This illustration was generated using a particle simulation built from ring
                recoveries linked to Ngulia, with an artificially induced pull toward Ngulia.
              </p>
            </div>

            <div class="home-map-section__stats">
              <StatCard
                label="Birds ringed"
                :value="formatNumber(summary.totalBirds)"
                description="Processed from the 1991-2023 master ringing workbook."
              />
              <StatCard
                label="Recoveries"
                :value="formatNumber(summary.totalRecoveries)"
                description="Long-distance links prepared for the dashboard recovery map."
              />
            </div>
          </div>

          <div class="home-map-section__viewport">
            <div ref="mapRef" class="map-wrap home-overview__map"></div>
            <div ref="nguliaMarkerRef" class="ngulia-marker-overlay">
              <button
                class="ngulia-marker-overlay__button"
                type="button"
                aria-label="Open Ngulia location details"
                :aria-expanded="showNguliaPopup ? 'true' : 'false'"
                @click.stop="showNguliaPopup = !showNguliaPopup"
              >
                <span class="ngulia-marker-overlay__dot"></span>
              </button>
              <div v-if="showNguliaPopup" class="ngulia-marker-overlay__popup">
                <span>Ngulia</span>
                <a
                  class="ngulia-marker-overlay__direction"
                  href="https://maps.app.goo.gl/YaBeC1uCZktYKiyM8"
                  target="_blank"
                  rel="noreferrer"
                  aria-label="Open Ngulia in Google Maps"
                  title="Open in Google Maps"
                  @click.stop
                >
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M21 3 10 14" />
                    <path d="M21 3 15 21l-5-7-7-5z" />
                    <circle cx="10" cy="14" r="1.2" fill="currentColor" stroke="none" />
                  </svg>
                </a>
              </div>
            </div>
            <div class="map-controls">
              <button
                class="map-controls__button"
                type="button"
                aria-label="Zoom in"
                title="Zoom in"
                @click="zoomMapIn"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M12 5v14M5 12h14" />
                </svg>
                <span class="sr-only">Zoom in</span>
              </button>
              <button
                class="map-controls__button"
                type="button"
                aria-label="Zoom out"
                title="Zoom out"
                @click="zoomMapOut"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M5 12h14" />
                </svg>
                <span class="sr-only">Zoom out</span>
              </button>
              <button
                class="map-controls__button"
                type="button"
                :aria-expanded="showSettings ? 'true' : 'false'"
                aria-controls="migration-settings-panel"
                aria-label="Map settings"
                title="Map settings"
                @click="showSettings = !showSettings"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path
                    d="M10.4 2.6h3.2l.55 2.25c.54.18 1.06.4 1.55.67l1.99-1.2 2.26 2.26-1.2 1.99c.27.49.49 1.01.67 1.55l2.25.55v3.2l-2.25.55c-.18.54-.4 1.06-.67 1.55l1.2 1.99-2.26 2.26-1.99-1.2c-.49.27-1.01.49-1.55.67l-.55 2.25h-3.2l-.55-2.25a8.14 8.14 0 0 1-1.55-.67l-1.99 1.2-2.26-2.26 1.2-1.99a8.14 8.14 0 0 1-.67-1.55L2.6 13.6v-3.2l2.25-.55c.18-.54.4-1.06.67-1.55l-1.2-1.99L6.58 4.05l1.99 1.2c.49-.27 1.01-.49 1.55-.67zM12 8.35A3.65 3.65 0 1 0 12 15.65 3.65 3.65 0 0 0 12 8.35z"
                  />
                </svg>
                <span class="sr-only">Settings</span>
              </button>
            </div>
            <div
              v-if="showSettings"
              id="migration-settings-panel"
              class="migration-controls"
              aria-label="Migration animation controls"
            >
              <div class="migration-controls__row migration-controls__row--single">
                <label>
                  <span>Layer</span>
                  <select v-model="selectedMapStyle">
                    <option v-for="style in mapStyles" :key="style.value" :value="style.value">
                      {{ style.label }}
                    </option>
                  </select>
                </label>
              </div>

              <div class="migration-controls__row">
                <label>
                  <span>Birds {{ formatNumber(migrationControls.count) }}</span>
                  <input
                    v-model.number="migrationControls.count"
                    type="range"
                    min="500"
                    max="3000"
                    step="100"
                  />
                </label>
                <label>
                  <span>Speed {{ migrationControls.speed.toFixed(1) }}x</span>
                  <input
                    v-model.number="migrationControls.speed"
                    type="range"
                    min="0.5"
                    max="3"
                    step="0.1"
                  />
                </label>
              </div>

              <div class="migration-controls__row">
                <label>
                  <span>Ngulia pull {{ migrationControls.pull.toFixed(2) }}</span>
                  <input
                    v-model.number="migrationControls.pull"
                    type="range"
                    min="0"
                    max="1"
                    step="0.05"
                  />
                </label>
                <label>
                  <span>Trail {{ Math.round(migrationControls.trail * 100) }}</span>
                  <input
                    v-model.number="migrationControls.trail"
                    type="range"
                    min="0.01"
                    max="0.12"
                    step="0.01"
                  />
                </label>
              </div>
            </div>
          </div>
        </div>
      </article>
    </section>

    <section class="page home-view__section">
      <div class="home-story-strip">
        <div class="home-story-strip__intro">
          <div class="section-label">Ngulia At A Glance</div>
          <h2 class="panel-title home-story-strip__title">The essentials.</h2>
        </div>

        <div class="grid home-story-strip__grid">
          <article v-for="box in historyVisitorBoxes" :key="box.title" class="panel">
            <div class="panel-inner">
              <div class="eyebrow">{{ box.eyebrow }}</div>
              <h2 class="panel-title">{{ box.title }}</h2>
              <ul class="bullets home-story-strip__bullets">
                <li v-for="item in box.items" :key="item">{{ item }}</li>
              </ul>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="page home-view__section">
      <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr))">
        <article v-for="card in homeCards" :key="card.to" class="panel">
          <div class="panel-inner">
            <div class="eyebrow">{{ card.label }}</div>
            <h2 class="panel-title">{{ card.title }}</h2>
            <p class="page-intro" style="font-size: 0.98rem; max-width: none">{{ card.text }}</p>
            <RouterLink class="button-link" :to="card.to">Open section</RouterLink>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import "mapbox-gl/dist/mapbox-gl.css";
import { MapboxOverlay } from "@deck.gl/mapbox";
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import BirdSky from "../components/BirdSky.vue";
import StatCard from "../components/StatCard.vue";
import { historyVisitorBoxes, homeCards } from "../data/siteContent.js";
import { getDashboardData, getMigrationProbabilitiesData } from "../lib/generatedData.js";
import mapboxgl from "../lib/mapbox.js";
import {
  advanceParticles,
  createMigrationParticles,
  migrationDeckLayers,
  syncParticleCount,
} from "../lib/migrationAnimation.js";
const NGULIA_COORDS = [38.211134674309974, -3.0140288001023605];
const summary = reactive({
  totalBirds: 0,
  totalSpecies: 0,
  yearStart: null,
  yearEnd: null,
  totalRecoveries: 0,
});
const migrationControls = reactive({
  speed: 1.4,
  count: 1500,
  pull: 1,
  trail: 0.04,
  fade: 0.18,
  site: NGULIA_COORDS,
});
const mapRef = ref(null);
const mapContentRef = ref(null);
const nguliaMarkerRef = ref(null);
const migrationProbabilities = ref(null);
const selectedMapStyle = ref("mapbox://styles/mapbox/dark-v11");
const showSettings = ref(false);
const showNguliaPopup = ref(false);
const showHeroSettings = ref(false);

const heroAnimationControls = reactive({
  baseDelayMin: 900,
  baseDelayMax: 3100,
  burstMinCount: 5,
  burstMaxCount: 8,
  burstDelayMin: 80,
  burstDelayMax: 420,
  burstDurationMin: 3000,
  burstDurationMax: 4600,
  burstPauseMin: 8500,
  burstPauseMax: 12500,
  startJitter: 1.5,
  endJitter: 3.2,
  topJitter: 2.5,
  durationJitter: 0.12,
  lowerFadeStart: 62,
  lowerFadeEnd: 100,
});

const heroSceneControls = reactive({
  beamWidth: 78,
  beamHeight: 86,
  beamBlur: 32,
  beamStrength: 1,
  lowerMist: 0.58,
  veilBlur: 1,
});

const heroBackgroundStyle = computed(() => ({
  "--hero-beam-width": `${heroSceneControls.beamWidth}rem`,
  "--hero-beam-height": `${heroSceneControls.beamHeight}rem`,
  "--hero-beam-blur": `${heroSceneControls.beamBlur}px`,
  "--hero-beam-strength": heroSceneControls.beamStrength,
  "--hero-lower-mist": heroSceneControls.lowerMist,
  "--hero-veil-blur": `${heroSceneControls.veilBlur}px`,
}));

const mapStyles = [
  { label: "Dark", value: "mapbox://styles/mapbox/dark-v11" },
  { label: "Satellite streets", value: "mapbox://styles/mapbox/satellite-streets-v12" },
  { label: "Satellite", value: "mapbox://styles/mapbox/satellite-v9" },
  { label: "Outdoors", value: "mapbox://styles/mapbox/outdoors-v12" },
  { label: "Light", value: "mapbox://styles/mapbox/light-v11" },
];

let map;
let deckOverlay;
let particles = [];
let animationFrame;
let lastFrameTime = 0;
let resizeObserver;

function formatNumber(value) {
  return new Intl.NumberFormat("en-US").format(value || 0);
}

function updateNguliaMarker() {
  if (!map || !nguliaMarkerRef.value) return;
  const point = map.project(NGULIA_COORDS);
  nguliaMarkerRef.value.style.transform = `translate(${point.x}px, ${point.y}px) translate(-50%, -50%)`;
}

function syncMapViewport() {
  if (!map) return;

  const mapRect = mapRef.value?.getBoundingClientRect();
  const contentRect = mapContentRef.value?.getBoundingClientRect();
  if (!mapRect || !contentRect) return;

  const contentMaxWidth =
    Number.parseFloat(
      getComputedStyle(document.documentElement).getPropertyValue("--content-width"),
    ) || 1180;
  const mapWidth = mapRect?.width ?? 0;
  const mapHeight = mapRect?.height ?? 0;
  const boundedContentWidth = Math.min(contentMaxWidth, Math.max(0, mapWidth - 32));
  const contentSideInset = Math.max(16, Math.round((mapWidth - boundedContentWidth) / 2));
  const desiredPoint = [
    (contentRect.right - mapRect.left + (mapWidth - contentSideInset)) / 2,
    mapHeight / 2 + 20,
  ];

  for (let i = 0; i < 6; i += 1) {
    const nguliaPoint = map.project(NGULIA_COORDS);
    const deltaX = nguliaPoint.x - desiredPoint[0];
    const deltaY = nguliaPoint.y - desiredPoint[1];
    if (Math.abs(deltaX) < 1 && Math.abs(deltaY) < 1) break;
    const adjustedCenter = map.unproject([mapWidth / 2 + deltaX, mapHeight / 2 + deltaY]);
    map.jumpTo({ center: adjustedCenter });
  }
}

function closeNguliaPopup() {
  showNguliaPopup.value = false;
}

function zoomMapIn() {
  if (map) map.zoomIn({ duration: 250 });
}

function zoomMapOut() {
  if (map) map.zoomOut({ duration: 250 });
}

function renderMigrationFrame(timestamp) {
  if (!deckOverlay || !migrationProbabilities.value) return;

  const delta = lastFrameTime ? Math.min(timestamp - lastFrameTime, 80) : 16;
  lastFrameTime = timestamp;
  particles = advanceParticles(particles, migrationProbabilities.value, migrationControls, delta);
  deckOverlay.setProps({ layers: migrationDeckLayers(particles, migrationControls) });
  animationFrame = requestAnimationFrame(renderMigrationFrame);
}

function resetMigrationParticles() {
  if (!migrationProbabilities.value) return;
  particles = createMigrationParticles(migrationProbabilities.value, migrationControls);
}

function startMigrationAnimation() {
  resetMigrationParticles();
  if (animationFrame) cancelAnimationFrame(animationFrame);
  lastFrameTime = 0;
  animationFrame = requestAnimationFrame(renderMigrationFrame);
}

onMounted(async () => {
  const [data, probabilityData] = await Promise.all([
    getDashboardData(),
    getMigrationProbabilitiesData(),
  ]);
  Object.assign(summary, data.summary);
  migrationProbabilities.value = probabilityData;

  await nextTick();

  map = new mapboxgl.Map({
    container: mapRef.value,
    style: selectedMapStyle.value,
    center: [38.5, 8.5],
    zoom: 1.62,
    pitch: 8,
    maxPitch: 45,
    bearing: 0,
    projection: "mercator",
    attributionControl: false,
    renderWorldCopies: false,
  });

  map.scrollZoom.disable();

  map.on("style.load", () => {
    map.setFog({
      "color": "rgba(6, 10, 18, 0.95)",
      "high-color": "rgba(18, 28, 46, 0.78)",
      "space-color": "rgba(1, 3, 7, 1)",
      "star-intensity": 0.2,
      "horizon-blend": 0.08,
    });
  });

  map.on("click", closeNguliaPopup);
  map.on("render", updateNguliaMarker);
  updateNguliaMarker();

  deckOverlay = new MapboxOverlay({ interleaved: false, layers: [] });
  map.addControl(deckOverlay);
  startMigrationAnimation();
  map.once("idle", syncMapViewport);
  window.setTimeout(() => {
    if (!map) return;
    map.resize();
    syncMapViewport();
    updateNguliaMarker();
  }, 320);

  resizeObserver = new ResizeObserver(() => {
    if (map) {
      map.resize();
      syncMapViewport();
      updateNguliaMarker();
    }
  });
  resizeObserver.observe(mapRef.value);
  if (mapContentRef.value) resizeObserver.observe(mapContentRef.value);
});

watch(
  () => migrationControls.count,
  () => {
    if (migrationProbabilities.value)
      particles = syncParticleCount(particles, migrationProbabilities.value, migrationControls);
  },
);

watch(() => migrationControls.pull, resetMigrationParticles);
watch(selectedMapStyle, (style) => {
  if (!map) return;
  map.setStyle(style);
  map.once("styledata", () => {
    syncMapViewport();
    updateNguliaMarker();
  });
});

onBeforeUnmount(() => {
  if (animationFrame) cancelAnimationFrame(animationFrame);
  if (resizeObserver) resizeObserver.disconnect();
  if (map) map.off("click", closeNguliaPopup);
  if (map) map.off("render", updateNguliaMarker);
  if (map && deckOverlay) map.removeControl(deckOverlay);
  if (map) map.remove();
});
</script>

<style scoped>
.home-view {
  position: relative;
}

.home-background {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.home-background__beam {
  position: absolute;
  bottom: -27rem;
  left: 50%;
  width: min(var(--hero-beam-width, 78rem), 104vw);
  height: var(--hero-beam-height, 86rem);
  transform: translateX(-50%);
  background:
    radial-gradient(
      ellipse at 50% 100%,
      rgba(255, 231, 160, var(--hero-beam-strength, 1)) 0%,
      rgba(255, 214, 103, calc(0.92 * var(--hero-beam-strength, 1))) 8%,
      rgba(247, 190, 58, calc(0.58 * var(--hero-beam-strength, 1))) 18%,
      rgba(247, 190, 58, calc(0.2 * var(--hero-beam-strength, 1))) 34%,
      rgba(247, 190, 58, 0) 56%
    ),
    radial-gradient(
      ellipse at 50% 84%,
      rgba(255, 213, 102, calc(0.34 * var(--hero-beam-strength, 1))) 0%,
      rgba(255, 213, 102, calc(0.17 * var(--hero-beam-strength, 1))) 20%,
      rgba(255, 213, 102, calc(0.06 * var(--hero-beam-strength, 1))) 38%,
      rgba(255, 213, 102, 0) 58%
    ),
    radial-gradient(
      ellipse at 50% 60%,
      rgba(255, 214, 118, calc(0.12 * var(--hero-beam-strength, 1))) 0%,
      rgba(255, 214, 118, calc(0.04 * var(--hero-beam-strength, 1))) 18%,
      rgba(255, 214, 118, 0) 44%
    );
  filter: blur(var(--hero-beam-blur, 32px));
  opacity: 1;
}

.home-background__veil {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(
      ellipse at 50% 100%,
      rgba(255, 223, 154, calc(0.2 * var(--hero-lower-mist, 0.58))) 0%,
      rgba(236, 192, 92, calc(0.14 * var(--hero-lower-mist, 0.58))) 16%,
      rgba(128, 98, 52, calc(0.06 * var(--hero-lower-mist, 0.58))) 30%,
      rgba(128, 98, 52, 0) 48%
    ),
    radial-gradient(
      ellipse at 50% 88%,
      rgba(244, 208, 126, calc(0.12 * var(--hero-lower-mist, 0.58))) 0%,
      rgba(170, 132, 70, calc(0.06 * var(--hero-lower-mist, 0.58))) 24%,
      rgba(170, 132, 70, 0) 42%
    ),
    linear-gradient(
      180deg,
      rgba(7, 11, 17, 0.18) 0%,
      rgba(7, 11, 17, 0.08) 24%,
      rgba(10, 15, 21, 0.14) 52%,
      rgba(22, 19, 14, 0.24) 68%,
      rgba(42, 34, 22, 0.42) 84%,
      rgba(72, 57, 37, 0.58) 100%
    ),
    linear-gradient(
      180deg,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 244, 214, 0.012) 58%,
      rgba(244, 220, 165, 0.05) 78%,
      rgba(236, 206, 146, 0.1) 100%
    );
  backdrop-filter: blur(var(--hero-veil-blur, 1px));
}

.home-hero {
  position: relative;
  min-height: calc(100vh - var(--header-height));
  min-height: calc(100dvh - var(--header-height));
  z-index: 1;
}

.home-hero__content {
  position: relative;
  display: grid;
  align-items: center;
  min-height: inherit;
  padding-top: clamp(1.6rem, 4vh, 3rem);
  padding-bottom: clamp(1.6rem, 4vh, 3rem);
}

.hero-controls {
  position: absolute;
  top: 1rem;
  right: 0;
  z-index: 4;
}

.hero-settings {
  top: 4.2rem;
  right: 0;
  width: min(34rem, calc(100% - 1rem));
  max-height: min(72vh, 42rem);
  overflow: auto;
}

.hero-settings__section {
  display: grid;
  gap: 0.7rem;
}

.hero-settings__section + .hero-settings__section {
  padding-top: 0.15rem;
  border-top: 1px solid rgba(243, 239, 230, 0.08);
}

.hero-settings__title {
  color: var(--accent-soft);
  font-size: 0.78rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.home-hero__copy {
  display: grid;
  align-self: center;
  max-width: 42rem;
  padding-bottom: 3.5rem;
}

.home-hero__title {
  font-size: clamp(2.8rem, 7vw, 6.4rem);
  line-height: 0.92;
  max-width: 12ch;
  margin: 1.2rem 0 1rem;
}

.home-hero__intro {
  max-width: 42rem;
  color: var(--text-soft);
  font-size: 1.08rem;
  line-height: 1.8;
}

.home-map-section {
  position: relative;
  z-index: 1;
  padding: 0 0 1.5rem;
}

.home-map-section__panel {
  position: relative;
  min-height: calc(100vh - var(--header-height));
  min-height: calc(100dvh - var(--header-height));
  margin: 0;
  border-radius: 0;
  border-left: 0;
  border-right: 0;
  overflow: hidden;
}

.home-map-section__panel::after {
  content: "";
  position: absolute;
  inset: 0;
  box-shadow: inset 0 0 0 1px rgba(243, 239, 230, 0.12);
  pointer-events: none;
}

.home-map-section__inner {
  position: relative;
  min-height: inherit;
  padding: 0;
}

.home-map-section__content {
  position: relative;
  z-index: 2;
  display: grid;
  align-content: center;
  gap: 1.35rem;
  width: min(54%, 73rem);
  min-height: inherit;
  padding: clamp(2rem, 5vh, 3.4rem) 1.2rem clamp(2rem, 5vh, 3.4rem)
    max(1.2rem, calc((100% - var(--content-width)) / 2 + 1rem));
  pointer-events: auto;
}

.home-map-section__content::before {
  content: "";
  position: absolute;
  inset: 0;
  right: -8rem;
  z-index: -1;
  background: linear-gradient(
    90deg,
    rgba(6, 10, 15, 0.94) 0%,
    rgba(6, 10, 15, 0.84) 48%,
    rgba(6, 10, 15, 0.42) 76%,
    rgba(6, 10, 15, 0) 100%
  );
  pointer-events: none;
}

.home-map-section__intro {
  max-width: 30rem;
  user-select: text;
}

.home-map-section__title {
  margin: 0.35rem 0 0.7rem;
  font-size: clamp(2rem, 4vw, 3.4rem);
  line-height: 0.98;
  max-width: 12ch;
}

.home-map-section__text {
  max-width: 40rem;
  margin: 0;
  color: var(--text-soft);
  font-size: 1rem;
  line-height: 1.7;
}

.home-map-section__note {
  max-width: 38rem;
  margin: 0;
  color: rgba(243, 239, 230, 0.62);
  font-size: 0.9rem;
  line-height: 1.55;
}

.home-map-section__stats {
  display: grid;
  gap: 0.9rem;
  max-width: 22rem;
  pointer-events: auto;
}

.home-map-section__viewport {
  position: absolute;
  inset: 0;
  min-height: 0;
}

.home-view__section {
  position: relative;
  z-index: 1;
}

.home-view__section:first-of-type {
  margin-top: 0;
}

.home-story-strip {
  display: grid;
  gap: 1.25rem;
}

.home-story-strip__title {
  font-size: clamp(1.8rem, 3vw, 2.5rem);
  margin-bottom: 0.7rem;
}

.home-story-strip__grid {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.home-story-strip__bullets {
  display: grid;
  gap: 0.72rem;
  padding-top: 0.35rem;
}

.home-overview__map {
  position: absolute;
  inset: 0;
  overflow: hidden;
  border-radius: inherit;
  background: rgba(5, 10, 16, 0.72);
}

.ngulia-marker-overlay {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 7;
  display: block;
  width: 1.3rem;
  height: 1.3rem;
  padding: 0;
  transform: translate(-50%, -50%);
  pointer-events: auto;
}

.ngulia-marker-overlay__button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.3rem;
  height: 1.3rem;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.ngulia-marker-overlay__button:focus-visible {
  outline: 2px solid rgba(255, 217, 120, 0.72);
  outline-offset: 3px;
}

.ngulia-marker-overlay__dot {
  display: block;
  width: 0.82rem;
  height: 0.82rem;
  border: 2px solid #ffffff;
  border-radius: 999px;
  background: #e34b4b;
  box-shadow:
    0 0 0 4px rgba(227, 75, 75, 0.22),
    0 0 18px rgba(255, 217, 120, 0.42);
}

.ngulia-marker-overlay__popup {
  position: absolute;
  left: 50%;
  bottom: calc(100% + 0.55rem);
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 0.42rem;
  padding: 0.32rem 0.58rem;
  border: 1px solid rgba(243, 239, 230, 0.14);
  border-radius: 999px;
  background: rgba(12, 18, 27, 0.92);
  color: var(--text);
  font-size: 0.78rem;
  line-height: 1;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.24);
  backdrop-filter: blur(12px);
  pointer-events: auto;
  white-space: nowrap;
}

.ngulia-marker-overlay__popup::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 100%;
  width: 0.55rem;
  height: 0.55rem;
  background: rgba(12, 18, 27, 0.92);
  border-right: 1px solid rgba(243, 239, 230, 0.14);
  border-bottom: 1px solid rgba(243, 239, 230, 0.14);
  transform: translate(-50%, -50%) rotate(45deg);
}

.ngulia-marker-overlay__direction {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.35rem;
  height: 1.35rem;
  border-radius: 999px;
  color: var(--accent-soft);
  background: rgba(255, 217, 120, 0.08);
  border: 1px solid rgba(255, 217, 120, 0.18);
}

.ngulia-marker-overlay__direction svg {
  width: 0.72rem;
  height: 0.72rem;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
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
    linear-gradient(180deg, rgba(17, 24, 34, 0.95), rgba(8, 13, 19, 0.88)), rgba(7, 12, 18, 0.82);
  color: var(--text);
  box-shadow:
    0 8px 24px rgba(0, 0, 0, 0.22),
    inset 0 0 0 1px rgba(255, 217, 120, 0.04);
  backdrop-filter: blur(12px);
  transition:
    transform 160ms ease,
    border-color 160ms ease,
    background 160ms ease;
}

.map-controls__button:hover {
  transform: translateY(-1px);
  border-color: rgba(255, 217, 120, 0.36);
  background:
    linear-gradient(180deg, rgba(25, 34, 47, 0.97), rgba(10, 16, 24, 0.92)), rgba(7, 12, 18, 0.9);
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

.migration-controls {
  position: absolute;
  top: 6.8rem;
  right: 0.9rem;
  width: min(24rem, calc(100% - 1.8rem));
  z-index: 5;
  display: grid;
  gap: 0.62rem;
  padding: 0.85rem;
  border: 1px solid rgba(243, 239, 230, 0.14);
  border-radius: 0.8rem;
  background: rgba(7, 12, 18, 0.76);
  backdrop-filter: blur(12px);
}

.migration-controls label {
  display: grid;
  gap: 0.32rem;
  min-width: 0;
  color: var(--text-soft);
  font-size: 0.76rem;
}

.migration-controls select,
.migration-controls input {
  width: 100%;
}

.migration-controls select {
  min-height: 2.15rem;
  border: 1px solid rgba(243, 239, 230, 0.16);
  border-radius: 0.55rem;
  background: rgba(255, 255, 255, 0.06);
  color: var(--text);
  padding: 0.42rem 0.55rem;
  font-size: 0.78rem;
}

.migration-controls input[type="range"] {
  accent-color: var(--accent-soft);
}

.migration-controls__row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.7rem;
}

.migration-controls__row--split {
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
}

.migration-controls__row--single {
  grid-template-columns: 1fr;
}

.migration-controls__meta {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.4rem;
  color: var(--text-soft);
  font-size: 0.78rem;
}

.migration-controls__meta strong {
  color: var(--accent-soft);
  font-size: 1rem;
}

:deep(.mapboxgl-map) {
  border-radius: inherit;
}

:deep(.mapboxgl-canvas-container) {
  border-radius: inherit;
  overflow: hidden;
}

:deep(.mapboxgl-canvas) {
  border-radius: inherit;
}

:deep(.mapboxgl-popup-content) {
  background: #0f1620;
  color: #f3efe6;
  border-radius: 0.8rem;
  box-shadow: 0 18px 44px rgba(0, 0, 0, 0.28);
}

:deep(.mapboxgl-popup-tip) {
  border-top-color: #0f1620 !important;
}

.home-hero__scroll-cue {
  position: absolute;
  left: 0;
  bottom: clamp(1.3rem, 4vh, 2.6rem);
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  color: rgba(243, 239, 230, 0.82);
  font-size: 0.82rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.home-hero__scroll-cue::after {
  content: "";
  width: 2.8rem;
  height: 1px;
  background: linear-gradient(90deg, rgba(255, 217, 120, 0.88), rgba(255, 217, 120, 0));
}

@media (max-width: 980px) {
  .home-background__beam {
    bottom: -24rem;
    width: min(66rem, 126vw);
    height: 74rem;
  }

  .home-map-section__intro {
    padding-top: 1.35rem;
  }

  .home-map-section__content {
    width: min(60%, 34rem);
    padding-right: 1rem;
  }
}

@media (max-width: 640px) {
  .home-hero {
    min-height: calc(100svh - var(--header-height));
  }

  .hero-controls {
    right: 0.75rem;
  }

  .hero-settings {
    left: 0.75rem;
    right: 0.75rem;
    width: auto;
    top: 4rem;
  }

  .home-background__beam {
    bottom: -22rem;
    width: min(46rem, 144vw);
    height: 66rem;
    filter: blur(28px);
  }

  .home-map-section__panel {
    min-height: max(44rem, calc(100svh - var(--header-height)));
  }

  .home-map-section__inner,
  .home-map-section__viewport {
    min-height: calc(100svh - var(--header-height));
  }

  .home-hero__title {
    max-width: 9ch;
  }

  .home-hero__intro {
    font-size: 1rem;
    line-height: 1.7;
  }

  .home-hero__copy {
    padding-bottom: 2.8rem;
  }

  .home-overview__map {
    min-height: auto;
  }

  .home-map-section__content {
    width: 100%;
    min-height: inherit;
    align-content: start;
    padding: 1rem 0.75rem 13rem;
  }

  .home-map-section__content::before {
    right: 0;
    bottom: auto;
    height: 68%;
    background: linear-gradient(
      180deg,
      rgba(6, 10, 15, 0.94) 0%,
      rgba(6, 10, 15, 0.82) 56%,
      rgba(6, 10, 15, 0.24) 86%,
      rgba(6, 10, 15, 0) 100%
    );
  }

  .home-map-section__intro {
    padding-top: 0;
  }

  .home-map-section__title {
    max-width: 10ch;
  }

  .home-map-section__stats {
    max-width: 100%;
  }

  .migration-controls {
    left: 0.55rem;
    right: 0.55rem;
    top: auto;
    bottom: 0.55rem;
    width: auto;
    max-height: min(48svh, 26rem);
    overflow: auto;
    gap: 0.48rem;
    padding: 0.62rem;
  }

  .map-controls {
    top: 0.55rem;
    right: 0.55rem;
  }

  .migration-controls__row,
  .migration-controls__row--split {
    grid-template-columns: 1fr;
  }

  .home-hero__scroll-cue {
    left: 0.75rem;
    bottom: 1.1rem;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
  }
}
</style>
