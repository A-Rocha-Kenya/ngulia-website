<template>
  <section class="page team-page">
    <div class="section-label">About / Team</div>
    <h1 class="page-title">The people behind Ngulia</h1>
    <p class="page-intro">
      The Ngulia project depends on long-term organisers, seasonal field leaders, and a much wider network of ringers,
      scribes, extractors, and collaborators.
    </p>

    <section class="team-section">
      <div class="section-label">Current Team</div>
      <div class="team-grid team-grid--current">
        <article v-for="person in currentTeam" :key="person.name" class="panel team-card">
          <div class="team-card__media">
            <img :src="person.photo" :alt="person.photoAlt" />
          </div>
          <div class="panel-inner team-card__body">
            <h2 class="panel-title">{{ person.name }}</h2>
            <p class="team-card__affiliation">{{ person.affiliation }}</p>
            <p class="muted">{{ person.bio }}</p>
            <div class="team-card__socials">
              <a
                v-for="social in person.socials"
                :key="social.label"
                class="team-card__social"
                :href="social.href"
                target="_blank"
                rel="noreferrer"
              >
                {{ social.label }}
              </a>
            </div>
          </div>
        </article>
      </div>
    </section>

    <section class="team-section">
      <div class="section-label">Project History</div>
      <h2 class="panel-title team-section__title">Historical leadership and long-term contributors</h2>
      <div class="team-grid team-grid--historical">
        <article v-for="person in historicalTeam" :key="person.name" class="panel team-card team-card--historical">
          <div class="team-card__media">
            <img :src="person.photo" :alt="person.photoAlt" />
          </div>
          <div class="panel-inner team-card__body">
            <h3 class="panel-title">{{ person.name }}</h3>
            <p class="team-card__affiliation">{{ person.affiliation }}</p>
            <p class="muted">{{ person.bio }}</p>
            <div class="team-card__socials">
              <a
                v-for="social in person.socials"
                :key="social.label"
                class="team-card__social"
                :href="social.href"
                target="_blank"
                rel="noreferrer"
              >
                {{ social.label }}
              </a>
            </div>
          </div>
        </article>
      </div>
    </section>

    <section class="team-section">
      <div class="section-label">Participants</div>
      <h2 class="panel-title team-section__title">Participants named in the reviewed archive material</h2>
      <article class="panel">
        <div class="panel-inner">
          <div class="team-roster__list">
            <span v-for="name in participants" :key="name" class="team-roster__name">{{ name }}</span>
          </div>
        </div>
      </article>
    </section>
  </section>
</template>

<script setup>
const currentTeam = [
  {
    name: 'Colin Jackson',
    affiliation: 'A Rocha Kenya; long-term Ngulia field organiser',
    bio:
      'Recent Ngulia reports consistently place Colin Jackson among the core organisers and contacts. The archive material also points to his role in training support, field coordination, and maintaining continuity during the later phase of the project.',
    photo: '/history-archive/ngulia-2012-field-1.jpg',
    photoAlt: 'Field team gathered around a table during a ringing session.',
    socials: [{ label: 'Email', href: 'mailto:colin.jackson@arocha.org' }]
  },
  {
    name: 'Current team member',
    affiliation: 'Affiliation to confirm',
    bio:
      'Placeholder card for an additional current team member. Replace with the confirmed name, organisation, short role description, and contact or profile links.',
    photo: '/history-archive/ngulia-2011-group.jpg',
    photoAlt: 'Group portrait of Ngulia participants and collaborators.',
    socials: [{ label: 'Profile pending', href: '#' }]
  },
  {
    name: 'Current team member',
    affiliation: 'Affiliation to confirm',
    bio:
      'Placeholder card for a second additional current team member. Replace with the confirmed name, organisation, short role description, and contact or profile links.',
    photo: '/history-archive/ngulia-2010-nets.jpg',
    photoAlt: 'Ringing team working beside mist nets in misty conditions.',
    socials: [{ label: 'Profile pending', href: '#' }]
  }
]

