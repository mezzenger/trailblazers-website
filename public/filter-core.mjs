export function normalize(value) {
  return String(value ?? '').toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
}
export function matchesProfile(profile, filters) {
  const searchable = [profile.name, profile.summary, ...(profile.achievements || [])].join(' ');
  return normalize(searchable).includes(normalize(filters.search))
    && (!filters.category || profile.categories.includes(filters.category))
    && (!filters.era || profile.era === filters.era)
    && (!filters.region || profile.region === filters.region);
}
export function compareProfiles(a, b, sort = 'name') {
  const byName = a.name.localeCompare(b.name, 'en');
  if (sort === 'born') {
    if (!a.born || !b.born) return Number(!a.born) - Number(!b.born) || byName;
    return a.born.localeCompare(b.born) || byName;
  }
  if (sort === 'period') return earliestMilestone(a) - earliestMilestone(b) || byName;
  return byName;
}

function earliestMilestone(profile) {
  return Math.min(...profile.milestones.map(milestone => milestone.year));
}
