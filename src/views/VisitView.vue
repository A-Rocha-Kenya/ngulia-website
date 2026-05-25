<template>
  <section class="page visit-page">
    <div class="section-label">Participate / Visit &amp; Volunteer</div>
    <h1 class="page-title">Come to Ngulia</h1>
    <p class="page-intro">
      This page combines simple visits, volunteer participation, and training interest in one
      place. Ngulia works best when every visit is planned around the field season, the needs of
      the researchers, and the long-term goal of building Kenyan ringing capacity.
    </p>

    <section class="visit-hero">
      <article class="panel visit-hero__story">
        <div class="panel-inner">
          <div class="eyebrow">Start here</div>
          <p class="visit-hero__lead">
            Do not arrive unannounced. Contact the team first, explain why you want to come, and
            be clear whether you are asking for a short visit, a volunteer role, or a training
            opportunity.
          </p>
          <p class="muted">
            The main season is usually November to December around the best moon and mist
            conditions. Some visits are simple introductions to the site. Others are working
            visits, with night catches, dawn net rounds, ringing table support, and long,
            irregular hours. The team needs people who strengthen the operation, not people who
            add uncertainty at the busiest moments.
          </p>
          <div class="visit-pill-row">
            <span v-for="item in heroPills" :key="item" class="pill">{{ item }}</span>
          </div>
          <div class="visit-contact-card">
            <div>
              <strong>Primary contact</strong>
              <p>Colin Jackson coordinates current Ngulia field organisation and is the right first contact for visits, volunteering, and training enquiries.</p>
            </div>
            <a class="button-link" :href="contactEmailHref">Email Colin Jackson</a>
          </div>
        </div>
      </article>

      <article class="panel visit-map-card">
        <div ref="mapRef" class="visit-map"></div>
      </article>
    </section>

    <section class="stats-grid visit-stats">
      <StatCard
        v-for="fact in headlineFacts"
        :key="fact.label"
        :label="fact.label"
        :value="fact.value"
        :description="fact.description"
      />
    </section>

    <section class="visit-section">
      <div class="section-label">Before you ask</div>
      <div class="visit-grid visit-grid--two">
        <article class="panel">
          <div class="panel-inner">
            <h2 class="panel-title">Who this page is for</h2>
            <ul class="bullets">
              <li>Visitors who want a short, coordinated introduction to the site and the project.</li>
              <li>Experienced ringers and extractors who can contribute directly to a field session.</li>
              <li>Scribes or support volunteers who are calm, accurate, and happy with repetitive but important work.</li>
              <li>Kenyan ringers in training, and experienced visitors who can support that training model appropriately.</li>
            </ul>
          </div>
        </article>

        <article class="panel">
          <div class="panel-inner">
            <h2 class="panel-title">What to include in your first email</h2>
            <ul class="bullets">
              <li>Your full name, organisation, and country.</li>
              <li>The dates you hope to come and how flexible those dates are.</li>
              <li>Whether you are proposing a simple visit, a volunteer role, or a training placement.</li>
              <li>Your ringing, extraction, bird handling, scribing, driving, or field-camp experience.</li>
              <li>Any constraints that affect logistics, accommodation, transport, or schedule.</li>
            </ul>
          </div>
        </article>
      </div>
    </section>

    <section class="visit-section">
      <div class="section-label">Practical plan</div>
      <div class="visit-plan-grid">
        <article v-for="card in planningCards" :key="card.title" class="panel">
          <div class="panel-inner">
            <div class="eyebrow">{{ card.eyebrow }}</div>
            <h2 class="panel-title">{{ card.title }}</h2>
            <p class="muted">{{ card.text }}</p>
          </div>
        </article>
      </div>
    </section>

    <section class="visit-section">
      <div class="section-label">What to expect</div>
      <div class="visit-grid visit-grid--story">
        <article class="panel">
          <div class="panel-inner">
            <h2 class="panel-title">The best visits are built around field reality</h2>
            <p class="muted">
              Some nights are spectacular. Others are quiet, wet, windy, or logistically awkward.
              A productive Ngulia session depends on moon, mist, rain, manpower and the timing of
              migration. Even during a strong season, there is no guaranteed spectacle on demand.
            </p>
            <p class="muted">
              If you come during the core season, expect late nights, pre-dawn activity, dust,
              uneven sleep, and stretches of patient waiting. Also expect one of the most striking
              migration settings in Africa: lodge lights below the ridge, grounded migrants in the
              bushes at dawn, and in some years visible daytime passage of rollers, bee-eaters,
              falcons and eagles.
            </p>
          </div>
        </article>

        <article class="panel">
          <div class="panel-inner">
            <div class="eyebrow">Bring with you</div>
            <h2 class="panel-title">Personal kit that helps</h2>
            <ul class="bullets">
              <li>Neutral field clothing for hot days and surprisingly cool late nights.</li>
              <li>A headlamp, notebook, water bottle, closed shoes, and basic personal medication.</li>
              <li>Binoculars for daytime watching, and patience for nights when the weather does not deliver.</li>
              <li>If volunteering as a ringer, bring your own licences, experience summary, and any essentials you normally rely on in the field.</li>
            </ul>
          </div>
        </article>
      </div>
    </section>

    <section class="visit-section">
      <div class="section-label">Roles and contribution</div>
      <div class="visit-grid visit-grid--two">
        <article class="panel">
          <div class="panel-inner">
            <div class="eyebrow">Most valuable help</div>
            <h2 class="panel-title">What genuinely strengthens the project</h2>
            <ul class="bullets">
              <li>Experienced ringers and extractors who can work safely and independently under pressure.</li>
              <li>Careful scribes who write clearly, stay focused, and keep the ringing table moving.</li>
              <li>Visitors who are flexible, self-sufficient, and realistic about changing field conditions.</li>
              <li>People who help train, mentor, or support Kenyan ringers without dominating the work.</li>
              <li>Advance coordination on transport, lodge arrangements, permits, and timing.</li>
            </ul>
          </div>
        </article>

        <article class="panel">
          <div class="panel-inner">
            <div class="eyebrow">What becomes a burden</div>
            <h2 class="panel-title">Common ways to make life harder for the team</h2>
            <ul class="bullets">
              <li>Turning up without prior agreement, or assuming the team can absorb extra people during a heavy catch.</li>
              <li>Expecting a tourism schedule when the work is organised around weather and migration.</li>
              <li>Needing intensive one-to-one training on peak nights when experienced hands are already stretched.</li>
              <li>Creating avoidable logistics problems through vague timing, special requests, or poor communication.</li>
              <li>Seeing Kenyan trainees as secondary to visiting volunteers rather than central to the long-term model.</li>
            </ul>
          </div>
        </article>
      </div>
    </section>

    <section class="visit-section">
      <div class="section-label">Training model</div>
      <div class="visit-grid visit-grid--story">
        <article class="panel">
          <div class="panel-inner">
            <h2 class="panel-title">Kenyan ringer training should be explicit</h2>
            <p class="muted">
              Ngulia is not only a place to host outside visitors. It should also function as a
              training ground for Kenyan ringers and field ornithologists. The best participation
              model is therefore not simply “extra hands”, but a structured mix of experienced
              organisers, capable visitors, scribes, and Kenyan trainees who can develop real
              competence over repeated seasons.
            </p>
            <p class="muted">
              That means the page should be read in a particular way: if you are highly
              experienced, ask how you can contribute without displacing local training. If you are
              earlier in your development, be open to support roles first. If you are interested in
              Kenyan capacity building, say so clearly in your enquiry.
            </p>
          </div>
        </article>

        <article class="panel">
          <div class="panel-inner">
            <div class="eyebrow">Good fit</div>
            <h2 class="panel-title">Who fits this model best</h2>
            <ul class="bullets">
              <li>Kenyan trainees seeking ringing and field-season experience in a serious migration setting.</li>
              <li>Skilled visiting ringers who are comfortable teaching by example and working within an existing local structure.</li>
              <li>Support volunteers who understand that data quality, safe handling, and team rhythm matter more than novelty.</li>
              <li>Researchers whose visit has a clear purpose and does not compete with core field operations.</li>
            </ul>
          </div>
        </article>
      </div>
    </section>

    <section class="visit-section">
      <article class="panel visit-closing">
        <div class="panel-inner">
          <div class="eyebrow">Contact and next step</div>
          <h2 class="panel-title">If you want to come</h2>
          <p class="muted">
            Start with an email, not a travel booking. Explain what role you have in mind, when
            you hope to come, and what level of experience you bring. The team can then advise
            whether a short visit, a volunteer role, or a training-focused placement makes sense in
            that season.
          </p>
          <div class="visit-actions">
            <a class="button-link" :href="contactEmailHref">Contact Colin Jackson</a>
            <RouterLink class="button-link" to="/about/team">See the team</RouterLink>
          </div>
        </div>
      </article>
    </section>
  </section>