const historicalTeam = [
  {
    name: 'David Pearson',
    affiliation: 'Long-term scientific lead',
    bio:
      'David Pearson appears throughout the historical material as one of the central figures in building and documenting the Ngulia project, from the early confirmation of the migration phenomenon to the later synthesis reports.',
    photo: '/history-archive/djp-pole.jpg',
    photoAlt: 'Fieldworker carrying bird bags during ringing work.',
    socials: [{ label: 'Archive contact', href: 'mailto:dpearson251@gmail.com' }]
  },
  {
    name: 'Graeme Backhurst',
    affiliation: 'Long-term project leader and organiser',
    bio:
      'Graeme Backhurst is repeatedly visible in the archive as a leading organiser, contact, and co-author. The older thanks documents and later reports both show his central role in the long-running Ngulia effort.',
    photo: '/history-archive/ngulia-1973-night-graeme.jpg',
    photoAlt: 'Historic night photograph associated with the early Ngulia field period.',
    socials: [{ label: 'Archive contact', href: 'mailto:graeme.backhurst@gmail.com' }]
  },
  {
    name: 'Daphne Backhurst',
    affiliation: 'Early project contributor',
    bio:
      'Daphne Backhurst is named in the historical notes among the early contributors who helped confirm that the migrant falls at Ngulia were a recurring phenomenon rather than an isolated event.',
    photo: '/history-archive/ngulia-2011-group.jpg',
    photoAlt: 'Group portrait of Ngulia participants and collaborators.',
    socials: []
  },
  {
    name: 'Peter Britton',
    affiliation: 'Early project contributor',
    bio:
      'Peter Britton is listed in the historical notes among the ornithologists involved in the early years when the field observations at Ngulia were being established into a repeatable scientific effort.',
    photo: '/history-archive/ngulia-2010-nets.jpg',
    photoAlt: 'Ringing team working beside mist nets in misty conditions.',
    socials: []
  },
  {
    name: 'Hazel Britton',
    affiliation: 'Early project contributor',
    bio:
      'Hazel Britton is also named in the early project history and belongs to the group of contributors associated with the formative years of the Ngulia ringing programme.',
    photo: '/history-archive/ngulia-2011-group.jpg',
    photoAlt: 'Group portrait of Ngulia participants and collaborators.',
    socials: []
  }
]

