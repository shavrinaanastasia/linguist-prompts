"""Build per-document and per-code correction proposals from the document-level pass."""
import csv, json, re, sys, collections
from pathlib import Path

doc_json, audit_csv, manual_csv, written_json, out_dir = sys.argv[1:6]
out = Path(out_dir)
D = json.load(open(doc_json, encoding='utf-8')); R = D['rows']
audit = {r['code']: r for r in csv.DictReader(open(audit_csv, encoding='utf-8'))}
manual = {r['код']: r for r in csv.DictReader(open(manual_csv, encoding='utf-8'))}
isoname = {x['iso639_3']: (x['name'] or '') for x in json.load(open(written_json, encoding='utf-8'))}
EXTRA_NAMES = {'cic':'Chickasaw','sgh':'Shughni (Bartangi)','pus':'Pashto','omn':'Minoan (Linear A)','mqb':'Mbuko','ozm':'Koonzime',
 'pyu':'Puyuma','ckv':'Kavalan','avk':'Kotava','luo':'Dholuo','xpr':'Parthian','bnn':'Bunun','szy':'Sakizaya','moe':'Innu (Montagnais)',
 'atj':'Atikamekw','tzj':"Tz'utujil",'kjb':"Q'anjob'al",'smp':'Samaritan Hebrew','fla':'Kalispel-Pend d\'Oreille','gaz':'West Central Oromo',
 'meq':'Merey','nnh':'Ngiemboon','tcy':'Tulu','auv':'Auvergnat','xsy':'Saisiyat','pra':'Prakrit','raj':'Rajasthani','ava':'Avar','tat':'Tatar',
 'gle':'Irish','tsg':'Tausug','cak':'Kaqchikel','kek':"Q'eqchi'",'lzz':'Laz','rmy':'Vlax Romani','rhg':'Rohingya','ayc':'Southern Aymara',
 'acr':'Achi','see':'Seneca','sei':'Seri','cku':'Koasati','rma':'Rama','tae':'Tariana','fng':'Fanagalo','hnn':'Hanunoo','grt':'Garo','nmy':'Namuyi',
 'tms':'Tima','tjm':'Timucua','roo':'Rotokas','cal':'Carolinian','tzh':'Tzeltal','trv':'Seediq','xmr':'Meroitic','brx':'Bodo','stq':'Saterfriesisch','kdr':'Karaim'}
name = lambda c: EXTRA_NAMES.get(c) or isoname.get(c) or ''

HIST = {('goh','deu'),('ang','gle'),('enm','gle'),('peo','fas'),('peo','sgh'),('grc','omn'),('sga','gle'),('jav','kaw'),('arc','akk'),('pal','pli')}
RELATED = {('prs','pus'),('fas','pus'),('pes','pus'),('ttt','tat'),('tzo','tzj'),('tzu','tzj'),('quc','cak'),('quc','kek'),('avx','ava'),
           ('tgl','tsg'),('sco','gle'),('sco','gla'),('tzo','tzh'),('dho','luo'),('raj','guj'),('csw','cic'),('chm','ccc'),('aym','ayc'),('rom','rmy'),('nah','nhe')}

def subseq(code, nm):
    s = re.sub(r'[^a-z]', '', nm.lower())
    if not s or s[0] != code[0]: return False
    it = iter(s); return all(ch in it for ch in code)

def etype(label, prop, *names):
    if (label, prop) in HIST: return 'historical_stage'
    if any(n and subseq(label, w) for n in names for w in re.split(r'[ ()/,-]+', n)): return 'code_from_name'
    if (label, prop) in RELATED: return 'related_or_neighbour_language'
    return 'wrong_language'

# per-code aggregation
by = collections.defaultdict(list)
for r in R: by[r[0]].append(r)
code_rows = []; code_type = {}
for code, rows in by.items():
    n = len(rows); conf = sum(r[6]=='label_confirmed' for r in rows)
    other = collections.Counter((r[7], r[8]) for r in rows if r[6]=='other_language_named')
    n_other = sum(other.values())
    top = other.most_common(3)
    best, best_name = (top[0][0] if top else ('',''))
    share = round(100*top[0][1]/n) if top else 0
    m = manual.get(code)
    if m and m['вероятный код'] not in ('—',''):
        mcode = m['вероятный код'].split(' ')[0].split('/')[0].strip()
    else: mcode = ''
    proposed = mcode if (mcode and len(mcode)==3) else (best if share >= 30 else '')
    if proposed == code: proposed = ''
    t = etype(code, proposed, name(proposed), best_name) if proposed else ''
    if proposed: code_type[code] = t
    level = ('verified' if m else ('high' if share>=70 and n>=5 else 'medium' if share>=30 and n>=3 else 'low'))
    ex = next((r for r in rows if r[6]=='other_language_named' and r[7]==proposed), None) or next((r for r in rows if r[6]=='other_language_named'), None)
    code_rows.append(dict(label_code=code, label_name=audit.get(code,{}).get('ref_name','') or name(code), docs_in_catalogue=audit.get(code,{}).get('total',n),
        docs_checked=n, label_confirmed_pct=round(100*conf/n), other_language_pct=round(100*n_other/n),
        proposed_code=proposed, proposed_name=name(proposed) or best_name, proposed_share_pct=share if proposed==best else '',
        error_type=t, confidence=level, other_candidates='; '.join(f"{c}:{k}" for (c,_),k in top),
        example=(f"{ex[2]}: {ex[3]}" if ex else ''), manual_note=(m['что на самом деле'] if m else '')))
