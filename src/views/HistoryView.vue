<template>
  <section class="page history-page">
    <div class="section-label">About / History</div>
    <h1 class="page-title">The Ngulia story</h1>
    <p class="page-intro">
      How a chance discovery at the lodge lights grew into one of Africa’s clearest long-term records of nocturnal bird migration.
    </p>

    <section class="history-hero">
      <article class="panel history-hero__story">
        <div class="panel-inner">
          <div class="eyebrow">Core story</div>
          <p class="muted history-hero__summary">
            What began as a chance observation at a lodge in 1969 grew into a long-running migration project, with
            decades of ringing, recoveries, and field collaboration built around the birds drawn down on key nights.
          </p>
          <ul class="bullets history-hero__bullets">
            <li v-for="item in coreStory" :key="item">{{ item }}</li>
          </ul>

          <div class="history-hero__facts">
            <div v-for="fact in heroFacts" :key="fact.label" class="history-hero__fact">
              <span class="history-hero__fact-value">{{ fact.value }}</span>
              <span class="history-hero__fact-label">{{ fact.label }}</span>
            </div>
          </div>
        </div>
      </article>
    </section>

    <section class="history-timeline-block">
      <h2 class="panel-title history-section-title">Timeline</h2>

      <Swiper
        class="history-timeline__main"
        :modules="modules"
        :navigation="true"
        :keyboard="{ enabled: true }"
        :space-between="20"
        :thumbs="{ swiper: timelineSwiper && !timelineSwiper.destroyed ? timelineSwiper : null }"
        @swiper="setMainSwiper"
        @slideChange="handleSlideChange"
      >
        <SwiperSlide v-for="item in timeline" :key="item.period">
          <article class="panel history-milestone">
            <div class="history-milestone__media">
              <img :src="item.image" :alt="item.imageAlt" />
              <div class="history-milestone__overlay">
                <h3>{{ item.title }}</h3>
                <p>{{ item.text }}</p>
              </div>
            </div>
          </article>
        </SwiperSlide>
      </Swiper>

      <div class="history-timeline__scale-wrap">
        <Swiper
          class="history-timeline__scale"
          :modules="modules"
          :slides-per-view="'auto'"
          :space-between="12"
          :watch-slides-progress="true"
          :slide-to-clicked-slide="true"
          @swiper="setTimelineSwiper"
        >
          <SwiperSlide
            v-for="(item, index) in timeline"
            :key="`${item.period}-${item.short}`"
            class="history-timeline__scale-slide"
          >
            <button
              type="button"
              :class="['history-timeline__marker', { 'is-active': activeIndex === index }]"
              @click="goToTimelineItem(index)"
            >
              <span class="history-timeline__marker-dot"></span>
              <span class="history-timeline__marker-period">{{ item.period }}</span>
              <span class="history-timeline__marker-label">{{ item.short }}</span>
            </button>
          </SwiperSlide>
        </Swiper>
      </div>
    </section>

    <section class="history-video grid">
      <article class="panel history-video__frame">
        <div class="history-video__embed">
          <iframe
            src="https://www.youtube-nocookie.com/embed/I3M2XbrAGsc"
            title="Ngulia history presentation by Colin Jackson"
            loading="lazy"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowfullscreen
          ></iframe>
        </div>
      </article>

      <article class="panel history-video__text">
        <div class="panel-inner">
          <div class="eyebrow">Video</div>
          <h2 class="panel-title">Colin Jackson on the history of the site</h2>
          <p class="muted">
            This presentation adds a spoken version of the project history and works well alongside the timeline and
            written narrative below.
          </p>
          <a class="button-link" href="https://www.youtube.com/watch?v=I3M2XbrAGsc" target="_blank" rel="noreferrer">
            Watch on YouTube
          </a>
        </div>
      </article>
    </section>

    <section class="history-story-block">
      <div class="section-label">Full story</div>

      <article class="panel history-story">
        <div class="panel-inner history-story__inner">
          <section v-for="(section, index) in reviewSections" :key="section.title" class="history-story__section">
            <div class="history-story__heading">
              <span class="history-story__index">{{ String(index + 1).padStart(2, '0') }}</span>
              <h3 class="panel-title">{{ section.title }}</h3>
            </div>

            <p v-for="paragraph in section.paragraphs" :key="paragraph" class="history-story__paragraph">
              {{ paragraph }}
            </p>

            <figure class="history-story__figure">
              <img :src="section.image" :alt="section.imageAlt" class="history-story__figure-image" />
              <figcaption>{{ section.figureCaption }}</figcaption>
            </figure>
          </section>
        </div>
      </article>
    </section>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { A11y, Keyboard, Navigation, Thumbs } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'