</template>

<script setup>
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import StatCard from '../components/StatCard.vue'

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN || ''

const contactEmail = 'colin.jackson@arocha.org'
const contactEmailHref = `mailto:${contactEmail}?subject=Ngulia%20visit%20or%20volunteer%20enquiry`
const NGULIA_COORDS = [38.211134674309974, -3.0140288001023605]

const heroPills = ['Visit', 'Volunteer', 'Training', 'Ngulia Lodge', 'Tsavo West']

const headlineFacts = [
  {
    label: 'Best season',
    value: 'Nov-Dec',
    description: 'Plan around the core late-autumn ringing period and the best moon and mist conditions.'
  },
  {
    label: 'Main base',
    value: 'Ngulia Lodge',
    description: 'The work is centred on the lodge, the floodlit area, and the nearby dawn netting ground.'
  },
  {
    label: 'First contact',
    value: 'Email first',
    description: 'Visits work best when dates, roles, and logistics are agreed in advance with the field organisers.'
  },
  {
    label: 'Best model',
    value: 'Train local',
    description: 'The long-term aim should include Kenyan ringer training and capacity building, not only outside participation.'
  }
]

const planningCards = [
  {
    eyebrow: 'Timing',
    title: 'Come for the right window',
    text:
      'The most useful timing is usually within the November to December field season, especially around the moon periods and weather windows that matter for migration. If your dates are rigid, say so early.'
  },
  {
    eyebrow: 'Getting there',
    title: 'Route and access need coordination',
    text:
      'Most visitors will approach from Nairobi by road toward Mtito Andei and then continue into Tsavo West toward Ngulia Lodge. Final route, park access, vehicle arrangements and arrival timing should be confirmed with the team before travel.'
  },
  {
    eyebrow: 'Stay',
    title: 'Accommodation is part of the field plan',
    text:
      'Lodge stay, food, costs, and any shared field arrangements need to be discussed in advance. Do not assume the team can improvise beds, transport, or field support at short notice.'
  },
  {
    eyebrow: 'Work rhythm',
    title: 'Expect irregular hours',
    text:
      'A strong night can mean work late into darkness, then again at dawn in the bushes and at the ringing table. Rest opportunities depend on the catch and the weather rather than on a fixed tourism-style schedule.'
  }
]

