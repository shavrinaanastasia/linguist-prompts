// Audit of the "Written in" language labels of the corpus catalogue.
//
// Run in the browser console on any page of the catalogue, after logging in
// (the API uses HTTP Basic auth, so the browser session supplies credentials;
// nothing secret is stored in this script). API_ROOT is the catalogue path prefix.
//
// For every ISO code returned by /api/languages?kind=written the script samples
// up to 1000 documents (page 1 + one random page of 500) and checks whether the
// LLM-written title/summary of each document names the labelled language,
// names a different language, or names no language at all.
// The result is downloaded as written_language_audit_full.json.

const API_ROOT = '/corpus/api';

// Languages used to describe other languages; mentioning them in a summary is
// not evidence against a label.
const META = new Set(['eng', 'fra', 'spa', 'por', 'rus', 'deu', 'zho', 'ita', 'cmn', 'nld', 'lat', 'ara']);

// Codes that refer to the same language (macrolanguage / B-code / dialect).
const GROUPS = [['ara','arb','arz','apc','ary','aeb','arq','ajp','acm','shu'],['fas','pes','prs','tgk'],['msa','zsm','ind','zlm'],['nep','npi'],['aze','azj','azb'],['zho','cmn','lzh','yue','och','nan'],['est','ekk'],['yid','ydd'],['swa','swh'],['ori','ory'],['kur','kmr','ckb'],['gon','esg'],['cre','crk','crj','csw','crl','crm','crx'],['oji','ojb','ojs','ojc','ojg','ojw','alq'],['deu','ger','gmh','nds','pdc','gsw','bar'],['nld','dut','dum'],['ron','rum','mol'],['eng','sco','enm','ang'],['gle','sga','mga','gla'],['san','pli','pra','inc','vsn'],['hin','urd','hns','bra','awa','bho','raj','mwr'],['sqi','alb','als','aln'],['hye','arm','xcl','hyw'],['mya','bur'],['bod','tib'],['ell','gre','grc'],['kat','geo'],['mkd','mac'],['fra','fre','fro','frm'],['ces','cze'],['slk','slo'],['isl','ice'],['cym','wel'],['eus','baq'],['mri','mao'],['nor','nob','nno'],['hbs','srp','hrv','bos'],['que','quz','quy'],['grn','gug'],['kom','kpv','koi'],['chm','mhr','mrj'],['mon','khk'],['pus','pbt'],['uzb','uzn'],['orm','gax'],['kok','gom'],['twi','aka'],['lav','lvs'],['ful','fuv'],['bua','bxr'],['zap','zai'],['den','scs'],['iku','ike'],['kon','kng'],['man','mnk'],['syr','syc','cld'],['tmh','taq'],['lah','pan'],['doi','dgo']];
const eqOf = c => new Set(GROUPS.find(g => g.includes(c)) || [c]);

// A few names the catalogue reference does not contain, or contains under another spelling.
const EXTRA_NAMES = {Hindi:'hin',Sanskrit:'san',English:'eng',Russian:'rus',German:'deu',French:'fra',Spanish:'spa',Portuguese:'por',Italian:'ita',Latin:'lat',Arabic:'ara',Persian:'fas',Farsi:'fas',Chinese:'zho',Mandarin:'cmn',Japanese:'jpn',Irish:'gle',Gaelic:'gla',Welsh:'cym',Scots:'sco',Cree:'cre',Ojibwe:'oji',Ojibwa:'oji',Prakrit:'pra',Chickasaw:'cic',Puyuma:'pyu',Kavalan:'ckv',Kotava:'avk',Laz:'lzz',Seneca:'see',Seri:'sei',Koasati:'cku',Rama:'rma',Tariana:'tae',Dholuo:'luo',Parthian:'xpr',Bunun:'bnn',Sakizaya:'szy',Montagnais:'moe',Innu:'moe',Koonzime:'ozm',Mbuko:'mqb',Bartangi:'sgh',Saterfriesisch:'stq',Fanagalo:'fng',Hanunoo:'hnn',Garo:'grt',Namuyi:'nmy',Tima:'tms',Timucua:'tjm',Achi:'acr',Rotokas:'roo',Carolinian:'cal',Kaqchikel:'cak',Tzeltal:'tzh',Seediq:'trv',Truku:'trv',Minoan:'omn',Meroitic:'xmr',Kachari:'brx',Talysh:'tly',Tati:'ttt',Kikamba:'kam',Lenape:'unm',Salish:'fla'};
const STOP = ['Standard','Western','Eastern','Northern','Southern','Central','Old','Middle','Modern','Classical','Ancient','North','South','West','East','Early','Upper','Lower','Language','Unknown','Fragment','Dictionary','Grammar','Vulgar','Literary','Sign','Proto','Dialect','Dialects'];

async function getJSON(path) { return (await fetch(API_ROOT + path)).json(); }

