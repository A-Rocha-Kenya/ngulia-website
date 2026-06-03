<template>
  <section class="page">
    <div class="section-label">Science / Publications</div>
    <h1 class="page-title">Publications</h1>
    <p class="page-intro">
      A reference list of publications and related outputs that draw on the Ngulia ringing project.
    </p>

    <section class="featured-grid">
      <article
        v-for="item in publications.highlights"
        :key="item.title"
        :class="[
          'panel',
          'featured-card',
          item.embedUrl ? 'featured-card--video' : 'featured-card--review'
        ]"
      >
        <div class="panel-inner">
          <div class="featured-badge">Featured</div>
          <h2 class="panel-title featured-title" v-html="cleanTitleHtml(item.displayTitle || item.title)"></h2>
          <p class="featured-summary">{{ item.description }}</p>
          <p v-if="!item.embedUrl" class="featured-reference">
            <span class="citation-authors">{{ formatAuthors(item.authors) }}</span><span v-if="item.year">{{ ` (${item.year}). ` }}</span>
            <span class="citation-title" v-html="titleWithPeriod(cleanTitleHtml(item.title))"></span><span>{{ ' ' }}</span><span v-if="item.journal">
              <span class="citation-journal">{{ cleanText(item.journal) }}</span>
            </span><span v-if="issueBlock(item)">{{ ` ${issueBlock(item)}` }}</span><span v-if="item.journal || issueBlock(item)">.</span><span v-if="item.doi">{{ ' DOI: ' }}<a :href="doiHref(item.doi)" target="_blank" rel="noreferrer" class="citation-link">{{ item.doi }}</a>.
            </span><span v-else-if="item.url">{{ ' ' }}<a :href="item.url" target="_blank" rel="noreferrer" class="citation-link">Link</a>.
            </span>
          </p>

          <div v-if="item.embedUrl" class="featured-video">
            <iframe
              :src="item.embedUrl"
              :title="plainTitle(item.title)"
              loading="lazy"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </article>
    </section>

    <article class="panel bibliography-panel">
      <div class="panel-inner">
        <div class="bibliography-toolbar">
          <div class="eyebrow">Bibliography</div>
          <input
            id="publication-filter"
            v-model="filterText"
            type="text"
            class="bibliography-filter__input"
            aria-label="Search bibliography"
            placeholder="Search author, title, year, journal, DOI..."
          />
        </div>

        <div class="publications-list">
          <section v-for="group in groupedEntries" :key="group.label" class="publications-group">
            <h3 class="publications-group__title">{{ group.label }}</h3>
            <article
              v-for="entry in group.entries"
              :id="referenceId(entry)"
              :key="`${entry.key}-${entry.title}-${entry.year}`"
              class="publications-item"
            >
              <p class="publication-citation">
                <span class="citation-authors">{{ formatAuthors(entry.authors) }}</span><span v-if="entry.year">{{ ` (${entry.year}). ` }}</span>
                <span class="citation-title" v-html="titleWithPeriod(cleanTitleHtml(entry.title))"></span><span>{{ ' ' }}</span><span v-if="entry.journal">
                  <span class="citation-journal">{{ cleanText(entry.journal) }}</span>
                </span><span v-if="issueBlock(entry)">{{ ` ${issueBlock(entry)}` }}</span><span v-if="entry.journal || issueBlock(entry)">.</span><span v-if="entry.doi">{{ ' DOI: ' }}<a :href="doiHref(entry.doi)" target="_blank" rel="noreferrer" class="citation-link">{{ entry.doi }}</a>.
                </span><span v-else-if="entry.url">{{ ' ' }}<a :href="entry.url" target="_blank" rel="noreferrer" class="citation-link">Link</a>.
                </span>
              </p>
            </article>
          </section>

          <p v-if="!groupedEntries.length" class="muted publications-empty">
            No references match the current filter.
          </p>
        </div>
      </div>
    </article>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import publicationsData from '../data/publicationsData.json'

const publications = ref(publicationsData)
const filterText = ref('')

const sortedEntries = computed(() =>
  [...publications.value.entries].sort((a, b) => {
    const yearDiff = Number.parseInt(b.year || '0', 10) - Number.parseInt(a.year || '0', 10)
    if (yearDiff) return yearDiff
    return plainTitle(a.title).localeCompare(plainTitle(b.title))
  })
)

