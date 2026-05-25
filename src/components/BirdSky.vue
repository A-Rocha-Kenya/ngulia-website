<template>
  <div class="bird-sky" aria-hidden="true" :style="birdSkyStyle">
    <span
      v-for="bird in birds"
      :key="bird.id"
      class="bird-sky__bird"
      :class="{ 'bird-sky__bird--active': bird.active }"
      :style="bird.style"
      @animationend="handleFlightEnd(bird.id)"
    ></span>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive } from 'vue'

const REFERENCE_VIEWPORT_WIDTH = 1280
const REFERENCE_VIEWPORT_HEIGHT = 800

const props = defineProps({
  settings: {
    type: Object,
    default: () => ({})
  }
})

const birdPresets = [
  { id: 1, style: { top: '12%', left: '8%', '--bird-size': '18px', '--bird-duration': '2.9s', '--bird-x': '18vw', '--bird-y': '6vh', '--bird-dip-x': '9vw', '--bird-dip-y': '4vh', '--bird-scale': '1.2', '--bird-opacity': '0.4', '--bird-tilt': '-8deg' } },
  { id: 2, style: { top: '22%', left: '20%', '--bird-size': '26px', '--bird-duration': '2.7s', '--bird-x': '22vw', '--bird-y': '-8vh', '--bird-dip-x': '11vw', '--bird-dip-y': '3vh', '--bird-scale': '1.45', '--bird-opacity': '0.58', '--bird-tilt': '3deg' } },
  { id: 3, style: { top: '15%', left: '42%', '--bird-size': '14px', '--bird-duration': '2.8s', '--bird-x': '14vw', '--bird-y': '10vh', '--bird-dip-x': '7vw', '--bird-dip-y': '5vh', '--bird-scale': '1.1', '--bird-opacity': '0.34', '--bird-tilt': '-12deg' } },
  { id: 4, style: { top: '28%', left: '58%', '--bird-size': '30px', '--bird-duration': '2.6s', '--bird-x': '26vw', '--bird-y': '-10vh', '--bird-dip-x': '13vw', '--bird-dip-y': '2vh', '--bird-scale': '1.5', '--bird-opacity': '0.62', '--bird-tilt': '10deg' } },
  { id: 5, style: { top: '18%', left: '76%', '--bird-size': '16px', '--bird-duration': '2.9s', '--bird-x': '20vw', '--bird-y': '7vh', '--bird-dip-x': '9vw', '--bird-dip-y': '4vh', '--bird-scale': '1.16', '--bird-opacity': '0.38', '--bird-tilt': '-5deg' } },
  { id: 6, style: { top: '42%', left: '12%', '--bird-size': '24px', '--bird-duration': '2.6s', '--bird-x': '24vw', '--bird-y': '-6vh', '--bird-dip-x': '12vw', '--bird-dip-y': '2vh', '--bird-scale': '1.34', '--bird-opacity': '0.5', '--bird-tilt': '6deg' } },
  { id: 7, style: { top: '50%', left: '34%', '--bird-size': '12px', '--bird-duration': '2.5s', '--bird-x': '16vw', '--bird-y': '5vh', '--bird-dip-x': '8vw', '--bird-dip-y': '3vh', '--bird-scale': '1.08', '--bird-opacity': '0.3', '--bird-tilt': '-10deg' } },
  { id: 8, style: { top: '46%', left: '64%', '--bird-size': '28px', '--bird-duration': '2.5s', '--bird-x': '28vw', '--bird-y': '-12vh', '--bird-dip-x': '15vw', '--bird-dip-y': '1vh', '--bird-scale': '1.58', '--bird-opacity': '0.64', '--bird-tilt': '12deg' } },
  { id: 9, style: { top: '56%', left: '80%', '--bird-size': '20px', '--bird-duration': '2.8s', '--bird-x': '18vw', '--bird-y': '8vh', '--bird-dip-x': '9vw', '--bird-dip-y': '3vh', '--bird-scale': '1.22', '--bird-opacity': '0.42', '--bird-tilt': '-4deg' } },
  { id: 10, style: { top: '34%', left: '30%', '--bird-size': '22px', '--bird-duration': '2.7s', '--bird-x': '19vw', '--bird-y': '-7vh', '--bird-dip-x': '10vw', '--bird-dip-y': '2vh', '--bird-scale': '1.28', '--bird-opacity': '0.48', '--bird-tilt': '7deg' } },
  { id: 11, style: { top: '10%', left: '68%', '--bird-size': '13px', '--bird-duration': '2.9s', '--bird-x': '15vw', '--bird-y': '9vh', '--bird-dip-x': '7vw', '--bird-dip-y': '5vh', '--bird-scale': '1.06', '--bird-opacity': '0.28', '--bird-tilt': '-14deg' } },
  { id: 12, style: { top: '60%', left: '52%', '--bird-size': '27px', '--bird-duration': '2.6s', '--bird-x': '25vw', '--bird-y': '-9vh', '--bird-dip-x': '13vw', '--bird-dip-y': '1vh', '--bird-scale': '1.52', '--bird-opacity': '0.6', '--bird-tilt': '9deg' } }
]