const modules = [A11y, Keyboard, Navigation, Thumbs]

const activeIndex = ref(0)
const mainSwiper = ref(null)
const timelineSwiper = ref(null)

const coreStory = [
  'Ngulia’s migration phenomenon was discovered in 1969, soon after the lodge opened.',
  'On moonless, misty nights, the lodge lights can draw thousands of night-migrating birds down from the sky.',
  'Most birds are Palaearctic migrants travelling from Europe or Asia toward Africa.',
  'Ringing at Ngulia has produced one of Africa’s longest and richest migration datasets.',
  'The site connects Tsavo to breeding areas in Eurasia, passage sites in the Middle East, and wintering areas farther south in Africa.'
]

const heroFacts = [
  { value: '1969', label: 'Discovery at the lodge lights' },
  { value: '499,677', label: 'Palaearctic birds ringed by 2012' },
  { value: '222', label: 'Long-distance movements reported by 2012' }
]

const timeline = [
  {
    period: '1969',
    short: 'Discovery',
    title: 'A chance observation becomes a migration story.',
    text:
      'Soon after the lodge opened, misty nights at the floodlights revealed large falls of Palaearctic migrants and turned an unexpected event into the start of a serious field project.',
    image: '/history-archive/ngulia-1973-night-graeme.jpg',
    imageAlt: 'Historic night photograph showing birds around the illuminated lodge area.'
  },
  {
    period: '1972-1973',
    short: 'Coverage begins',
    title: 'The phenomenon is confirmed through regular fieldwork.',
    text:
      'Near-continuous seasonal coverage made the falls measurable, showing that the migration pattern repeated and could support long-term ringing work rather than isolated observations.',
    image: '/history-archive/djp-pole.jpg',
    imageAlt: 'Fieldworker carrying a pole with bird bags during ringing work.'
  },
  {
    period: '1976-1980s',
    short: 'Night catching grows',
    title: 'Methods evolve and the project becomes a real station.',
    text:
      'Night catching below the floodlights expanded, catches increased sharply, and Ngulia moved from remarkable field notes to a sustained ringing operation recognised across Africa.',
    image: '/history-archive/ngulia-2010-nets.jpg',
    imageAlt: 'Ringing team working beside mist nets in misty conditions.'
  },
  {
    period: '1993-1995',
    short: 'Expansion',
    title: 'Larger teams and a steadier operation reshape the work.',
    text:
      'The 1990s brought bigger teams, a shift in dawn netting, and more stable lighting, making the annual sessions more robust and more collaborative.',
    image: '/history-archive/ngulia-2012-field-1.jpg',
    imageAlt: 'Field team gathered around a table during a ringing session.'
  },
  {
    period: '2012-2014',
    short: 'Half-million and radar',
    title: 'The dataset becomes continental in scale and broader in method.',
    text:
      'By 2012 the ringing totals and recoveries had reached a remarkable scale, and radar work soon widened the picture from grounded birds to migration moving overhead across Tsavo.',
    image: '/history-archive/ngulia-2011-group.jpg',
    imageAlt: 'Group portrait of project participants at Ngulia.'
  },
  {
    period: '2015-2019',
    short: 'Living landscape',
    title: 'The habitat changes, but the project keeps evolving.',
    text:
      'Elephant-driven habitat change altered the daytime netting area, showing that the history of Ngulia is not only about data and people, but also about a field site that keeps changing.',
    image: '/history-archive/ngulia-2010-elephants.jpg',
    imageAlt: 'Elephants in vegetation near the Ngulia field area.'
  }
]