const filteredEntries = computed(() => {
  const query = filterText.value.trim().toLowerCase()
  if (!query) return sortedEntries.value

  return sortedEntries.value.filter((entry) =>
    [
      entry.key,
      entry.title,
      entry.authors,
      entry.journal,
      entry.year,
      entry.volume,
      entry.issue,
      entry.pages,
      entry.doi
    ]
      .filter(Boolean)
      .join(' ')
      .toLowerCase()
      .includes(query)
  )
})

const groupedEntries = computed(() => {
  const order = ['Articles', 'Books', 'Chapters', 'Websites', 'Reports', 'Other']
  const groups = new Map(order.map((label) => [label, []]))

  for (const entry of filteredEntries.value) {
    const label = entryGroupLabel(entry)
    if (!groups.has(label)) groups.set(label, [])
    groups.get(label).push(entry)
  }

  return order
    .map((label) => ({ label, entries: groups.get(label) || [] }))
    .filter((group) => group.entries.length)
})

function splitAuthors(authors = '') {
  return authors
    .split(/\s+and\s+/i)
    .map((author) => author.trim())
    .filter(Boolean)
}

function isMostlyUppercase(value = '') {
  const letters = [...value].filter((char) => /\p{L}/u.test(char))
  if (!letters.length) return false
  const uppercaseLetters = letters.filter((char) => char === char.toUpperCase()).length
  return uppercaseLetters / letters.length > 0.8
}

function titleCaseToken(token = '') {
  if (/^\d/.test(token)) return token
  if (/^\p{L}\.$/u.test(token)) return token.toUpperCase()
  if (/^\p{L}\.\p{L}\.?$/u.test(token)) return token.toUpperCase()
  if (token.includes('-')) return token.split('-').map(titleCaseToken).join('-')
  if (token.includes("'")) return token.split("'").map((part, index) => (index === 0 ? titleCaseToken(part) : part ? `${part[0].toUpperCase()}${part.slice(1).toLowerCase()}` : part)).join("'")
  if (/^\p{L}+\.$/u.test(token)) return `${token.slice(0, 1).toUpperCase()}${token.slice(1).toLowerCase()}`
  return token ? `${token[0].toUpperCase()}${token.slice(1).toLowerCase()}` : token
}

function cleanText(value = '') {
  const normalized = value.replace(/\\&/g, '&').replace(/\s+/g, ' ').trim()
  return isMostlyUppercase(normalized) ? normalized.toLowerCase().split(' ').map(titleCaseToken).join(' ') : normalized
}

function cleanTitleHtml(value = '') {
  const normalized = value.replace(/\\&/g, '&').replace(/\s+/g, ' ').trim()
  return isMostlyUppercase(normalized.replace(/<[^>]+>/g, ''))
    ? normalized.replace(/(^|>)([^<]+)/g, (_, prefix, text) => `${prefix}${text.toLowerCase().split(' ').map(titleCaseToken).join(' ')}`)
    : normalized
}

function formatAuthors(authors = '') {
  const names = splitAuthors(authors).map(cleanText)
  if (names.length <= 1) return names[0] || ''
  if (names.length === 2) return `${names[0]} & ${names[1]}`
  return `${names.slice(0, -1).join(', ')}, & ${names.at(-1)}`
}

function plainTitle(title = '') {
  return cleanTitleHtml(title).replace(/<[^>]+>/g, '').replace(/[.]+$/, '').trim()
}

function titleWithPeriod(title = '') {
  const trimmed = title.trim()
  if (!trimmed) return ''
  return /[.!?]$/.test(trimmed) ? trimmed : `${trimmed}.`
}

function doiHref(doi = '') {
  return `https://doi.org/${doi}`
}

function issueBlock(entry) {
  let text = ''
  if (entry.volume) text += entry.volume
  if (entry.issue) text += `(${entry.issue})`
  if (entry.pages) text += `${text ? ': ' : ''}${entry.pages}`
  return text
}

function entryGroupLabel(entry) {
  const type = (entry.entryType || '').toLowerCase()
  const journal = cleanText(entry.journal || '').toLowerCase()

  if (type === 'techreport') return 'Reports'
  if (type === 'book') return 'Books'
  if (type === 'incollection' || type === 'inbook' || type === 'inproceedings') return 'Chapters'
  if (type === 'misc') return 'Other'
  if (type === 'online' || journal.includes('website')) return 'Websites'
  return 'Articles'
}

