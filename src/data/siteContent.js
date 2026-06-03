export const siteMeta = {
  title: 'Ngulia Bird Migration Project',
  strapline: 'Night migration, ringing science, and recovery routes across Africa, the Middle East, and Eurasia.',
  footerEmail: 'colin.jackson@arocha.org'
}

export const navigation = [
  {
    label: 'Science',
    items: [
      { label: 'Dashboard', to: '/science/dashboard' },
      { label: 'Visible migration', to: '/science/vimig' },
      { label: 'Ageing & Moult', to: '/science/molting' },
      { label: 'Data', to: '/science/data' },
      { label: 'Publications', to: '/science/publications' }
    ]
  },
  {
    label: 'About',
    items: [
      { label: 'History', to: '/about/history' },
      { label: 'Team', to: '/about/team' },
      { label: 'Partners', to: '/about/partners' }
    ]
  },
  {
    label: 'Participate',
    items: [
      { label: 'Visit & volunteer', to: '/participate/visit' },
      { label: 'Donate', to: '/participate/donate' }
    ]
  }
]

export const homeCards = [
  {
    label: 'Science',
    title: 'Interactive summaries, recovery routes, and open data',
    text: 'Explore long-term ringing patterns, top species, the dashboard recovery map, and the datasets that support the website science pages.',
    to: '/science/dashboard'
  },
  {
    label: 'History',
    title: 'The Ngulia story',
    text: 'Follow the discovery, timeline, and long-form story of how a chance observation became long-term migration science.',
    to: '/about/history'
  },
  {
    label: 'Participate',
    title: 'Visit, volunteer, or support the work',
    text: 'Find the practical information needed to plan a visit, join the field team, or support the project financially.',
    to: '/participate/visit'
  }
]

export const historyVisitorBoxes = [
  {
    eyebrow: 'Why Visit Ngulia',
    title: 'Why does Ngulia matter?',
    items: [
      'Ngulia is one of Africa’s best-known bird ringing sites for long-distance migrants.',
      'Hundreds of thousands of migrants have been recorded here over decades.',
      'Recoveries connect this site to Europe, Asia, the Middle East, and southern Africa.',
      'The project helps explain migration timing, body condition, and long-term change.'
    ]
  },
  {
    eyebrow: 'What You May See',
    title: 'What might you see here?',
    items: [
      'Warblers, nightingales, shrikes, and flycatchers during the November to December season.',
      'Birds dropping near the lodge lights on misty, moonless nights.',
      'Freshly grounded migrants moving through the bushes at dawn.',
      'A dramatic escarpment setting that shapes the migration experience.'
    ]
  },
  {
    eyebrow: 'Best Timing',
    title: 'When are conditions best?',
    items: [
      'The main season is November and December.',
      'The most dramatic nights are often moonless or close to new moon.',
      'Low mist or cloud at lodge level can bring migrants down in large numbers.',
      'On clear nights, many birds may pass overhead without landing.'
    ]
  },
  {
    eyebrow: 'What We Learn',
    title: 'What does ringing reveal?',
    items: [
      'Where migrants come from and where they go next.',
      'How migration timing differs between species.',
      'Whether birds are young or adult when they pass through.',
      'How body condition and numbers change across years.'
    ]
  }
]

export const aboutSections = {
  history: {
    eyebrow: 'About / History',
    title: 'A light, a ridge, and a migration bottleneck',
    intro:
      'Ngulia Lodge in Tsavo West became internationally important when large numbers of nocturnal migrants were found descending around the lodge lights under misty conditions. That discovery shaped decades of ringing, observation, and recovery work.',
    sections: [
      {
        title: 'Core story',
        bullets: [
          'Night migrants attracted to the lodge lights were first noted in 1969.',
          'Autumn ringing sessions over November and December built a uniquely long time series.',
          'Ngulia became especially important for Marsh Warbler, Thrush Nightingale, and Common Whitethroat, along with many scarcer migrants.'
        ]
      },
      {
        title: 'Why the site matters',
        bullets: [
          'The dataset spans multiple decades and allows comparisons across years, species, and weather conditions.',
          'Recovery links connect Ngulia to breeding areas, passage sites, and wintering regions far beyond Kenya.',
          'The site combines migration ecology, moulting patterns, condition metrics, and long-term change.'
        ]
      }
    ]
  },
  team: {
    eyebrow: 'About / Team',
    title: 'A field project built around ringing teams',
    intro:
      'The website should present the project through the people who lead fieldwork, research, logistics, and long-term continuity. This page is designed to make the project feel human while staying factual.',
    sections: [
      {
        title: 'Suggested team blocks',
        bullets: [
          'Scientific leads and long-term coordinators',
          'Field team leads during the ringing season',
          'Data, recovery, and analysis contributors',
          'Partner contacts where relevant'
        ]
      },
      {
        title: 'Page intent',
        bullets: [
          'Show faces, roles, and short descriptions rather than long biographies.',
          'Make it easy for volunteers and collaborators to understand who is involved.',
          'Add section-specific contact points only where needed.'
        ]
      }
    ]
  },
  partners: {
    eyebrow: 'About / Partners',
    title: 'Organizations that make the project possible',
    intro:
      'The partners page should explain each organization’s role clearly, with restrained text, logos where available, and direct links out to their own websites.',
    sections: [
      {
        title: 'Current partner list',
        bullets: [
          'A Rocha Kenya',
          'Kenya Wildlife Service',
          'Ngulia Safari Lodge',
          'National Museums of Kenya',
          'SOI',
          'Safring',
          'Museum partner to confirm'
        ]
      },
      {
        title: 'Design approach',
        bullets: [
          'Use equal visual treatment for logos rather than oversized sponsor blocks.',
          'Keep descriptions short and functional.',
          'Link this page clearly from participation and donation content.'
        ]
      }
    ]
  }
}