for code, m in manual.items():
    if code in by or 'ошибка' not in m['вердикт']: continue
    mcode = m['вероятный код'].split(' ')[0].split('/')[0].strip()
    if len(mcode)!=3: continue
    t = etype(code, mcode, name(mcode), m['что на самом деле'])
    if code=='goh': t='historical_stage'
    code_type[code]=t
    code_rows.append(dict(label_code=code, label_name=audit.get(code,{}).get('ref_name',''), docs_in_catalogue=audit.get(code,{}).get('total',m['документов']),
        docs_checked='', label_confirmed_pct='', other_language_pct='', proposed_code=mcode, proposed_name=name(mcode), proposed_share_pct='',
        error_type=t, confidence='verified', other_candidates='', example='', manual_note=m['что на самом деле']+' — '+m['основание']))
OVERRIDE = {'bil': ('', 'low', '', 'смешанный код: латынь (Саллюстий), турецкий, билокси (`bll`) — у каждого документа свой язык, замена для кода целиком не подходит'),
            'avx': ('tab', 'medium', 'wrong_language', 'аннотации модели называют аварский, но по словоформам (апIиди, ляхин) тексты похожи на табасаранский — нужна ручная проверка')}
for r in code_rows:
    if r['label_code'] in OVERRIDE:
        c, conf, t, note = OVERRIDE[r['label_code']]
        r.update(proposed_code=c, proposed_name=(name(c) or 'Tabasaran') if c else '', proposed_share_pct='', confidence=conf, error_type=t, manual_note=note)
        code_type[r['label_code']] = t
code_rows.sort(key=lambda r: (-int(r['docs_in_catalogue']) if str(r['docs_in_catalogue']).isdigit() else 0))
with open(out/'proposed_corrections_by_code.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=list(code_rows[0].keys())); w.writeheader(); w.writerows(code_rows)

# per-document
doc_rows = []
for r in R:
    label, basis = r[0], r[6]
    if basis == 'label_confirmed':
        prop, pname, conf, et = label, name(label) or r[1], 'keep', ''
    elif basis == 'other_language_named':
        prop, pname = r[7], name(r[7]) or r[8]; et = etype(label, prop, pname, r[8])
        cr = next((c for c in code_rows if c['label_code']==label), None)
        if label in OVERRIDE and OVERRIDE[label][0]: prop, pname, et = OVERRIDE[label][0], 'Tabasaran', OVERRIDE[label][2]
        conf = 'high' if (cr and cr['proposed_code']==prop and cr['confidence'] in ('verified','high')) else 'medium'
    else:
        cr = next((c for c in code_rows if c['label_code']==label), None)
        prop = cr['proposed_code'] if cr and cr['confidence'] in ('verified','high') else ''
        pname = name(prop) if prop else ''; conf = 'low (by code)' if prop else 'review'
        et = code_type.get(label,'') if prop else ''
    # keep other languages of the document, replacing only the wrong label
    wl = [x for x in r[5].split(',') if x]
    new_wl = [prop if (x==label and prop) else x for x in wl] if prop else wl
    doc_rows.append(dict(doc_id=r[2], title=r[3], format=r[4], label_code=label, label_name=r[1],
        current_written_languages=r[5], proposed_code=prop, proposed_name=pname, proposed_written_languages=','.join(dict.fromkeys(new_wl)),
        basis=basis, error_type=et, confidence=conf, summary_excerpt=r[10]))
with open(out/'proposed_corrections_by_document.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=list(doc_rows[0].keys())); w.writeheader(); w.writerows(doc_rows)
print(len(code_rows), len(doc_rows), collections.Counter(d['confidence'] for d in doc_rows), collections.Counter(c['error_type'] for c in code_rows if c['proposed_code']))