const participants = [
  'Alec Forbes-Watson',
  'Alex Mwalimu',
  'Alexandra de Sosa',
  'Alain Jacot',
  'Albert Baya',
  'Amir Balaban',
  'Andrew Kinzer',
  'Anna Forbes-Watson',
  'Anna di Lorenzo',
  'Attila Sandor',
  'Barry Williams',
  'Benjamin Wishikoti',
  'Bengt Hansson',
  'Bennie van den Brink',
  'Benno van den Hoek',
  'Bernard Amakobe',
  'Brian Manton',
  'Brian Watmough',
  'Cedric Khayale',
  'Chege Kariuki',
  'Chris Bridges',
  'Chris Wade',
  'Claudia Maves',
  'Colin Jackson',
  'Colin de Kock',
  'Cornelia Hafner',
  'Cornelia Laux',
  'Daphne Backhurst',
  'Dave Fletcher',
  'David Gitau',
  'David Murdoch',
  'David Ngala',
  'David Pearson',
  'David Turner',
  'Dephence Mghoi',
  'Dominic Chesire',
  'Don Turner',
  'Edgar Kaeslin',
  'Edson Mlamba',
  'Edwig Vanhassel',
  'Edwin Gichohi',
  'Edwin Njuguna',
  'Erik Ness',
  'Esther Wangoi',
  'Francis Argyle',
  'Franziska Hillig',
  'Gabor Lovei',
  'Gabriella Rosquist',
  'Gerhard Nikolaus',
  'Gidon Perlman',
  'Gladys Kungu',
  'Graeme Backhurst',
  'Graham Grieve',
  'Gyorgy Miklay',
  'Hamisi Nyale Mumbo',
  'Hazel Britton',
  'Heike Nikolaus',
  'Herbert Stark',
  'Ian Kerton',
  'Jaap Gijsbertsen',
  'Jacinta Mureithi',
  'James Ndungu',
  'James Wachira',
  'Jan Heckmann',
  'Jan Kaiser',
  'Jan Rosmus',
  'Jan van Duinen',
  'Janette Troop',
  'Jaroslav Jelinek',
  'Jeff Davis',
  'Jerry Lewis',
  'Jeremy Barker',
  'Joanna Turner',
  'John Dalziel',
  'John Gitiri',
  'John Musina',
  'John Willsher',
  'Jon Hornbuckle',
  'Jonathan Baya',
  'Joost Valkenburg',
  'Joseph Mwangi',
  'Joseph Oyugi',
  'Julia Ibbotson',
  'Julia Loshchagina',
  'Kandy Brown',
  'Kane Bridges',
  'Kathleen OBrien',
  'Katie Hanlon',
  'Keith Sunderland',
  'Kell Horton',
  'Kerry Leonard',
  'Leon Bennun',
  'Lennox Kirao',
  'Lennox Kithi',
  'Lex Tervelde',
  'Libby Manton',
  'Lispa Wachira',
  'Lorraine Wheaton',
  'Lubo Cerva',
  'Lubo Karasek',
  'Ludek Hovorka',
  'Ludo Roothaert',
  'Maarten Virrips',
  'Malcolm Wilson',
  'Marc Hebbelinck',
  'Martha Nzisa',
  'Martin Cade',
  'Martin Sternman',
  'Mary Ellen Rowe',
  'Mercy Njeri',
  'Mikhail Markovets',
  'Mikko Ojanen',
  'Miles Coverdale',
  'Moses Kinuthia',
  'Nicodemus Nalianya',
  'Nicole Stoeber',
  'Norbert Roothaert',
  'Oliver Nasirwa',
  'Patricia Moynahan',
  'Patrick Gichuki',
  'Patrik Wildjang',
  'Paul Roper',
  'Peter Britton',
  'Peter Kennerley',
  'Peter Kohler',
  'Peter Thomas',
  'Peter Wairasho',
  'Phil Jones',
  'Ray Knock',
  'Richard Charles',
  'Richard Seddon',
  'Ron Cleveley',
  'Roni Brereton-Stiles',
  'Roni Jackson',
  'Rupert Watson',
  'Ruud Kampf',
  'Sameer Wamaye',
  'Samina Mohn',
  'Sarah Waring',
  'Shai Agmon',
  'Shailesh Patel',
  'Sharon Pincott',
  'Silas Ekesa',
  'Simon Valle',
  'Steve Rook',
  'Stephen Chege',
  'Sumiko Tanaka',
  'Sylvester Karimi',
  'Tabitha Njoki',
  'Tibor Csorgo',
  'Titus Imboma',
  'Tracey Couto',
  'Trevor Squire',
  'Ursula Kohler',
  'Victoria Spulniak',
  'Vincent van der Spek',
  'Vicki Parfit',
  'Walter Roggeman',
  'Wanyoike Wamiti',
  'Wellington Kombe',
  'Willis Ochieng',
  'Zsoka Csapo'
]
</script>

<style scoped>
.team-page {
  padding-top: 2rem;
}

.team-section {
  margin-top: 2rem;
}

.team-section__title {
  margin: 0.35rem 0 1rem;
  font-size: clamp(1.45rem, 2.2vw, 1.95rem);
}

.team-grid {
  display: grid;
  gap: 1rem;
}

.team-grid--current {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.team-grid--historical {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.team-card {
  overflow: hidden;
}

.team-card__media {
  height: 18rem;
  background: #0d141d;
}

.team-card__media img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.team-card__body {
  display: grid;
  gap: 0.8rem;
}

.team-card__affiliation {
  margin: -0.1rem 0 0;
  color: var(--accent-soft);
  font-size: 0.96rem;
  line-height: 1.45;
}

.team-card__socials {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
}

.team-card__social {
  display: inline-flex;
  align-items: center;
  min-height: 2rem;
  padding: 0.38rem 0.7rem;
  border-radius: 999px;
  border: 1px solid rgba(242, 193, 78, 0.2);
  background: rgba(242, 193, 78, 0.08);
  color: var(--text);
  font-size: 0.85rem;
}

.team-card--historical .team-card__media {
  height: 15rem;
}

.team-roster__list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem;
}

.team-roster__name {
  display: inline-flex;
  align-items: center;
  min-height: 2.3rem;
  padding: 0.45rem 0.8rem;
  border-radius: 999px;
  border: 1px solid rgba(243, 239, 230, 0.1);
  background: rgba(9, 16, 25, 0.46);
  color: var(--text-soft);
  line-height: 1.3;
}

@media (max-width: 980px) {
  .team-grid--current {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 700px) {
  .team-grid--current {
    grid-template-columns: 1fr;
  }
}
</style>