const reviewSections = [
  {
    title: 'A migration story discovered by accident',
    image: '/history-archive/ngulia-1973-night-graeme.jpg',
    imageAlt: 'Historic night photograph showing birds around the illuminated lodge area.',
    figureCaption: 'Historic night image from Ngulia showing the early light-attraction phenomenon.',
    paragraphs: [
      'Ngulia’s bird migration story began in 1969, the same year Ngulia Safari Lodge opened on the edge of the escarpment in Tsavo West National Park. The lodge sits at about 920 m above sea level, above a 300 m escarpment, with the Ngulia ridge rising behind it to 1,821 m. Its powerful game-viewing floodlights were intended to illuminate waterholes and attract mammals. Instead, on misty December nights, they revealed one of Africa’s most remarkable bird migration phenomena. Huge numbers of Palaearctic migrant birds, mostly small passerines travelling from Europe and Asia toward wintering areas farther south in Africa, were drawn down to the lights.',
      'The first observations were made by Alec Forbes-Watson, who found large numbers of migrant birds around the lodge lights and collected specimens for the National Museum in Nairobi. The effect was dramatic but also dangerous: many birds struck an illuminated white wall, and one 1.5 kW light had to be moved to reduce casualties. In the following years, David Pearson, Graeme Backhurst, Daphne Backhurst, Peter and Hazel Britton and others confirmed that these arrivals were not isolated events but a regular late-autumn phenomenon.'
    ]
  },
  {
    title: 'Why Ngulia is special',
    image: '/history-archive/ngulia-2010-nets.jpg',
    imageAlt: 'Ringing team standing beside mist nets in cloudy conditions.',
    figureCaption: 'Mist-netting scene that reflects the conditions and field setting behind the Ngulia phenomenon.',
    paragraphs: [
      'The Ngulia phenomenon depends on a rare combination of geography, weather and darkness. During November and December, large numbers of night-migrating birds cross southeastern Kenya on their way south. When low cloud or mist descends to the level of the lodge lights, especially on moonless nights, birds that would normally pass unseen overhead are drawn down toward the illuminated area. Showers or rain can intensify the effect. When conditions are right, thousands of birds may be grounded around the lodge by dawn. Most disperse during the morning and move on the following night.',
      'The main species in the early years were Marsh Warbler, Thrush Nightingale and Common Whitethroat, with many other Palaearctic migrants occurring in smaller numbers. Surprisingly few Afrotropical migrants were caught compared with the huge numbers of Eurasian migrants, although species such as Harlequin Quail and Jacobin Cuckoo were regularly noted.'
    ]
  },
  {
    title: 'From discovery to long-term ringing station',
    image: '/history-archive/djp-pole.jpg',
    imageAlt: 'Fieldworker holding a pole with multiple bird bags.',
    figureCaption: 'Archive image of ringing logistics as the annual sessions became more regular and organised.',
    paragraphs: [
      'By the 1972-73 season, near-continuous daily coverage was achieved from late November to early January, and more than 2,500 passerine migrants were ringed. This established the basic pattern of the site: birds were grounded when mist reached bush-top height or lower under moonless conditions; clear nights or high cloud produced few birds on the ground, even when migration was visible overhead.',
      'From 1972 to 1992, small teams returned each year around the November-December new moon periods. At first, most birds were caught after dawn in mist nets set in the bush south of the lodge. From 1976, night catching below the floodlights became increasingly important, with one to three nets positioned close to the lights. This change increased catches substantially, and on good nights even small Kenya-based teams could process more than 1,000 birds.',
      'By the 1980s, Ngulia was already recognised as a unique ringing site for Palaearctic passerines in Africa. The project had become not only a spectacular field operation, but also a major scientific resource, collecting data on timing, age, moult, weight, fat stores, species composition and long-distance recoveries.'
    ]
  },
  {
    title: 'Growth, international collaboration and scientific value',
    image: '/history-archive/ngulia-2012-field-1.jpg',
    imageAlt: 'Project team working together around a table at Ngulia.',
    figureCaption: 'Later field teams reflect the more collaborative and international scale of the project.',
    paragraphs: [
      'After 1993, the scale of the operation expanded. Larger teams became involved, including Kenyan and international ringers. In 1994, dawn netting was moved to the north of the lodge, beyond the floodlights, which often produced larger catches. By 2012, the lodge had been manned on more than 1,100 autumn nights. Mist had occurred on more than 60% of those nights and rain on 26%. By then, 499,677 Palaearctic birds had been ringed at Ngulia, producing 222 long-distance ringing movements connecting the site with breeding areas in Europe and Asia, passage sites in the Middle East, wintering areas in southern Africa, and a likely Ethiopian stopover area.',
      'These recoveries showed that Ngulia is linked to a vast migration system. Birds passing the lodge include populations breeding from western and northern Europe across to Siberia and central and southwest Asia. Many travel through the Middle East, Arabia and the Horn of Africa before reaching Kenya. Some winter not far beyond Kenya or northern Tanzania, while others continue to Botswana, Mozambique, Zimbabwe or South Africa.'
    ]
  },
  {
    title: 'What the birds reveal',
    image: '/history-archive/ngulia-2011-group.jpg',
    imageAlt: 'Group portrait of Ngulia participants and collaborators.',
    figureCaption: 'The long record depends on repeated work by people returning to the site over many seasons.',
    paragraphs: [
      'The long-term data show that different species pass Ngulia at different times. Thrush Nightingale tends to occur earlier and declines by mid-December, whereas Marsh Warbler passage increases from mid-November and can continue into January. November species include Red-backed Shrike, Olive-tree Warbler, Rufous Scrub Robin, Spotted Flycatcher and Eurasian Nightjar.',
      'Measurements of weight and fat show that some birds arrive with enough fuel for long onward flights. Marsh Warbler, Common Whitethroat, River Warbler, Willow Warbler, Basra Reed Warbler, Olive-tree Warbler and Red-backed Shrike can be 20-30%, sometimes even 50%, above lean weight. Other species, such as Irania, Common Nightingale, Rufous Scrub Robin, Upcher’s Warbler and Isabelline Shrike, rarely carry such large reserves and generally do not migrate much farther south than Ngulia.',
      'The data also show long-term changes. Over four decades, Marsh Warbler increased as a proportion of the catch, while Common Whitethroat declined. Isabelline Shrike and Rufous Scrub Robin became much less prominent, with likely declines also in Upcher’s Warbler and Willow Warbler.'
    ]
  },
  {
    title: 'Recent years and new technology',
    image: '/history-archive/ngulia-2012-field-1.jpg',
    imageAlt: 'Field team gathered around equipment and notes during project work.',
    figureCaption: 'Recent seasons combine long-running field practice with newer tools and broader scientific questions.',
    paragraphs: [
      'The 2013-2015 seasons added another 35,000 Palaearctic birds to the Ngulia total and 20 additional recoveries. The 2013 season was particularly strong, with 21,052 migrants ringed between 25 November and 13 December, helped by frequent persistent night mist. In 2014, mist was mostly restricted to the first week and 7,051 migrants were ringed. In 2015, a later session with nine misty nights produced 7,638 migrants.',
      'In 2013, a radar system from the Swiss Ornithological Institute operated at Ngulia from November to April. This allowed researchers to compare birds caught on the ground with migration passing overhead. Radar data showed migration increasing in late November and December, decreasing toward February, and rising again in March and April as birds moved north toward Eurasia. The radar also confirmed that birds migrate over Ngulia even on clear, mist-free nights, when they are not caught at the lodge.',
      'This was an important step because ringing tells the story of birds brought down by mist and light, while radar reveals the broader flow of migration above Tsavo. Together, they show that Ngulia is both a spectacular local phenomenon and a window into one of the great long-distance bird migration systems of the world.'
    ]
  },
  {
    title: 'A living project',
    image: '/history-archive/ngulia-2010-elephants.jpg',
    imageAlt: 'Elephants moving through vegetation near Ngulia.',
    figureCaption: 'Elephant pressure has helped reshape the vegetation around the lodge and the daytime netting area.',
    paragraphs: [
      'Ngulia is not only a place of scientific discovery. It is also a long-running collaboration between Kenyan institutions, visiting ringers, the lodge, Kenya Wildlife Service, museums, conservation organisations and volunteers. The work has continued for decades because people return year after year to document, handle and release birds that may have crossed continents.',
      'The story is still changing. The bush around the lodge, especially the daytime netting area, has been strongly modified by elephants, shifting from more continuous bush in the 1990s to more open grassland with scattered bushes by 2015. This affects how grounded birds are held around the lodge and how many can be caught after dawn.',
      'After more than half a century, Ngulia remains one of the most important places in Africa for studying Palaearctic migrant birds. Its history is a story of chance discovery, careful observation, international collaboration and long-term commitment to understanding the journeys of birds that connect Europe, Asia, the Middle East and Africa.'
    ]
  }
]

