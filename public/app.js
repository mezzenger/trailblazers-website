import {matchesProfile, compareProfiles} from './filter-core.mjs';
const themeButton = document.querySelector('.theme-toggle');
function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  themeButton?.setAttribute('aria-pressed', String(theme === 'dark'));
}
try {
  if (localStorage.getItem('trailblazers-theme') === 'dark') applyTheme('dark');
} catch {
  // The theme still works when browser storage is unavailable.
}
themeButton?.addEventListener('click', () => {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  try {
    localStorage.setItem('trailblazers-theme', next);
  } catch {
    // Keep the theme active for this page.
  }
});

const search = document.querySelector('#search');
const category = document.querySelector('#category');
const era = document.querySelector('#era');
const region = document.querySelector('#region');
const sort = document.querySelector('#sort');
const grid = document.querySelector('#card-grid');
const cards = grid ? [...grid.querySelectorAll('.person-card')].map(element => ({
  element,
  profile: JSON.parse(element.dataset.profile),
})) : [];
const count = document.querySelector('#result-count');
const empty = document.querySelector('#empty-state');
let currentSort;
function updateCollection() {
  if (!grid) return;
  let shown = 0;
  const filters = {search: search.value, category: category.value, era: era.value, region: region.value};
  for (const { element, profile } of cards) {
    const matches = matchesProfile(profile, filters);
    element.hidden = !matches;
    if (matches) shown++;
  }
  if (sort.value !== currentSort) {
    currentSort = sort.value;
    const ordered = [...cards].sort((a, b) => compareProfiles(a.profile, b.profile, currentSort));
    grid.replaceChildren(...ordered.map(card => card.element));
  }
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
  search.focus({preventScroll: true});
  document.querySelector('#collection').scrollIntoView();
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
  const today = new Date();
  const ordinal = Date.UTC(today.getFullYear(), today.getMonth(), today.getDate()) / 86400000 + 719163;
  const { element: dailyCard, profile: person } = cards[ordinal % cards.length];
  dailyPanel.querySelector('p').textContent = person.summary;
  const dailyLink = dailyPanel.querySelector('.button');
  dailyLink.href = dailyCard.querySelector('.card-link').href;
  dailyLink.firstChild.textContent = `Meet ${person.name} `;
  dailyPanel.querySelector('.daily-name strong').textContent = person.name;
  dailyPanel.querySelector('.daily-name > span').textContent = person.categories[0];
  const oldPortrait = dailyPanel.querySelector('.daily-name .portrait-frame, .daily-name .portrait--type');
  const newPortrait = dailyCard.querySelector('.portrait-frame, .portrait--type').cloneNode(true);
  oldPortrait.replaceWith(newPortrait);
}

document.querySelectorAll('.portrait-frame img').forEach(image => {
  function showFallback() {
    image.hidden = true;
    const frame = image.parentElement;
    frame.querySelector('.credit').hidden = true;
    frame.querySelector('.portrait--type').hidden = false;
  }
  image.addEventListener('error', showFallback);
  if (image.complete && image.naturalWidth === 0) showFallback();
});