function referenceId(entry) {
  return `ref-${cleanText(entry.key || plainTitle(entry.title)).toLowerCase().replace(/[^a-z0-9]+/g, '-')}`
}
</script>

<style scoped>
.featured-grid {
  display: grid;
  gap: 1.25rem;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  margin-top: 2rem;
}

.featured-card {
  position: relative;
  overflow: hidden;
  border-color: rgba(242, 193, 78, 0.14);
}

.featured-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at top right, rgba(242, 193, 78, 0.16), transparent 34%),
    linear-gradient(140deg, rgba(78, 167, 160, 0.08), transparent 48%);
  pointer-events: none;
}

.featured-card--review {
  grid-column: span 7;
  background:
    linear-gradient(180deg, rgba(20, 29, 41, 0.98), rgba(11, 17, 25, 0.95)),
    linear-gradient(120deg, rgba(242, 193, 78, 0.08), transparent 40%);
}

.featured-card--video {
  grid-column: span 5;
  background:
    linear-gradient(180deg, rgba(13, 22, 32, 0.98), rgba(9, 14, 22, 0.96)),
    linear-gradient(160deg, rgba(78, 167, 160, 0.08), transparent 52%);
}

.featured-card .panel-inner {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.featured-summary {
  margin: 0 0 1.15rem;
  color: var(--text);
  line-height: 1.7;
  max-width: 44rem;
}

.featured-badge {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  margin-bottom: 0.95rem;
  padding: 0.24rem 0.58rem;
  border-radius: 999px;
  border: 1px solid rgba(242, 193, 78, 0.2);
  background: rgba(242, 193, 78, 0.08);
  color: var(--accent-soft);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.featured-title {
  margin-bottom: 0.75rem;
  font-size: clamp(1.45rem, 2.4vw, 2.25rem);
  line-height: 1;
}

.featured-reference,
.publication-citation {
  margin: 0;
  color: var(--text-soft);
  line-height: 1.75;
  overflow-wrap: anywhere;
}

.publication-citation {
  padding-left: 1.6rem;
  text-indent: -1.6rem;
}

.featured-reference {
  margin-top: auto;
  padding: 1rem 1.1rem;
  border: 1px solid rgba(243, 239, 230, 0.1);
  border-radius: 1rem;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.02));
  padding-left: 2.7rem;
  text-indent: -1.6rem;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

.citation-authors,
.citation-title {
  color: var(--text);
}

.citation-journal {
  font-style: italic;
}

.citation-link {
  color: var(--accent-soft);
  text-decoration: underline;
  text-underline-offset: 0.15em;
  overflow-wrap: anywhere;
}

.featured-video {
  margin-top: auto;
  border-radius: 1rem;
  overflow: hidden;
  border: 1px solid rgba(243, 239, 230, 0.12);
  background: rgba(7, 11, 17, 0.92);
  aspect-ratio: 16 / 9;
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.25);
}

.featured-video iframe {
  width: 100%;
  height: 100%;
  border: 0;
}

.bibliography-panel {
  margin-top: 1.5rem;
}

.bibliography-toolbar {
  display: grid;
  gap: 0.8rem;
  margin-bottom: 1.4rem;
}

.bibliography-filter__input {
  width: 100%;
  padding: 0.9rem 1rem;
  border-radius: 1rem;
  border: 1px solid var(--border);
  background: rgba(8, 14, 21, 0.92);
  color: var(--text);
}

.bibliography-filter__input::placeholder {
  color: rgba(168, 179, 194, 0.78);
}

.bibliography-filter__input:focus {
  outline: 1px solid rgba(242, 193, 78, 0.4);
  border-color: rgba(242, 193, 78, 0.3);
}

.publications-list {
  display: grid;
  gap: 1.4rem;
}

.publications-group {
  display: grid;
  gap: 0.8rem;
}

.publications-group__title {
  margin: 0;
  font-size: 1rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--accent-soft);
}

.publications-item {
  display: grid;
  gap: 0.55rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.publications-item:first-child {
  padding-top: 0;
  border-top: 0;
}

.publications-empty {
  margin: 0;
  padding-top: 0.2rem;
}

@media (max-width: 900px) {
  .featured-grid {
    grid-template-columns: 1fr;
  }

  .featured-card--review,
  .featured-card--video {
    grid-column: span 1;
  }
}

@media (max-width: 640px) {
  .publication-citation,
  .featured-reference {
    padding-left: 0;
    text-indent: 0;
  }
}
</style>
