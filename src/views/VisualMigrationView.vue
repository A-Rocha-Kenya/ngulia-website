<template>
  <section class="page vimig-page">
    <div class="section-label">Science / Visible migration</div>
    <h1 class="page-title">Vimig at Ngulia</h1>
    <p class="page-intro">
      Ngulia is famous for misty nights when the lodge lights bring down nocturnal migrants.
      The same site also has a strong daytime story: rollers streaming down the valley,
      falcons moving in weather fronts, and a steady cast of eagles, buzzards, hawks and
      bee-eaters crossing the escarpment.
    </p>

    <section class="vimig-hero">
      <figure class="panel vimig-photo-card">
        <img :src="publicAsset('species-photos/eurasian-roller.jpg')" alt="Eurasian Roller photographed for the Ngulia website." />
        <figcaption>
          Eurasian Roller is one of the clearest visible migrants at Ngulia, often seen in
          loose flocks passing the valley in the morning, especially in early December.
        </figcaption>
      </figure>

      <article class="panel">
        <div class="panel-inner">
          <div class="eyebrow">Page focus</div>
          <p class="vimig-hero__lead">
            This page is about birds you can watch moving past Ngulia in daylight, not only the
            birds handled in the nets.
          </p>
          <p class="muted">
            The published Ngulia overview treats visible migration as a secondary thread beside
            the famous light-attraction phenomenon. The annual binders, however, show that the
            escarpment has repeatedly produced memorable daytime movements, especially of rollers,
            falcons and mixed raptor passage.
          </p>
          <div class="vimig-pill-row">
            <span v-for="item in heroPills" :key="item" class="pill">{{ item }}</span>
          </div>
          <ul class="bullets vimig-hero__bullets">
            <li v-for="item in heroBullets" :key="item">{{ item }}</li>
          </ul>
        </div>
      </article>
    </section>

    <section class="stats-grid vimig-stats">
      <StatCard
        v-for="fact in headlineFacts"
        :key="fact.label"
        :label="fact.label"
        :value="fact.value"
        :description="fact.description"
      />
    </section>

    <section class="vimig-section">
      <div class="section-label">What the documents say</div>
      <div class="vimig-source-grid">
        <article v-for="source in sourceCards" :key="source.title" class="panel">
          <div class="panel-inner">
            <div class="eyebrow">{{ source.eyebrow }}</div>
            <h2 class="panel-title">{{ source.title }}</h2>
            <p class="muted">{{ source.text }}</p>
          </div>
        </article>
      </div>
    </section>

    <section class="vimig-section">
      <div class="section-label">Why Ngulia works</div>
      <div class="vimig-explainer">
        <article class="panel">
          <div class="panel-inner">
            <h2 class="panel-title">A second migration story beside the lights</h2>
            <p class="muted">
              The classic Ngulia story happens at night under mist, low cloud and moonless skies.
              Visible migration is different. It depends on the same escarpment landscape, the
              same repeated watch effort, and often the same unstable weather, but what the
              observer sees is movement through open air: birds passing the ridge, dropping into
              the valley, circling on rising air, or suddenly appearing in numbers after showers.
            </p>
            <p class="muted">
              That makes Ngulia remarkable in two ways at once. It is a place where migrants can
              be studied in the hand, but it is also a vantage point where some of the same
              migration can be watched as behaviour, flock movement and weather-driven spectacle.
            </p>
          </div>
        </article>

        <article class="panel">
          <div class="panel-inner">
            <div class="eyebrow">Typical conditions</div>
            <h2 class="panel-title">When visible migration stands out</h2>
            <ul class="bullets">
              <li>Early morning movements of rollers and bee-eaters down the valley, often strongest in early December.</li>
              <li>Falcon passage after storms or showers, sometimes with birds dropping low around the lodge or roosting in the valley.</li>
              <li>Mixed raptor passage on clearer days, with Steppe Eagles, Lesser Spotted Eagles, Booted Eagles, Steppe Buzzards and Eurasian Sparrowhawks among the regular possibilities.</li>
              <li>Daytime hirundines and swifts when weather shifts, reminding observers that not all Ngulia migration is a night-light story.</li>
            </ul>
          </div>
        </article>

        <figure class="panel vimig-photo-card vimig-photo-card--secondary">
          <img :src="publicAsset('species-photos/barn-swallow.jpg')" alt="Barn Swallow photographed for the Ngulia website." />
          <figcaption>
            Hirundines are part of the daytime picture too. A Barn Swallow controlled at Ngulia
            carried a ring from Kazakhstan in the 2013 season update.
          </figcaption>
        </figure>
      </div>
    </section>

    <section class="vimig-section">
      <div class="section-label">Families on the move</div>
      <div class="vimig-family-grid">
        <article v-for="family in familyCards" :key="family.title" class="panel vimig-family-card">
          <div class="panel-inner">
            <div class="vimig-family-card__header">
              <div>
                <div class="eyebrow">{{ family.family }}</div>
                <h2 class="panel-title">{{ family.title }}</h2>
              </div>
              <div class="vimig-family-card__badge">
                <span>{{ family.recordValue }}</span>
                <small>{{ family.recordLabel }}</small>
              </div>
            </div>

            <p class="muted">{{ family.story }}</p>

            <div class="vimig-family-card__species">
              <div v-for="entry in family.species" :key="entry.name" class="vimig-species-note">
                <h3>{{ entry.name }}</h3>
                <p>{{ entry.note }}</p>
              </div>
            </div>
          </div>
        </article>
      </div>
      <p class="vimig-section__note">
        Counts and anecdotes on this page are drawn from the Ngulia binder reports and the
        published Ngulia review papers, with emphasis on notable visible-migration observations.
      </p>
    </section>

    <section class="vimig-section">
      <article class="panel vimig-closing">
        <div class="panel-inner">
          <div class="eyebrow">Page direction</div>
          <h2 class="panel-title">Keep this page human-scale</h2>
          <p class="muted">
            The strongest material here is not a giant spreadsheet of every overhead sighting. It
            is the combination of place, weather and memorable observations: the morning when
            rollers poured past in waves, the day when Amur Falcons seemed endless, and the
            decades of field notes showing that Ngulia is remarkable by day as well as by night.
          </p>
          <div class="vimig-actions">
            <RouterLink class="button-link" to="/about/history">Read the history</RouterLink>
            <RouterLink class="button-link" to="/science/publications">See publications</RouterLink>
          </div>
        </div>
      </article>
    </section>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import StatCard from '../components/StatCard.vue'