async function buildNameIndex() {
  const written = await getJSON('/languages?kind=written&limit=5000');
  const described = await getJSON('/languages?kind=described&limit=5000');
  const dict = {...EXTRA_NAMES};
  const own = {};
  const words = name => String(name || '').split(/[,;/()]/).flatMap(p => p.trim().split(' ')).filter(t => t.length >= 4 && /^[A-ZÀ-Ž]/.test(t) && !STOP.includes(t));
  const add = (name, code) => { if (!code) return; for (const w of words(name)) { if (!(w in dict)) dict[w] = code; (own[code] ||= new Set()).add(w); } };
  for (const x of written) if (x.documents >= 3) add(x.name, x.iso639_3);
  for (const x of described) add(x.name, x.iso639_3);
  for (const [n, c] of Object.entries(dict)) (own[c] ||= new Set()).add(n);
  const re = new RegExp('\\b(' + Object.keys(dict).map(s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')', 'g');
  const refName = Object.fromEntries(written.map(x => [x.iso639_3, x.name || '']));
  return {written, dict, own, re, refName};
}

async function auditCode(code, idx) {
  const q = `/documents?written=${encodeURIComponent(code)}&page_size=500`;
  const p1 = await getJSON(q + '&page=1');
  let items = p1.items; const total = p1.total;
  if (total > 500) {
    const pages = Math.ceil(total / 500);
    const p2 = await getJSON(q + '&page=' + (2 + Math.floor(Math.random() * (pages - 1))));
    items = items.concat(p2.items);
  }
  const eq = eqOf(code); const isMeta = [...eq].some(c => META.has(c));
  const ownNames = new Set([...eq].flatMap(c => [...(idx.own[c] || [])]));
  let prim = 0, match = 0, other = 0, metaOnly = 0, none = 0;
  const oth = {}, othName = {}, fmt = {}, src = {}, firstLang = {}; const examples = [];
  const bump = (o, k) => { o[k] = (o[k] || 0) + 1; };
  for (const it of items) {
    const wl = it.written_languages || [];
    if (wl[0] === code) prim++; else bump(firstLang, wl[0] || '?');
    bump(fmt, it.format);
    for (const s of (it.sources || []).slice(0, 1)) bump(src, s.source || s.name || String(s));
    const text = (it.summary || '') + ' ' + (it.title || '');
    const names = [...text.matchAll(idx.re)].map(m => m[1]);
    let hasOwn = false; for (const n of ownNames) if (text.includes(n)) { hasOwn = true; break; }
    const codes = new Set(names.map(n => idx.dict[n]));
    const nonMeta = [...codes].filter(c => isMeta || !META.has(c));
    if (hasOwn || [...codes].some(c => eq.has(c))) match++;
    else if (nonMeta.length) {
      other++;
      for (const n of names) { const c = idx.dict[n]; if (!isMeta && META.has(c)) continue; bump(oth, c); othName[c] = n; }
      if (examples.length < 2) examples.push(it.id + ': ' + (it.title || '').slice(0, 60).replace(/[\t\n]/g, ' '));
    } else if (codes.size) metaOnly++; else none++;
  }
  const sorted = o => Object.entries(o).sort((a, b) => b[1] - a[1]);
  const top = (o, k = 4) => sorted(o).slice(0, k).map(([a, b]) => a + ':' + b).join(' ');
  const n = items.length || 1, pc = x => Math.round(100 * x / n);
  const best = (sorted(oth)[0] || [null])[0];
  let verdict = 'ok';
  if (['und', 'mis', 'mul', 'zxx'].includes(code)) verdict = 'special';
  else if (pc(other) >= 50 && pc(match) < 25) verdict = 'mislabel';
  else if (pc(other) >= 20) verdict = 'partial';
  else if (pc(match) < 30) verdict = 'unverifiable';
  const flagged = verdict === 'mislabel' || verdict === 'partial';
  return {code, ref_name: idx.refName[code] || '', total, sample: items.length,
    primary_pct: pc(prim), match_pct: pc(match), other_pct: pc(other), meta_only_pct: pc(metaOnly), none_pct: pc(none),
    verdict, suggested: flagged ? (best || '') : '', suggested_name: flagged && best ? othName[best] : '',
    other_langs: top(oth), primary_was: top(firstLang), formats: top(fmt, 3), sources: top(src, 3), examples: examples.join(' ; ')};
}

async function runAudit(concurrency = 4) {
  const idx = await buildNameIndex();
  const codes = idx.written.map(x => x.iso639_3);
  const rows = []; let i = 0;
  const worker = async () => { while (i < codes.length) { const c = codes[i++]; try { rows.push(await auditCode(c, idx)); } catch (e) { console.warn(c, e); } } };
  await Promise.all(Array.from({length: concurrency}, worker));
  const blob = new Blob([JSON.stringify({generated: new Date().toISOString(), rows})], {type: 'application/json'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'written_language_audit_full.json'; a.click();
  return rows.length;
}

// runAudit();
