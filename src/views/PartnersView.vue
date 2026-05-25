<template>
  <section class="page partners-page">
    <div class="section-label">About / Partners</div>
    <h1 class="page-title">Partners behind the Ngulia project</h1>
    <p class="page-intro">
      The archive reports point most clearly to three core partners, supported by a wider set of historical funders,
      institutions, and collaborating organizations acknowledged across the Ngulia reports.
    </p>

    <section class="partners-section">
      <div class="section-label">Primary Partners</div>
      <div class="partners-grid partners-grid--primary">
        <article v-for="partner in primaryPartners" :key="partner.name" class="panel partner-card partner-card--primary">
          <div class="partner-card__logo-wrap">
            <img :src="partner.logo" :alt="`${partner.name} logo`" class="partner-card__logo" />
          </div>
          <div class="panel-inner partner-card__body">
            <h2 class="panel-title">{{ partner.name }}</h2>
            <p class="muted">{{ partner.description }}</p>
            <a class="button-link" :href="partner.url" target="_blank" rel="noreferrer">Visit website</a>
          </div>
        </article>
      </div>
    </section>

    <section class="partners-section">
      <div class="section-label">Secondary Partners</div>
      <h2 class="panel-title partners-section__title">Historical supporters and collaborating organizations</h2>
      <div class="partners-grid partners-grid--secondary">
        <article v-for="partner in secondaryPartners" :key="partner.name" class="panel partner-card partner-card--secondary">
          <div class="partner-card__logo-wrap partner-card__logo-wrap--secondary">
            <img :src="partner.logo" :alt="`${partner.name} logo`" class="partner-card__logo partner-card__logo--secondary" />
          </div>
          <div class="panel-inner partner-card__body">
            <h3 class="panel-title">{{ partner.name }}</h3>
            <p class="muted">{{ partner.description }}</p>
            <a class="partner-card__link" :href="partner.url" target="_blank" rel="noreferrer">{{ partner.linkLabel }}</a>
          </div>
        </article>
      </div>
    </section>
  </section>
</template>

<script setup>
const primaryPartners = [
  {
    name: 'A Rocha Kenya',
    description:
      'A Rocha Kenya appears in the later project material through Colin Jackson and represents one of the clearest current organizational anchors around the Ngulia work.',
    url: 'https://www.arocha.or.ke/',
    logo: '/partner-logos/a-rocha-kenya.svg'
  },
  {
    name: 'Kenya Wildlife Service',
    description:
      'The Ngulia reports repeatedly thank Kenya Wildlife Service for permission to ring at the site and for continued support for the project over many years.',
    url: 'https://www.kws.go.ke/',
    logo: '/partner-logos/kws.png'
  },
  {
    name: 'Ngulia Lodge',
    description:
      'Ngulia Lodge is central to the field operation itself, providing the physical setting, practical support, and continuity that made the migration project possible.',
    url: 'https://nguliasafarilodge.com/',
    logo: '/partner-logos/ngulia-lodge.png'
  }
]

const secondaryPartners = [
  {
    name: 'National Museums of Kenya',
    description:
      'The museum network appears directly in the reports as a funding and scientific partner, and the historical notes also connect the earliest observations to museum collecting in Nairobi.',
    url: 'https://nmk.go.ke/',
    linkLabel: 'National Museums of Kenya',
    logo: '/partner-logos/nmk.webp'
  },
  {
    name: 'Nature Kenya',
    description:
      'Nature Kenya is acknowledged in the archive reports, including through the Bird Committee / EANHS history that supported participation and wider ornithological work around the project.',
    url: 'https://naturekenya.org/',
    linkLabel: 'Nature Kenya',
    logo: '/partner-logos/nature-kenya.png'
  },
  {
    name: 'Wetland Trust',
    description:
      'The Wetland Trust is one of the most frequently acknowledged funding partners in the reports, repeatedly credited for rings and financial support.',
    url: 'https://www.wwt.org.uk/',
    linkLabel: 'Wetland Trust / WWT',
    logo: '/partner-logos/wwt.svg'
  },
  {
    name: 'Swedish Ringing Centre',
    description:
      'The reports repeatedly thank the Swedish Ringing Centre for ring support and the forwarding of recovery information. The linked page sits within the Swedish Museum of Natural History.',
    url: 'https://www.nrm.se/english/researchandcollections/environmentalresearchandmonitoring/birdmonitoring/thebirdringingcentre.9001658.html',
    linkLabel: 'Swedish Ringing Centre',
    logo: '/partner-logos/nrm.svg'
  },
  {
    name: 'Earthwatch',
    description:
      'The older thanks material names Earthwatch teams and co-leaders as part of the field effort during the project’s volunteer-supported phases.',
    url: 'https://www.earthwatch.org/',
    linkLabel: 'Earthwatch',
    logo: '/partner-logos/earthwatch.svg'
  },
  {
    name: 'Kenya Safari Lodges & Hotels',
    description:
      'The thanks material identifies Kenya Safari Lodges & Hotels as the company behind Ngulia Safari Lodge in the later management period, making it part of the project’s operational support history.',
    url: 'https://nguliasafarilodge.com/',
    linkLabel: 'Ngulia Lodge site',
    logo: '/partner-logos/ngulia-lodge.png'
  }
]
</script>

<style scoped>
.partners-page {
  padding-top: 2rem;
}

.partners-section {
  margin-top: 2rem;
}

.partners-section__title {
  margin: 0.35rem 0 1rem;
  font-size: clamp(1.45rem, 2.2vw, 1.95rem);
}

.partners-grid {
  display: grid;
  gap: 1rem;
}

.partners-grid--primary {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.partners-grid--secondary {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.partner-card {
  overflow: hidden;
}

.partner-card__logo-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 12rem;
  padding: 1.4rem;
  background:
    linear-gradient(180deg, rgba(15, 23, 35, 0.95), rgba(9, 16, 25, 0.88)),
    radial-gradient(circle at top left, rgba(242, 193, 78, 0.08), rgba(242, 193, 78, 0) 36%);
}

.partner-card__logo-wrap--secondary {
  min-height: 9.5rem;
  padding: 1rem;
}

.partner-card__logo {
  display: block;
  max-width: min(220px, 100%);
  max-height: 86px;
  width: auto;
  height: auto;
  object-fit: contain;
}

.partner-card__logo--secondary {
  max-width: min(180px, 100%);
  max-height: 64px;
}

.partner-card__body {
  display: grid;
  gap: 0.85rem;
}

.partner-card__link {
  color: var(--accent-soft);
  text-decoration: none;
}

.partner-card--primary {
  position: relative;
}

.partner-card--primary::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at top left, rgba(242, 193, 78, 0.12), rgba(242, 193, 78, 0) 28%),
    linear-gradient(135deg, rgba(78, 167, 160, 0.08), rgba(78, 167, 160, 0) 34%);
}

@media (max-width: 980px) {
  .partners-grid--primary {
    grid-template-columns: 1fr;
  }
}
</style>