function setMainSwiper(swiper) {
  mainSwiper.value = swiper
}

function setTimelineSwiper(swiper) {
  timelineSwiper.value = swiper
}

function handleSlideChange(swiper) {
  activeIndex.value = swiper.realIndex
}

function goToTimelineItem(index) {
  activeIndex.value = index
  if (mainSwiper.value) mainSwiper.value.slideTo(index)
}
</script>

<style scoped>
.history-page {
  padding-top: 2rem;
}

.history-hero {
  margin-top: 2rem;
}

.history-hero__story {
  position: relative;
  overflow: hidden;
}

.history-hero__story::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at top left, rgba(242, 193, 78, 0.16), rgba(242, 193, 78, 0) 34%),
    linear-gradient(135deg, rgba(78, 167, 160, 0.12), rgba(78, 167, 160, 0) 36%);
}

.history-hero__summary {
  max-width: 48rem;
  line-height: 1.8;
}

.history-hero__bullets {
  margin-top: 1.2rem;
}

.history-hero__facts {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
  margin-top: 1.4rem;
}

.history-hero__fact {
  padding: 0.95rem 1rem;
  border: 1px solid rgba(243, 239, 230, 0.08);
  border-radius: 1rem;
  background: rgba(8, 13, 20, 0.3);
}