const birds = reactive(
  birdPresets.map((bird) => ({
    id: bird.id,
    baseStyle: bird.style,
    style: bird.style,
    active: false
  }))
)

const timers = new Map()
let burstTimer = null
let burstUntil = 0

const resolvedSettings = computed(() => ({
  baseDelayMin: props.settings.baseDelayMin ?? 900,
  baseDelayMax: props.settings.baseDelayMax ?? 3100,
  burstMinCount: props.settings.burstMinCount ?? 5,
  burstMaxCount: props.settings.burstMaxCount ?? 8,
  burstDelayMin: props.settings.burstDelayMin ?? 80,
  burstDelayMax: props.settings.burstDelayMax ?? 420,
  burstDurationMin: props.settings.burstDurationMin ?? 3000,
  burstDurationMax: props.settings.burstDurationMax ?? 4600,
  burstPauseMin: props.settings.burstPauseMin ?? 8500,
  burstPauseMax: props.settings.burstPauseMax ?? 12500,
  startJitter: props.settings.startJitter ?? 1.5,
  endJitter: props.settings.endJitter ?? 3.2,
  topJitter: props.settings.topJitter ?? 2.5,
  durationJitter: props.settings.durationJitter ?? 0.12,
  lowerFadeStart: props.settings.lowerFadeStart ?? 62,
  lowerFadeEnd: props.settings.lowerFadeEnd ?? 100
}))

const birdSkyStyle = computed(() => {
  const fadeStart = resolvedSettings.value.lowerFadeStart
  const fadeEnd = resolvedSettings.value.lowerFadeEnd
  const fadeMid = Math.min(fadeEnd - 4, fadeStart + 12)
  return {
    '--bird-unit-x': `max(1vw, ${(REFERENCE_VIEWPORT_WIDTH / 100).toFixed(2)}px)`,
    '--bird-unit-y': `max(1vh, ${(REFERENCE_VIEWPORT_HEIGHT / 100).toFixed(2)}px)`,
    '--bird-fade-start': `${fadeStart}%`,
    '--bird-fade-mid': `${fadeMid}%`,
    '--bird-fade-end': `${fadeEnd}%`
  }
})

function randomBetween(min, max) {
  return Math.round(min + Math.random() * (max - min))
}

function randomInt(min, max) {
  return Math.floor(min + Math.random() * (max - min + 1))
}

function randomFloat(min, max) {
  return min + Math.random() * (max - min)
}

function parseCssNumber(value) {
  return Number.parseFloat(value)
}

function toFlightDistance(value, axis) {
  return `calc(${value.toFixed(2)} * var(${axis === 'x' ? '--bird-unit-x' : '--bird-unit-y'}))`
}

function buildFlightStyle(baseStyle) {
  const settings = resolvedSettings.value
  const top = parseCssNumber(baseStyle.top)
  const left = parseCssNumber(baseStyle.left)
  const x = parseCssNumber(baseStyle['--bird-x'])
  const y = parseCssNumber(baseStyle['--bird-y'])
  const duration = parseCssNumber(baseStyle['--bird-duration'])
  const tilt = parseCssNumber(baseStyle['--bird-tilt'])

  return {
    ...baseStyle,
    top: `${(top + randomFloat(-settings.topJitter, settings.topJitter)).toFixed(2)}%`,
    left: `${(left + randomFloat(-settings.topJitter, settings.topJitter)).toFixed(2)}%`,
    '--bird-duration': `${Math.max(2.35, duration + randomFloat(-settings.durationJitter, settings.durationJitter)).toFixed(2)}s`,
    '--bird-start-x': toFlightDistance(-10 + randomFloat(-settings.startJitter, settings.startJitter), 'x'),
    '--bird-start-y': toFlightDistance(12 + randomFloat(-settings.startJitter * 1.33, settings.startJitter * 1.33), 'y'),
    '--bird-end-x': toFlightDistance(x + randomFloat(-settings.endJitter, settings.endJitter), 'x'),
    '--bird-end-y': toFlightDistance(y + randomFloat(-settings.endJitter, settings.endJitter), 'y'),
    '--bird-tilt-end': `${(tilt + randomFloat(3.5, 5.5)).toFixed(2)}deg`
  }
}