const mapRef = ref(null)
let map

onMounted(() => {
  map = new mapboxgl.Map({
    container: mapRef.value,
    style: 'mapbox://styles/mapbox/satellite-v9',
    center: [38.21970885934542, -2.995353445406323],
    zoom: 13.266892405903148,
    bearing: 26.400000000000432,
    pitch: 77.00000000000004,
    projection: 'globe',
    attributionControl: false
  })

  map.on('style.load', () => {
    map.setFog({
      color: 'rgb(7, 12, 18)',
      'high-color': 'rgb(20, 32, 46)',
      'horizon-blend': 0.1,
      'space-color': 'rgb(2, 5, 10)',
      'star-intensity': 0.45
    })

    map.addSource('visit-dem', {
      type: 'raster-dem',
      url: 'mapbox://mapbox.mapbox-terrain-dem-v1',
      tileSize: 512,
      maxzoom: 14
    })

    map.setTerrain({ source: 'visit-dem', exaggeration: 1.45 })

    new mapboxgl.Marker({ color: '#f2c14e', scale: 0.95 })
      .setLngLat(NGULIA_COORDS)
      .addTo(map)
  })
})

onBeforeUnmount(() => {
  if (map) map.remove()
})
</script>

<style scoped>
.visit-page {
  padding-bottom: 5rem;
}

.visit-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
  gap: 1.25rem;
  align-items: stretch;
  margin-top: 2rem;
}

.visit-hero__lead {
  margin: 0 0 1rem;
  font-size: 1.15rem;
  line-height: 1.65;
}

.visit-pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
  margin: 1.15rem 0;
}

.visit-contact-card {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: end;
  padding: 1rem 1.1rem;
  margin-top: 1.3rem;
  border-radius: 1.1rem;
  border: 1px solid rgba(242, 193, 78, 0.2);
  background: linear-gradient(180deg, rgba(242, 193, 78, 0.08), rgba(78, 167, 160, 0.08));
}

.visit-contact-card strong {
  display: block;
  margin-bottom: 0.35rem;
}

.visit-contact-card p {
  margin: 0;
  color: var(--text-soft);
  line-height: 1.6;
}

.visit-map-card {
  overflow: hidden;
  position: relative;
  min-height: 25rem;
}

.visit-map {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.visit-map::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at top, rgba(8, 12, 18, 0) 0%, rgba(8, 12, 18, 0.08) 52%, rgba(4, 7, 12, 0.42) 100%),
    linear-gradient(180deg, rgba(4, 7, 12, 0.04), rgba(4, 7, 12, 0.35));
}

.visit-stats {
  margin-top: 1.5rem;
}

.visit-section {
  margin-top: 3rem;
}

.visit-grid,
.visit-plan-grid {
  display: grid;
  gap: 1.25rem;
  margin-top: 1rem;
}

.visit-grid--two {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.visit-grid--story {
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.95fr);
}

.visit-plan-grid {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.visit-closing {
  position: relative;
  overflow: hidden;
}

.visit-closing::before {
  content: '';
  position: absolute;
  inset: auto 15% -4rem auto;
  width: 18rem;
  height: 18rem;
  background: radial-gradient(circle, rgba(242, 193, 78, 0.14), rgba(242, 193, 78, 0));
  pointer-events: none;
}

.visit-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  margin-top: 1.25rem;
}

@media (max-width: 1020px) {
  .visit-hero,
  .visit-grid--two,
  .visit-grid--story {
    grid-template-columns: 1fr;
  }

  .visit-map-card__body {
    min-height: 21rem;
  }
}

@media (max-width: 700px) {
  .visit-contact-card {
    flex-direction: column;
    align-items: start;
  }

  .visit-map-card {
    min-height: 20rem;
  }
}
</style>
