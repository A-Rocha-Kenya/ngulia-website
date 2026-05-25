<template>
  <section class="page molt-page">
    <div class="section-label">Science / Ageing, Moult &amp; Biometrics</div>
    <h1 class="page-title">What birds in the hand reveal</h1>
    <p class="page-intro">
      Ngulia is famous for dramatic nights at the lodge lights, but the science comes from what
      happens once birds are safely in the hand. Ageing, moult scoring, sexing when possible,
      and careful biometrics turn each catch into evidence about migration strategy, timing, and
      condition for both Afro-Palearctic and Afrotropical birds.
    </p>

    <section class="molt-hero">
      <article class="panel">
        <div class="panel-inner">
          <div class="eyebrow">Page focus</div>
          <p class="molt-hero__lead">
            This page keeps the literature in the background and the ringing table in the
            foreground.
          </p>
          <p class="muted">
            The point is not simply to say that birds moult. It is to show why Ngulia still needs
            birds in the hand: to separate first-year from adult birds, read feather limits and
            moult strategy, measure body condition, document sex where it can be assigned, and
            build a comparable long-term dataset from one season to the next.
          </p>
          <div class="molt-pill-row">
            <span v-for="item in heroPills" :key="item" class="pill">{{ item }}</span>
          </div>
          <ul class="bullets molt-hero__bullets">
            <li v-for="item in heroBullets" :key="item">{{ item }}</li>
          </ul>
        </div>
      </article>

      <figure class="panel molt-photo-card">
        <img src="/history-archive/ngulia-2012-field-1.jpg" alt="Ngulia team working around the ringing table." />
        <figcaption>
          The ringing table is where plumage, feathers, moult, weight, wing length, fat and
          written notes become one scientific record.
        </figcaption>
      </figure>
    </section>

    <section class="stats-grid molt-stats">
      <StatCard
        v-for="fact in keyFacts"
        :key="fact.label"
        :label="fact.label"
        :value="fact.value"
        :description="fact.description"
      />
    </section>

    <section class="molt-section">
      <div class="section-label">Why Handle Birds</div>
      <div class="molt-grid molt-grid--story">
        <article class="panel">
          <div class="panel-inner">
            <h2 class="panel-title">Why ringing matters beyond a species list</h2>
            <p class="muted">
              A dawn count can tell us that migrants were present. It cannot reliably show whether
              a Marsh Warbler was a first-year bird or an adult, whether a Barred Warbler still
              carries old secondaries, whether a migrant has suspended moult for flight, or whether
              the bird is lean, heavy, or carrying substantial fuel for the next leg south.
            </p>
            <p class="muted">
              At Ngulia, each handled bird helps answer a practical set of questions: who is moving
              through Tsavo, when different age classes pass, whether feather renewal happened on
              the breeding grounds or in Africa, and how condition changes across nights, seasons,
              and decades.
            </p>
          </div>
        </article>

        <article class="panel">
          <div class="panel-inner">
            <div class="eyebrow">At the table</div>
            <h2 class="panel-title">What is recorded in practice</h2>
            <ul class="bullets">
              <li>Age from plumage, retained juvenile feathers, bare-part colour, and in some passerines skull ossification.</li>
              <li>Moult from the state of primaries, secondaries, tail feathers, and visible feather limits.</li>
              <li>Sex when plumage or measurements make it possible in species such as Irania, Barred Warbler, and some Whitethroats.</li>
              <li>Biometrics including wing length, weight, and fat that show readiness for onward flight.</li>
              <li>Feather evidence in the broad sense: which feathers are old, fresh, growing, suspended, or retained from earlier plumages.</li>
            </ul>
          </div>
        </article>
      </div>
    </section>

    <section class="molt-section">
      <div class="section-label">What Ngulia Reads</div>
      <div class="molt-card-grid">
        <article v-for="card in processCards" :key="card.title" class="panel">
          <div class="panel-inner">
            <div class="eyebrow">{{ card.eyebrow }}</div>
            <h2 class="panel-title">{{ card.title }}</h2>
            <p class="muted">{{ card.text }}</p>
          </div>
        </article>
      </div>
    </section>

    <section class="molt-section">
      <div class="section-label">What It Reveals</div>
      <div class="molt-grid molt-grid--story">
        <article class="panel">
          <div class="panel-inner">
            <h2 class="panel-title">The questions these data answer</h2>
            <div class="molt-question-list">
              <div v-for="item in questions" :key="item.title" class="molt-question">
                <h3>{{ item.title }}</h3>
                <p>{{ item.text }}</p>
              </div>
            </div>
          </div>
        </article>

        <figure class="panel molt-photo-card molt-photo-card--species">
          <img src="/generated/photos/barred-warbler.jpg" alt="Barred Warbler held in the hand at Ngulia." />
          <figcaption>
            Barred Warbler is one of the Ngulia species that helped clarify complex split moult
            strategies between Eurasia and East Africa.
          </figcaption>
        </figure>
      </div>
    </section>

    <section class="molt-section">
      <div class="section-label">Afrotropical Birds</div>
      <div class="molt-grid molt-grid--story">
        <article class="panel">
          <div class="panel-inner">
            <h2 class="panel-title">This is not only a Palearctic story</h2>
            <p class="muted">
              Ngulia is best known for Eurasian migrants, and one striking result of the long
              programme is that Afrotropical migrants are relatively scarce in the catches between
              October and April. That contrast is itself part of the science, but it does not mean
              African migrants are irrelevant here.
            </p>
            <p class="muted">
              The same ringing work documents nocturnal or rain-linked movements of Harlequin
              Quail, Jacobin Cuckoo, Diederik Cuckoo, Plain Nightjar, Nubian Nightjar and many
              other species moving within East Africa. For several of these birds, ageing and sexing
              criteria are less standardised than in classic Palearctic warblers, which makes the
              in-hand notes even more valuable.
            </p>
          </div>
        </article>

        <article class="panel">
          <div class="panel-inner">
            <div class="eyebrow">Afrotrop ageing notes</div>
            <h2 class="panel-title">Why Afrotropical ageing deserves space on this page</h2>
            <p class="muted">
              The archived Afrotropical ageing sheets used by the team work through juvenile,
              immature, distinct immature, sub-adult, full adult and unageable adult categories.
              The logic is explicit: use plumage, retained juvenile feathers, soft-part colour and,
              where applicable, skull ossification to make age calls that can be checked later.
            </p>
            <p class="muted">
              That approach fits Ngulia well. The site is not only a place to process large numbers
              of migrants, but also a place to improve the criteria needed to read African birds
              more confidently in the hand.
            </p>
          </div>
        </article>
      </div>
    </section>

    <section class="molt-section">
      <div class="section-label">Long-Term Goal</div>
      <article class="panel molt-goal">
        <div class="panel-inner">
          <h2 class="panel-title">Why the work should continue</h2>
          <p class="muted">
            Ngulia matters because the same measurements have been taken across decades at one of
            Africa’s most distinctive migration sites. That continuity lets the project compare age
            ratios, moulting states, species mix, and body condition across years instead of
            treating each ringing season as an isolated spectacle.
          </p>
          <p class="muted">
            The goal is simple and durable: keep building a dataset that explains how migrants use
            East Africa, where they pause to moult, how young and adult birds differ, and how
            Afrotropical movements fit into a site famous for Afro-Palearctic passage.
          </p>
          <div class="molt-actions">
            <RouterLink class="button-link" to="/science/dashboard">Explore the dashboard</RouterLink>
            <RouterLink class="button-link" to="/science/publications">See publications</RouterLink>
          </div>
        </div>
      </article>
    </section>
  </section>