.history-hero__fact-value {
  display: block;
  font-size: 1.55rem;
  font-weight: 700;
  color: var(--accent-soft);
  margin-bottom: 0.25rem;
}

.history-hero__fact-label {
  color: var(--text-soft);
  line-height: 1.5;
}

.history-timeline-block,
.history-story-block {
  margin-top: 2rem;
}

.history-section-title {
  font-size: clamp(1.5rem, 2.3vw, 2rem);
  margin: 0 0 0.9rem;
}

:deep(.history-timeline__main .swiper-button-prev),
:deep(.history-timeline__main .swiper-button-next) {
  width: 2.85rem;
  height: 2.85rem;
  border-radius: 999px;
  color: var(--text);
  background: rgba(10, 18, 28, 0.82);
  border: 1px solid rgba(243, 239, 230, 0.12);
  backdrop-filter: blur(14px);
}

:deep(.history-timeline__main .swiper-button-prev::after),
:deep(.history-timeline__main .swiper-button-next::after) {
  font-size: 1rem;
  font-weight: 700;
}

.history-milestone {
  overflow: hidden;
}

.history-milestone__media {
  position: relative;
  min-height: 24rem;
  background: #0d141d;
}

.history-milestone__media img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.history-milestone__overlay {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: end;
  gap: 0.7rem;
  min-height: 24rem;
  padding: 1.25rem;
  background:
    linear-gradient(180deg, rgba(7, 11, 17, 0.12) 0%, rgba(7, 11, 17, 0.46) 48%, rgba(7, 11, 17, 0.9) 100%);
}

.history-milestone__overlay h3 {
  margin: 0;
  font-size: clamp(1.5rem, 3vw, 2.3rem);
  max-width: 16ch;
}