import { publicAsset } from '../lib/publicAsset'

const heroPills = ['Rollers', 'Falcons', 'Raptors', 'Bee-eaters', 'Hirundines']

const heroBullets = [
  'The main published literature is still weighted toward nocturnal light attraction and ringing results.',
  'Visible migration appears most strongly in the annual reports, where weather, ridge watches and standout counts were noted day by day.',
  'Rollers and Amur Falcons provide the clearest high-count stories, while mixed raptor passage gives the site its variety.'
]

const headlineFacts = [
  {
    label: 'Amur Falcons',
    value: '26,000',
    description: 'Counted moving west over Ngulia on 27 November 2011 in about one and a half hours.'
  },
  {
    label: 'Eurasian Rollers',
    value: '>1,000',
    description: 'Counted passing south west of the ridge in under 20 minutes on 14 November 1980.'
  },
  {
    label: 'Amur Falcon roost',
    value: '1,500',
    description: 'Estimated gathering at the lodge and in the Ngulia valley after heavy showers on 1 December 2014.'
  },
  {
    label: 'Steppe Eagles',
    value: '43',
    description: 'Counted passing south on 14 November in one of the later binder reports.'
  }
]

const sourceCards = [
  {
    eyebrow: 'Published overview',
    title: 'The formal literature keeps vimig in the background',
    text:
      'The 1969-2012 Ngulia review makes clear that the site is defined first by nocturnal migrants drawn down in mist and rain under moonless conditions. Visible migration is acknowledged, especially for Eurasian Roller and some birds of prey, but it is not the central analytical thread of the paper.'
  },
  {
    eyebrow: 'Older Scopus reports',
    title: 'Rollers were already recognised as classic day migrants',
    text:
      'Earlier reports describe loose flocks of Eurasian Rollers moving south down the Ngulia valley, usually in early December, and note that storms can also put rollers into the trees around the lodge at night. That is an important bridge between the daytime and night-time Ngulia stories.'
  },
  {
    eyebrow: 'Annual binders',
    title: 'The binders hold the strongest stories',
    text:
      'The annual reports repeatedly record visible migration in a vivid, practical way: over 1000 rollers in minutes, 26 000 Amur Falcons on one morning, regular mixed raptor passage, and notes on how showers, thunderstorms and changing winds reshape what can be seen from the lodge.'
  }
]

