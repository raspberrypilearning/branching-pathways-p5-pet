const KEY = 'branching-pathways-p5-pet-v1';
const main = document.querySelector('#main');
const nav = document.querySelector('#site-nav');
const notice = document.querySelector('#notice');
let data;
let project = {version: 1, kind: 'p5-pet-notes', ready: false, checks: {}, notes: {}, name: 'My pet'};
let returnTo = null;
let pending = null;

const esc = value => String(value ?? '').replace(/[&<>"']/g, letter => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[letter]));
const stages = () => data.groups.filter(group => group.slug !== 'setup');
const groupFor = id => data.groups.find(group => group.options.some(option => option.id === id));
const groupRoute = group => group.options.length === 1 ? 'step/' + group.options[0].id : group.slug;
const validRoute = route => route === 'home' || route === 'hub' || stages().some(group => group.slug === route) || /^step\/\d+[A-Z]$/.test(route) && !!data.pages[route.slice(5)];
const currentRoute = () => {
  let route;
  try {route = decodeURIComponent(location.hash.slice(1)) || 'home';}
  catch {return 'home';}
  return validRoute(route) ? route : 'home';
};
const pageId = () => currentRoute().startsWith('step/') ? currentRoute().slice(5) : null;
const ready = () => project.ready && project.checks['1A'];

const paths = {
  home: 'M3 10l9-7 9 7v11H3V10m6 11v-8h6v8',
  pico: 'M6 3h12v18H6zM9 7h6v6H9zM3 6h3m-3 6h3m-3 6h3M18 6h3m-3 6h3m-3 6h3',
  grid: 'M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z',
  dial: 'M12 4a8 8 0 110 16 8 8 0 010-16m0 8l4-5',
  speaker: 'M4 10v4h4l6 5V5l-6 5H4m13-2c3 2 3 6 0 8m3-11c5 4 5 10 0 14',
  connect: 'M2 7h6v10H2zM16 7h6v10h-6zM8 12h8m-5-3l3 3-3 3',
  shape: 'M3 7l9-5 9 5v12l-9 3-9-3V7m0 0l9 5 9-5M12 12v10',
  repeat: 'M20 8a8 8 0 00-14-3L3 8m0-6v6h6M4 16a8 8 0 0014 3l3-3m0 6v-6h-6',
  spark: 'M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3z',
  code: 'M8 5l-6 7 6 7m8-14l6 7-6 7M14 3l-4 18',
  toggle: 'M7 6h10a6 6 0 010 12H7A6 6 0 017 6m1 3a3 3 0 110 6 3 3 0 010-6',
  wave: 'M2 12c4-12 6 12 10 0s6 12 10 0',
  plus: 'M12 3v18M3 12h18',
  pencil: 'M4 15L16 3l5 5L9 20l-6 1zM13 6l5 5M4 15l5 5',
  reuse: 'M4 8l4-5 4 5M8 3v13a5 5 0 005 5h7M20 16l-4 5',
  treasure: 'M3 10h18v11H3zM3 10V8a9 6 0 0118 0v2M10 10v5h4v-5',
  tilt: 'M3 15L15 3l7 7-12 12zM2 5h5V1'
};
paths.pet = 'M4 9l-1-6 6 4m6 0l6-4-1 6M4 9c-3 11 19 11 16 0M8 12h.01M16 12h.01M10 16h4';
const icon = name => `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${paths[name] || paths.spark}"/></svg>`;
const routeTitle = route => route.startsWith('step/') ? data.pages[route.slice(5)]?.title : stages().find(group => group.slug === route)?.title;

function toast(message) {
  notice.textContent = message;
  notice.classList.add('visible');
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => notice.classList.remove('visible'), 4000);
}
function persist() {
  try {localStorage.setItem(KEY, JSON.stringify(project));}
  catch {toast('Browser saving is unavailable. Use Save notes.');}
}
function download(contents, filename, type) {
  const url = URL.createObjectURL(new Blob([contents], {type}));
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function restore(value) {
  if (!value || value.version !== 1 || value.kind !== 'p5-pet-notes' || typeof value !== 'object') throw Error('Choose a My p5 Pet notes file.');
  const safe = {version:1, kind:'p5-pet-notes', ready:value.ready === true, checks:{}, notes:{}, name:'My pet'};
  if (typeof value.name === 'string') safe.name = value.name.slice(0, 100);
  if (value.checks && typeof value.checks === 'object' && !Array.isArray(value.checks))
    for (const [key, done] of Object.entries(value.checks))
      if (data.pages[key] && typeof done === 'boolean') safe.checks[key] = done;
  if (value.notes && typeof value.notes === 'object' && !Array.isArray(value.notes))
    for (const [key, text] of Object.entries(value.notes))
      if (data.pages[key] && typeof text === 'string') safe.notes[key] = text.slice(0, 10000);
  if (!safe.checks['1A']) safe.ready = false;
  return safe;
}
function navigation() {
  const route = currentRoute();
  const active = pageId() ? groupFor(pageId())?.slug : route;
  const navLink = (to, title, symbol, selected, status = '') => `<a class="nav-link ${selected ? 'current' : ''}" href="#${to}" ${selected ? 'aria-current="page"' : ''}>${icon(symbol)}<span>${title}</span>${status}</a>`;
  nav.innerHTML = `<div class="nav-links">
    ${navLink('home', 'Start', 'home', route === 'home')}
    ${navLink('step/1A', 'Meet your pet', 'code', active === 'setup', ready() ? '<span class="nav-status" aria-label="Starter tested">✓</span>' : '')}
    <span class="nav-label">YOUR PET · YOUR CHOICES</span>
    ${navLink('hub', 'Choose a part', 'grid', route === 'hub')}
    ${stages().map(group => navLink(groupRoute(group), esc(group.title), group.icon, active === group.slug)).join('')}
    </div><div class="sidebar-note"><strong>Your route.</strong><p>Change direction whenever you like.</p><small>Save your Python in the editor. Save your notes here.</small></div>
    <a class="source-link" href="https://github.com/raspberrypilearning/python-bytes" target="_blank" rel="noopener">Inspired by Python Bytes ↗</a>`;
  const links = nav.querySelector('.nav-links');
  const current = nav.querySelector('[aria-current]');
  if (current && links.scrollWidth > links.clientWidth)
    links.scrollLeft = Math.max(0, current.offsetLeft - links.clientWidth / 2 + current.offsetWidth / 2);
}
function returnBanner(id = null) {
  return returnTo && returnTo !== id && data.pages[returnTo] ? `<div class="return-banner">Explore this help, then return whenever you like. <a href="#step/${returnTo}" data-return>Return to ${esc(data.pages[returnTo].title)} →</a></div>` : '';
}
function renderHome() {
  return `<section class="hero"><div class="hero-copy"><span class="eyebrow">BRANCHING PATHWAYS · PYTHON + P5</span><h1>A little creature.<br><em>A lot of personality.</em></h1><p>Code a pet that reacts to you. Its look, moves and moods are yours to invent.</p><div class="actions"><a class="button primary" href="${ready() ? '#hub' : '#step/1A'}">${ready() ? 'Back to my pet' : 'Meet your starter pet'} →</a><a class="quiet-link" href="#ideas">Ideas to borrow</a></div><p class="small">First, run your pet. Then start wherever you like.</p></div>
    <div class="hero-art"><img src="assets/pet-maker.svg" alt="Three invented pets: a bouncy purple creature, a sleepy green blob and a little yellow robot."></div></section>
    <div class="intro-strip"><strong>One pet. Your route.</strong><span>Draw, move or play — your next choice is yours.</span></div>
    <section class="panel start-with"><h2>Start with</h2><p>A computer, a web browser and your imagination. You will write Python with p5 in the Raspberry Pi Code Editor.</p></section>`;
}
function renderHub() {
  return `${returnBanner()}<div class="page-head"><span class="eyebrow">YOUR PET</span><h1>Where will you start?</h1><p>Pick a part. You can change direction at any time.</p></div>
    <div class="hub-note"><span class="status-dot"></span><strong>Starter tested</strong><a href="#step/1A">Check it again</a><span class="push">Your creature. Your code. Your choices.</span></div>
    <div class="parts-grid">${stages().map(group => `<a class="part-card tone-${group.tone}" href="#${groupRoute(group)}"><div class="part-top">${icon(group.icon)}<span class="arrow" aria-hidden="true">↗</span></div><h2>${esc(group.title)}</h2><span class="part-sub">${esc(group.subtitle)}</span><p>${esc(group.description)}</p></a>`).join('')}</div>`;
}
function renderGroup(group) {
  const components = group.options.some(option => option.image);
  return `${returnBanner()}<div class="page-head"><a class="back-link" href="#hub">← Your choices</a><span class="eyebrow">YOUR PET · ${esc(group.title)}</span><h1>${esc(group.title)}</h1><p>${esc(group.description)} ${components ? 'Pick a part to change.' : 'Pick an idea to try. You can change it as you go.'}</p></div>
    ${group.slug === 'ideas' ? '<p class="hub-note">These are examples. Mix their ideas or invent your own.</p>' : ''}
    <div class="${components ? 'component-grid' : 'choice-grid'}">${group.options.map(option => `<a class="${components ? 'component-card' : 'choice-card tone-' + group.tone}" href="#step/${option.id}">
      ${option.image ? `<img src="images/components/${esc(option.image)}" alt="" loading="lazy" width="240" height="160">` : `<div class="part-top">${icon(option.icon || group.icon)}<span class="arrow" aria-hidden="true">↗</span></div>`}
      <div class="card-copy"><h2>${esc(option.title)}</h2><p>${esc(option.description || '')}</p><span class="card-action">${components ? 'Try this idea' : 'Explore this idea'} <span aria-hidden="true">→</span>${project.checks[option.id] ? '<span class="tried">Tried ✓</span>' : ''}</span></div>
    </a>`).join('')}</div>`;
}
function renderStep(id) {
  const page = data.pages[id];
  const group = groupFor(id);
  const setup = id === '1A';
  const back = setup ? ready() ? 'hub' : 'home' : group.options.length === 1 ? 'hub' : group.slug;
  return `<div class="page-head breadcrumb"><a class="back-link" href="#${back}">← ${back === 'home' ? 'Start' : setup || back === 'hub' ? 'Your choices' : esc(group.title)}</a><span class="eyebrow">${esc(group.title)}</span><a class="editor-link" href="https://editor.raspberrypi.org/en/" target="_blank" rel="noopener">Open Code Editor ↗</a></div>${returnBanner(id)}
    <article class="learner-page layout-${group.slug}"><div class="lesson-intro"><h1>${esc(page.title)}</h1>${page.intro}</div>
      <div class="lesson-grid">${page.sections.map(section => `<section class="lesson-section section-${section.key}"><h2>${esc(section.title)}</h2>${section.html}</section>`).join('')}</div>
    </article><section class="panel record"><h2>${setup ? 'Did your pet react?' : 'Keep track of this idea'}</h2><label class="check-row"><input id="page-check" type="checkbox" ${project.checks[id] ? 'checked' : ''}><span>${setup ? 'I ran the starter and made my pet react to a click.' : 'I tried this idea.'}</span></label>${setup ? '<p class="small">Tick this after your pet reacts. Then choose any part.</p>' : `<details class="optional-note" ${project.notes[id] ? 'open' : ''}><summary>My notes (optional)</summary><label class="note-label" for="page-note">What will you try next?</label><textarea id="page-note" rows="3">${esc(project.notes[id] || '')}</textarea></details>`}<div class="actions"><a class="button primary" href="#hub">${setup ? 'Open the choices' : 'Choose another part'} →</a>${returnTo && returnTo !== id ? `<a class="button" href="#step/${returnTo}" data-return>Return to my earlier idea</a>` : ''}</div></section>`;
}
function render() {
  const route = currentRoute();
  const id = pageId();
  if (!ready() && route !== 'home' && id !== '1A') {
    pending = route;
    main.innerHTML = `<div class="page-head"><span class="eyebrow">START HERE</span><h1>Meet your pet first</h1><p>Run the pet starter and try its click reaction. Then every pathway is open.</p></div><div class="panel"><p>We’ll keep your place: <strong>${esc(routeTitle(route) || 'your choices')}</strong>.</p><a class="button primary" href="#step/1A">Open the starter →</a></div>`;
  } else if (route === 'home') main.innerHTML = renderHome();
  else if (route === 'hub') main.innerHTML = renderHub();
  else if (!id) main.innerHTML = renderGroup(stages().find(group => group.slug === route));
  else main.innerHTML = renderStep(id);
  navigation();
  document.title = `${routeTitle(route) || (route === 'hub' ? 'Choose a part' : 'My p5 Pet')} · Branching pathways`;
}
document.addEventListener('click', async event => {
  const target = event.target;
  if (target.closest('.skip-link')) {
    event.preventDefault();
    main.focus();
    return;
  }
  const copy = target.closest('.copy-code');
  if (copy) {
    const code = copy.closest('.code-wrap').querySelector('code').textContent;
    try {await navigator.clipboard.writeText(code); toast('Code copied.');}
    catch {toast('Select the code to copy it.');}
  }
  const link = target.closest('a');
  if (link?.hasAttribute('data-prereq') && pageId()) returnTo = pageId();
  if (link?.hasAttribute('data-return')) returnTo = null;
});
document.addEventListener('change', event => {
  if (event.target.id === 'page-check') {
    const id = pageId();
    project.checks[id] = event.target.checked;
    if (id === '1A') project.ready = event.target.checked;
    persist();
    if (id === '1A' && ready() && pending) {
      const destination = pending;
      pending = null;
      location.hash = destination;
    } else {
      render();
      document.querySelector('#page-check')?.focus({preventScroll:true});
    }
  }
});
document.addEventListener('input', event => {
  if (event.target.id === 'page-note') {
    project.notes[pageId()] = event.target.value.slice(0, 10000);
    persist();
  }
});
document.querySelector('#save-project').addEventListener('click', () => download(JSON.stringify(project, null, 2), 'p5-pet-notes.json', 'application/json'));
document.querySelector('#open-project').addEventListener('click', () => document.querySelector('#project-file').click());
document.querySelector('#project-file').addEventListener('change', async event => {
  const file = event.target.files[0];
  if (!file) return;
  try {
    if (file.size > 500000) throw Error('That notes file is too large.');
    const next = restore(JSON.parse(await file.text()));
    download(JSON.stringify(project, null, 2), 'p5-pet-notes-before-import.json', 'application/json');
    project = next;
    persist();
    location.hash = ready() ? '#hub' : '#step/1A';
    render();
    toast('Notes opened. Your previous notes were downloaded.');
  } catch (error) {toast(error.message || 'Could not open those notes. Your work is unchanged.');}
  event.target.value = '';
});
window.addEventListener('hashchange', () => {render(); window.scrollTo(0, 0); main.focus({preventScroll:true});});
try {
  const response = await fetch('data/pages.json?v=1');
  if (!response.ok) throw Error('Page data unavailable');
  data = await response.json();
  try {const saved = localStorage.getItem(KEY); if (saved) project = restore(JSON.parse(saved));}
  catch {toast('Saved notes could not be opened. You can import a notes file.');}
  render();
} catch {
  main.innerHTML = '<h1>The pathway could not load</h1><p>Try reloading the page, or use the <a href="en/landing.md">Markdown project</a>.</p>';
}
