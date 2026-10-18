import {matchesProfile, compareProfiles} from './filter-core.mjs';
const themeButton = document.querySelector('.theme-toggle');
const savedTheme = localStorage.getItem('trailblazers-theme');
if (savedTheme) document.documentElement.dataset.theme = savedTheme;
themeButton?.addEventListener('click', () => {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  localStorage.setItem('trailblazers-theme', next);
  themeButton.setAttribute('aria-label', `Switch to ${next === 'dark' ? 'light' : 'dark'} theme`);
});

const search = document.querySelector('#search');
const category = document.querySelector('#category');
const era = document.querySelector('#era');
const region = document.querySelector('#region');
const sort = document.querySelector('#sort');
const grid = document.querySelector('#card-grid');
const cards = grid ? [...grid.querySelectorAll('.person-card')] : [];
const count = document.querySelector('#result-count');
const empty = document.querySelector('#empty-state');
function updateCollection() {
  if (!grid) return;
  const term = normalize(search.value);
  let shown = 0;
  const filters = {search: term, category: category.value, era: era.value, region: region.value};
  for (const card of cards) {
    const matches = matchesProfile(JSON.parse(card.dataset.profile), filters);
    card.hidden = !matches;
    if (matches) shown++;
  }
  const ordered = [...cards].sort((a,b) => compareProfiles(JSON.parse(a.dataset.profile), JSON.parse(b.dataset.profile), sort.value));
  grid.replaceChildren(...ordered);
  count.textContent = `Showing ${shown} ${shown === 1 ? 'person' : 'people'}`;
  empty.hidden = shown > 0;
}
for (const control of [search,category,era,region,sort]) control?.addEventListener(control === search ? 'input' : 'change', updateCollection);
function clearFilters() { search.value='';category.value='';era.value='';region.value='';sort.value='name';updateCollection();search.focus(); }
document.querySelector('#clear-filters')?.addEventListener('click', clearFilters);
document.querySelector('#empty-clear')?.addEventListener('click', clearFilters);
document.querySelectorAll('[data-category-jump]').forEach(button => button.addEventListener('click', () => {
  category.value = button.dataset.categoryJump;
  updateCollection();
  document.querySelector('#collection').scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
}));
updateCollection();

const range = document.querySelector('#timeline-range');
const timelineItems = [...document.querySelectorAll('#timeline-list li')];
function updateTimeline() {
  if (!range) return;
  document.querySelector('#timeline-output').value = range.value;
  for (const item of timelineItems) item.hidden = Number(item.querySelector('time').textContent) > Number(range.value);
}
range?.addEventListener('input', updateTimeline);
updateTimeline();

const shareButton = document.querySelector('#share-button');
shareButton?.addEventListener('click', async () => {
  const status = document.querySelector('#share-status');
  try {
    if (navigator.share) await navigator.share({title: document.title, url: location.href});
    else { await navigator.clipboard.writeText(location.href); status.textContent = 'Link copied to clipboard.'; }
  } catch (error) { if (error.name !== 'AbortError') status.textContent = 'Copy the address in your browser to share this story.'; }
});

// Rotate the daily selection in the visitor's browser; the build-time choice is the no-script fallback.
const dailyPanel = document.querySelector('.daily-panel');
if (dailyPanel && cards.length) {
  const dailyCard = cards[Math.floor(Date.now() / 86400000) % cards.length];
  const person = JSON.parse(dailyCard.dataset.profile);
  dailyPanel.querySelector('p').textContent = person.summary;
  const dailyLink = dailyPanel.querySelector('.button');
  dailyLink.href = dailyCard.querySelector('.card-link').href;
  dailyLink.textContent = `Meet ${person.name} ↗`;
  dailyPanel.querySelector('.daily-name strong').textContent = person.name;
  dailyPanel.querySelector('.daily-name > span').textContent = person.categories[0];
  const portrait = dailyPanel.querySelector('.portrait--type');
  if (portrait) {
    portrait.setAttribute('aria-label', `Typographic portrait placeholder for ${person.name}`);
    portrait.querySelector('span').textContent = person.name.replaceAll('.', '').split(' ').filter(part => !['c','j'].includes(part.toLowerCase())).map(part => part[0]).join('').slice(0,2);
  }
}