const familyCards = [
  {
    family: 'Falconidae',
    title: 'Falcons',
    recordValue: '26,000',
    recordLabel: 'Amur Falcons, 27 November 2011',
    story:
      'Falcons are where Ngulia’s vimig story becomes dramatic. Amur Falcon passage is irregular enough to feel event-driven, but when conditions align the counts become unforgettable. Sooty Falcon and Eleonora’s Falcon add a pelagic, storm-edge feel to the escarpment watches.',
    species: [
      {
        name: 'Amur Falcon',
        note: 'The headline record is 26,000 moving west over the lodge on 27 November 2011, with binders calling it the largest ever recorded at Ngulia.'
      },
      {
        name: 'Sooty Falcon',
        note: 'Repeatedly noted in late November and early December, often during unsettled weather when birds are easier to watch low over the lodge.'
      },
      {
        name: 'Eleonora’s Falcon and Eurasian Hobby',
        note: 'These species recur in the reports as regular supporting characters within mixed falcon passage.'
      }
    ]
  },
  {
    family: 'Accipitridae',
    title: 'Eagles, buzzards and hawks',
    recordValue: '43',
    recordLabel: 'Steppe Eagles counted southbound',
    story:
      'Raptor passage at Ngulia is often described as varied rather than massive. That is part of the appeal. Steppe Eagles, Lesser Spotted Eagles, Booted Eagles, Steppe Buzzards, European Honey Buzzards and Eurasian Sparrowhawks all feature, with the occasional Greater Spotted, Imperial or Levant Sparrowhawk adding real surprise.',
    species: [
      {
        name: 'Steppe Eagle',
        note: 'The binders include a count of 43 passing south on 14 November, while other years mention daily tallies in the tens rather than the hundreds.'
      },
      {
        name: 'Lesser Spotted Eagle and Booted Eagle',
        note: 'These are among the most regular supporting migrants in mixed November passage, often noted alongside Steppe Buzzards and Honey Buzzards.'
      },
      {
        name: 'Eurasian Sparrowhawk and Levant Sparrowhawk',
        note: 'Sparrowhawks are scarcer but memorable; the reports treat photographed or ringed birds as genuine highlights.'
      }
    ]
  },
  {
    family: 'Coraciidae and Meropidae',
    title: 'Rollers and bee-eaters',
    recordValue: '>1,000',
    recordLabel: 'Eurasian Rollers in under 20 minutes',
    story:
      'If one family captures the feeling of morning vimig at Ngulia, it is this one. The reports repeatedly describe roller passage down the valley, often in early December, with Blue-cheeked and Eurasian Bee-eaters passing in smaller but regular groups.',
    species: [
      {
        name: 'Eurasian Roller',
        note: 'A classic Ngulia visible migrant. One 1980 report counted well over 1000 passing south west of the ridge in less than 20 minutes.'
      },
      {
        name: 'Blue-cheeked Bee-eater',
        note: 'Usually smaller parties than rollers, but often noted in the same watches and useful for showing that Ngulia daylight movement is taxonomically broader than one species.'
      },
      {
        name: 'Lilac-breasted Roller',
        note: 'Not a visible-migration count story, but the ringers even caught the Somali race lorti, which gives the roller section a useful local-to-regional twist.'
      }
    ]
  },
  {
    family: 'Hirundinidae and Apodidae',
    title: 'Swallows, martins and swifts',
    recordValue: '59%',
    recordLabel: 'Share of total catch taken by day in one 2013 session',
    story:
      'The daytime atmosphere at Ngulia is not only about large raptors. Hirundines and swifts often reveal when weather has shifted and migrants are moving low enough to watch or net. They are less theatrical in the binders than rollers or falcons, but they make the daytime page feel true to field experience.',
    species: [
      {
        name: 'Barn Swallow',
        note: 'A Barn Swallow controlled in 2013 carried a ring from Kazakhstan, linking a very familiar visible migrant to the broader flyway in one clean story.'
      },
      {
        name: 'Common House Martin',
        note: 'Some seasons mention strong daytime attraction to sound lures and visible concentrations around the lodge when conditions turn right.'
      },
      {
        name: 'Common Swift',
        note: 'The binders often mention swifts overhead during the same weather shifts that concentrate falcons and rollers in the valley.'
      }
    ]
  }
]
</script>

