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
  if (sort === 'born') return (a.born || '9999').localeCompare(b.born || '9999') || a.name.localeCompare(b.name);
  if (sort === 'period') return String(a.milestones[0].year).localeCompare(String(b.milestones[0].year)) || a.name.localeCompare(b.name);
  return a.name.localeCompare(b.name);
}