function inBurst() {
  return Date.now() < burstUntil
}

function nextSpawnDelay() {
  const settings = resolvedSettings.value
  if (inBurst()) {
    return randomBetween(settings.burstDelayMin, settings.burstDelayMax)
  }

  const skew = 1 - Math.pow(Math.random(), 1.8)
  return Math.round(settings.baseDelayMin + skew * Math.max(0, settings.baseDelayMax - settings.baseDelayMin))
}

function clearBirdTimer(id) {
  const timer = timers.get(id)
  if (timer) {
    window.clearTimeout(timer)
    timers.delete(id)
  }
}

function scheduleBird(id, delay = nextSpawnDelay()) {
  clearBirdTimer(id)
  timers.set(
    id,
    window.setTimeout(() => {
      startBird(id)
    }, delay)
  )
}

function startBird(id) {
  const bird = birds.find((entry) => entry.id === id)
  if (!bird || bird.active) {
    return
  }

  bird.style = buildFlightStyle(bird.baseStyle)
  bird.active = false

  requestAnimationFrame(() => {
    bird.active = true
  })
}

function scheduleBurst() {
  const settings = resolvedSettings.value
  burstTimer = window.setTimeout(() => {
    burstUntil = Date.now() + randomBetween(settings.burstDurationMin, settings.burstDurationMax)

    const inactiveBirds = birds.filter((bird) => !bird.active)
    const burstCount = Math.min(inactiveBirds.length, randomInt(settings.burstMinCount, settings.burstMaxCount))

    inactiveBirds
      .sort(() => Math.random() - 0.5)
      .slice(0, burstCount)
      .forEach((bird) => {
        scheduleBird(bird.id, randomBetween(0, settings.burstDelayMax))
      })

    scheduleBurst()
  }, randomBetween(settings.burstPauseMin, settings.burstPauseMax))
}

function handleFlightEnd(id) {
  const bird = birds.find((entry) => entry.id === id)
  if (!bird) {
    return
  }

  bird.active = false
  scheduleBird(id)
}

onMounted(() => {
  birds.forEach((bird) => {
    scheduleBird(bird.id, randomBetween(0, Math.max(1200, resolvedSettings.value.baseDelayMax)))
  })

  scheduleBurst()
})

onBeforeUnmount(() => {
  timers.forEach((timer) => window.clearTimeout(timer))
  timers.clear()

  if (burstTimer) {
    window.clearTimeout(burstTimer)
  }
})
</script>

<style scoped>
.bird-sky {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  mask-image: linear-gradient(180deg, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 1) var(--bird-fade-start), rgba(0, 0, 0, 0.72) var(--bird-fade-mid), rgba(0, 0, 0, 0.12) var(--bird-fade-end));
  -webkit-mask-image: linear-gradient(180deg, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 1) var(--bird-fade-start), rgba(0, 0, 0, 0.72) var(--bird-fade-mid), rgba(0, 0, 0, 0.12) var(--bird-fade-end));
}

.bird-sky__bird {
  position: absolute;
  width: calc(var(--bird-size) * 2.3);
  height: calc(var(--bird-size) * 0.9);
  opacity: 0;
  filter: blur(0.2px);
  transform: rotate(var(--bird-tilt));
  will-change: transform, opacity;
}

.bird-sky__bird--active {
  animation: fly-through var(--bird-duration) linear 1;
}

.bird-sky__bird::before,
.bird-sky__bird::after {
  content: '';
  position: absolute;
  top: 32%;
  width: 54%;
  height: 52%;
  border-top: max(2px, calc(var(--bird-size) * 0.13)) solid rgba(243, 239, 230, 0.8);
  border-radius: 100% 100% 0 0;
}

.bird-sky__bird::before {
  left: -2%;
  transform: rotate(-16deg);
  transform-origin: right center;
}

.bird-sky__bird::after {
  right: -2%;
  transform: rotate(16deg);
  transform-origin: left center;
}

@keyframes fly-through {
  0% {
    transform: translate3d(var(--bird-start-x), var(--bird-start-y), 0) scale(0.72) rotate(var(--bird-tilt));
    opacity: 0;
  }
  14% {
    opacity: var(--bird-opacity);
  }
  82% {
    opacity: calc(var(--bird-opacity) * 1.06);
  }
  100% {
    transform: translate3d(var(--bird-end-x), var(--bird-end-y), 0) scale(var(--bird-scale)) rotate(var(--bird-tilt-end));
    opacity: 0;
  }
}
</style>