<style scoped>
.vimig-page {
  padding-bottom: 5rem;
}

.vimig-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr);
  gap: 1.25rem;
  align-items: stretch;
  margin-top: 2rem;
}

.vimig-hero__lead {
  margin: 0 0 0.9rem;
  font-size: 1.18rem;
  line-height: 1.6;
}

.vimig-pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
  margin: 1.2rem 0 1rem;
}

.vimig-hero__bullets {
  margin-top: 0.8rem;
}

.vimig-photo-card {
  overflow: hidden;
}

.vimig-photo-card img {
  display: block;
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}

.vimig-photo-card figcaption {
  padding: 1rem 1.15rem 1.15rem;
  color: var(--text-soft);
  line-height: 1.65;
}

.vimig-stats {
  margin-top: 1.5rem;
}

.vimig-section {
  margin-top: 3rem;
}

.vimig-source-grid,
.vimig-family-grid {
  display: grid;
  gap: 1.25rem;
}

.vimig-source-grid {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  margin-top: 1rem;
}

.vimig-explainer {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr);
  gap: 1.25rem;
  align-items: start;
  margin-top: 1rem;
}

.vimig-photo-card--secondary img {
  aspect-ratio: 5 / 4;
}

.vimig-family-grid {
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  margin-top: 1rem;
}

.vimig-family-card {
  position: relative;
  overflow: hidden;
}

.vimig-family-card::before {
  content: '';
  position: absolute;
  inset: 0 0 auto;
  height: 0.35rem;
  background: linear-gradient(90deg, var(--accent-soft), var(--teal), rgba(255, 255, 255, 0));
}

.vimig-family-card__header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: start;
}

.vimig-family-card__badge {
  min-width: 8.4rem;
  padding: 0.8rem 0.9rem;
  border-radius: 1rem;
  background: rgba(255, 217, 120, 0.08);
  border: 1px solid rgba(255, 217, 120, 0.18);
  text-align: right;
}

.vimig-family-card__badge span {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--accent-soft);
}

.vimig-family-card__badge small {
  display: block;
  margin-top: 0.25rem;
  color: var(--text-soft);
  line-height: 1.45;
}

.vimig-family-card__species {
  display: grid;
  gap: 0.9rem;
  margin-top: 1rem;
}

.vimig-species-note {
  padding-top: 0.9rem;
  border-top: 1px solid rgba(243, 239, 230, 0.08);
}

.vimig-species-note h3 {
  margin: 0 0 0.35rem;
  font-size: 1rem;
}

.vimig-species-note p {
  margin: 0;
  color: var(--text-soft);
  line-height: 1.65;
}

.vimig-section__note {
  margin: 1rem 0 0;
  color: var(--text-soft);
  line-height: 1.65;
}

.vimig-closing {
  position: relative;
  overflow: hidden;
}

.vimig-closing::before {
  content: '';
  position: absolute;
  inset: auto -12% -3rem 35%;
  height: 10rem;
  background: radial-gradient(circle, rgba(78, 167, 160, 0.18), rgba(78, 167, 160, 0));
  pointer-events: none;
}

.vimig-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  margin-top: 1.2rem;
}

@media (max-width: 980px) {
  .vimig-hero,
  .vimig-explainer {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .vimig-family-card__header {
    flex-direction: column;
  }

  .vimig-family-card__badge {
    width: 100%;
    text-align: left;
  }
}
</style>