</template>

<script setup>
import StatCard from '../components/StatCard.vue'

const heroPills = ['Ageing', 'Moult', 'Sexing', 'Biometrics', 'Afrotropical migrants']

const heroBullets = [
  'In many Ngulia species, first-year birds outnumber adults, but the balance changes by species and through the season.',
  'Feather state can show whether a bird moulted on the breeding grounds, in northeast Africa, or is still heading toward a later winter moult.',
  'Weight and fat scores connect migration timing to physiological readiness for the next leg south.',
  'Afrotropical migrants are fewer in the catches, but they add a different and still underused layer of migration information.'
]

const keyFacts = [
  {
    label: 'Palaearctic birds ringed',
    value: '499,677',
    description: 'Ringed at Ngulia by 2012 in the long-term overview paper.'
  },
  {
    label: 'Typical age balance',
    value: '2:1',
    description: 'First-year birds often outnumber adults across the season as a whole.'
  },
  {
    label: 'Afrotropical migrants reviewed',
    value: '64',
    description: 'Species treated in the Ngulia-focused East Africa review.'
  },
  {
    label: 'Harlequin Quail ringed',
    value: '2169',
    description: 'A reminder that Ngulia also captures substantial Afrotropical movement.'
  }
]

const processCards = [
  {
    eyebrow: 'Ageing',
    title: 'Juvenile, immature, sub-adult, adult',
    text:
      'Ageing is not cosmetic. It tells Ngulia whether passage is dominated by young birds, whether adults pass earlier or later, and whether one season produced a different demographic signal from another.'
  },
  {
    eyebrow: 'Moult',
    title: 'Fresh, worn, growing, or suspended feathers',
    text:
      'Moult scoring reveals where feather renewal fits into migration. At Ngulia that can mean birds arriving with old worn primaries, very fresh feathers grown in Africa, or suspended moult that signals an active migratory state.'
  },
  {
    eyebrow: 'Sexing',
    title: 'Useful where it can be done well',
    text:
      'Not every species can be sexed confidently, but when it is possible the result sharpens how wing length, plumage tone, timing and body condition are interpreted within a species.'
  },
  {
    eyebrow: 'Biometrics',
    title: 'Wing, weight, fat, and structure',
    text:
      'Biometrics make the dataset comparable. They help separate populations, estimate fuel loads, and connect the ringing session to bigger questions about stopover use and onward flight range.'
  }
]