export const scienceSections = {
  molting: {
    eyebrow: 'Science / Ageing, Moult & Biometrics',
    title: 'What birds in the hand reveal',
    intro:
      'This page focuses on why Ngulia handles birds in the hand: to age them, score moult, take biometrics, and connect those records to migration strategy for both Afro-Palearctic and Afrotropical species.',
    sections: [
      {
        title: 'Core themes',
        bullets: [
          'Ageing, moult, sexing, and biometrics as part of one ringing workflow',
          'Why Afrotropical birds belong in the same story as Eurasian migrants',
          'How in-hand evidence motivates the need for long-term ringing'
        ]
      },
      {
        title: 'Page direction',
        bullets: [
          'Fieldwork and long-term goals are foregrounded over literature review',
          'Species examples are used to illustrate discovery rather than catalogue every moult pattern',
          'The live page is implemented in a dedicated view component'
        ]
      }
    ]
  },
  data: {
    eyebrow: 'Science / Data',
    title: 'Open-access data and processed website outputs',
    intro:
      'The website is built from processed Ngulia datasets prepared from the long-term ringing and recovery source files. This page explains what data exist, how they are used, and how open access should be handled.',
    sections: [
      {
        title: 'Core source datasets',
        bullets: [
          'Curated daily counts support the ringing summaries and phenology views',
          'Curated recoveries support the recovery views and migration probability surface',
          'Raw spreadsheets remain the source of truth and are not read directly in the frontend'
        ]
      },
      {
        title: 'Processed outputs',
        bullets: [
          'Dashboard summary tables and yearly totals',
          'Species-level summaries and phenology tables',
          'Recovery map files prepared for Mapbox GL JS',
          'Migration probability grids used on the home page'
        ]
      },
      {
        title: 'Open-access approach',
        bullets: [
          'Website-facing data products should be reproducible from the source files through a preprocessing step',
          'Processed files can be shared in open formats such as JSON or CSV',
          'Licensing, citation guidance, and download endpoints still need to be finalized'
        ]
      }
    ]
  }
}

export const participateSections = {
  volunteer: {
    eyebrow: 'Participate / Volunteer',
    title: 'Volunteer for ringing and field support',
    intro:
      'This page should work as a practical guide for ringers and scribes who want to join the Ngulia sessions. It is meant to be skimmed quickly and should stay concrete.',
    sections: [
      {
        title: 'Roles',
        bullets: [
          'Volunteer as a ringer',
          'Volunteer as a scribe',
          'Clarify expectations, prior experience, and the kind of field schedule involved'
        ]
      },
      {
        title: 'Practical information',
        bullets: [
          'Accommodation, food, cost, and transport',
          'Typical work rhythm, rest periods, and training opportunities',
          'Application route and volunteer contact point to confirm'
        ]
      }
    ]
  },
  visit: {
    eyebrow: 'Participate / Visit',
    title: 'Plan a simple visit to Ngulia',
    intro:
      'Not every visitor will join the ringing team. This page should explain if and when simple visits are possible, what people can expect to see, and how requests should be coordinated.',
    sections: [
      {
        title: 'What to include',
        bullets: [
          'Who visits are suitable for',
          'Whether visits are possible during or outside the ringing season',
          'What visitors might see at the site'
        ]
      },
      {
        title: 'Planning details',
        bullets: [
          'Timing, access, and logistics',
          'Who coordinates requests',
          'Whether visits should remain limited or actively encouraged'
        ]
      }
    ]
  },
  donate: {
    eyebrow: 'Participate / Donate',
    title: 'Support the project financially',
    intro:
      'This page should explain why support matters, what donations pay for, and how individual or organizational contributions strengthen the field season and long-term science.',
    sections: [
      {
        title: 'Use of funds',
        bullets: [
          'Accommodation and field costs',
          'Training and transport for Kenyan ringers',
          'Data management, coordination, and future science communication'
        ]
      },
      {
        title: 'Open details to confirm',
        bullets: [
          'Who receives the donations',
          'Whether one-time and recurring options will both be offered',
          'Whether to develop a corporate sponsorship route'
        ]
      }
    ]
  }
}