.history-milestone__overlay p {
  margin: 0;
  max-width: 40rem;
  color: rgba(243, 239, 230, 0.88);
  line-height: 1.72;
}

.history-timeline__scale-wrap {
  position: relative;
  margin-top: 1rem;
  padding: 0.15rem 0 0.2rem;
}

.history-timeline__scale-wrap::before {
  content: '';
  position: absolute;
  top: 1.48rem;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, rgba(242, 193, 78, 0.18), rgba(78, 167, 160, 0.48), rgba(242, 193, 78, 0.18));
  pointer-events: none;
}

.history-timeline__scale-slide {
  width: 168px;
}

.history-timeline__marker {
  display: grid;
  gap: 0.28rem;
  width: 100%;
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--text);
  text-align: left;
  cursor: pointer;
}

.history-timeline__marker-dot {
  width: 0.9rem;
  height: 0.9rem;
  border-radius: 999px;
  border: 2px solid rgba(255, 217, 120, 0.52);
  background: rgba(10, 18, 28, 0.96);
  box-shadow: 0 0 0 0 rgba(255, 217, 120, 0.22);
  transition: transform 180ms ease, box-shadow 180ms ease, background 180ms ease;
}

.history-timeline__marker-period {
  display: block;
  margin-top: 0.5rem;
  color: var(--accent-soft);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.74rem;
}

.history-timeline__marker-label {
  display: block;
  color: var(--text-soft);
  line-height: 1.45;
}

.history-timeline__marker.is-active .history-timeline__marker-dot,
.history-timeline__marker:hover .history-timeline__marker-dot {
  transform: scale(1.08);
  background: var(--accent-soft);
  box-shadow: 0 0 0 8px rgba(255, 217, 120, 0.14);
}

.history-timeline__marker.is-active .history-timeline__marker-label,
.history-timeline__marker:hover .history-timeline__marker-label {
  color: var(--text);
}

.history-video {
  grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
  margin-top: 2rem;
  align-items: stretch;
}

.history-video__frame {
  overflow: hidden;
}

.history-video__embed {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
}

.history-video__embed iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

.history-video__text {
  display: flex;
}

.history-video__text .panel-inner {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.9rem;
}

.history-story__inner {
  padding: 1.6rem;
}

.history-story__section + .history-story__section {
  margin-top: 2.2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(243, 239, 230, 0.08);
}

.history-story__heading {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  margin-bottom: 1rem;
}

.history-story__index {
  flex: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 2.2rem;
  height: 2.2rem;
  border-radius: 999px;
  border: 1px solid rgba(242, 193, 78, 0.28);
  color: var(--accent-soft);
  background: rgba(242, 193, 78, 0.08);
  font-size: 0.8rem;
  letter-spacing: 0.08em;
}

.history-story__paragraph {
  margin: 0 0 1rem;
  color: var(--text-soft);
  line-height: 1.82;
  max-width: 54rem;
}

.history-story__figure {
  margin: 1.35rem 0 0;
  border: 1px solid rgba(243, 239, 230, 0.08);
  border-radius: 1.2rem;
  overflow: hidden;
}

.history-story__figure-image {
  display: block;
  width: 100%;
  max-height: 34rem;
  object-fit: cover;
}

.history-story__figure figcaption {
  padding: 0.9rem 1.2rem 1.05rem;
  color: var(--text-soft);
  background: rgba(8, 13, 20, 0.52);
  line-height: 1.6;
}

@media (max-width: 980px) {
  .history-video {
    grid-template-columns: 1fr;
  }

  :deep(.history-timeline__main .swiper-button-prev),
  :deep(.history-timeline__main .swiper-button-next) {
    display: none;
  }

  .history-milestone__media,
  .history-milestone__overlay {
    min-height: 22rem;
  }
}

@media (max-width: 640px) {
  .history-hero__facts {
    grid-template-columns: 1fr;
  }

  .history-story__inner {
    padding: 1.2rem;
  }

  .history-story__heading {
    align-items: start;
  }

  .history-timeline__scale-slide {
    width: 150px;
  }
}
</style>