const questions = [
  {
    title: 'When do young and adult birds pass?',
    text:
      'Ngulia has shown that many species are not age-neutral in timing. In Marsh Warbler, for example, young birds pass later on average than adults.'
  },
  {
    title: 'Where did moult happen?',
    text:
      'The feather state of birds at Ngulia points to different strategies: some moulted before leaving Eurasia, some in northeast Africa, and some are still carrying feathers due for replacement farther south.'
  },
  {
    title: 'What unusual strategies become visible only in the hand?',
    text:
      'Handled birds have helped clarify complex patterns such as the split flight-feather moult of Barred Warbler and similar mixed strategies in other long-distance migrants.'
  },
  {
    title: 'How do African migrants fit into the same system?',
    text:
      'Ngulia’s Afrotropical records show that rain-linked intra-African movements also pass the site, even though the catches are dominated by Eurasian migrants.'
  }
]
</script>

<style scoped>
.molt-page {
  display: grid;
  gap: 2rem;
}

.molt-hero,
.molt-grid--story {
  display: grid;
  gap: 1.25rem;
  grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
}

.molt-hero__lead {
  margin: 0 0 0.7rem;
  font-size: 1.35rem;
  line-height: 1.35;
}

.molt-pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem;
  margin: 1rem 0 1rem;
}

.molt-hero__bullets {
  margin-top: 0.2rem;
}

.molt-stats {
  margin-top: -0.25rem;
}

.molt-section {
  display: grid;
  gap: 1rem;
}

.molt-grid {
  display: grid;
  gap: 1.25rem;
}

.molt-card-grid {
  display: grid;
  gap: 1.25rem;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.molt-photo-card {
  margin: 0;
  overflow: hidden;
}

.molt-photo-card img {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 320px;
  object-fit: cover;
}

.molt-photo-card figcaption {
  padding: 1rem 1.2rem 1.2rem;
  color: var(--text-soft);
  line-height: 1.65;
}

.molt-photo-card--species img {
  min-height: 0;
  aspect-ratio: 1.15 / 1;
}

.molt-question-list {
  display: grid;
  gap: 1rem;
}

.molt-question h3 {
  margin: 0 0 0.35rem;
  font-size: 1rem;
}

.molt-question p {
  margin: 0;
  color: var(--text-soft);
  line-height: 1.7;
}

.molt-goal .panel-inner {
  display: grid;
  gap: 0.8rem;
}

.molt-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  margin-top: 0.25rem;
}

@media (max-width: 980px) {
  .molt-hero,
  .molt-grid--story,
  .molt-card-grid {
    grid-template-columns: 1fr;
  }

  .molt-photo-card img {
    min-height: 260px;
  }
}

@media (max-width: 640px) {
  .molt-page {
    gap: 1.5rem;
  }

  .molt-hero__lead {
    font-size: 1.15rem;
  }

  .molt-actions {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
