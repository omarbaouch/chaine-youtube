import json, re, sys, collections
B='/home/claude/chaine-youtube/videos/baguette/'
P=json.load(open(B+'plans_v2.json'))
CODES=json.load(open(B+'_workspace/00_codes_refs.json'))
ALL={v['ref'] for pl in CODES.values() for v in pl.values()}
REG=json.load(open(B+'_workspace/reglages_v6.json'))
for k,x in REG.items():
    if k.startswith('p'):
        ALL|=({x['media_ref']} if 'media_ref' in x else set())|{m['media_ref'] for m in x.get('medias',[])}
err=[]
# formats consécutifs
for a,b in zip(P,P[1:]):
    if a['format']==b['format']: err.append(f"format identique consécutif {a['id']}->{b['id']} ({a['format']})")
# ids
ids=[p['id'] for p in P]
for i,c in collections.Counter(ids).items():
    if c>1: err.append(f"id en double {i}")
for i in ids:
    if not re.fullmatch(r'p\d{3}b?',i): err.append(f"id mal formé {i}")
# refs (en tenant compte des réglages qui remplacent les médias)
def refs_of(p):
    r=[]
    reg=REG.get(p['id'],{})
    if 'media_ref' in reg: r.append(reg['media_ref'])
    elif p.get('media_ref'): r.append(p['media_ref'])
    meds=reg.get('medias',p.get('medias',[]))
    r+= [m['media_ref'] for m in meds]
    return r
used=collections.Counter()
EXEMPT={'pi:3277831'}  # baguette coupée (o01 + retours decoupe)
for p in P:
    for r in refs_of(p):
        used[r]+=1
        if r not in ALL: err.append(f"ref inconnue {p['id']} {r}")
# réglages : médias des clés p0xx comptent comme utilisés même si le plan n'est pas repris
ids_set=set(ids)
for k,v in REG.items():
    if not k.startswith('p') or k in ids_set: continue
    for r in ([v['media_ref']] if 'media_ref' in v else [])+[m['media_ref'] for m in v.get('medias',[])]:
        used[r]+=1
for o in REG['_avant']:
    if o.get('media_ref'): used[o['media_ref']]+=1
for r,c in used.items():
    if c>1 and r not in EXEMPT: err.append(f"ref en double x{c} {r}")
for p in P:
    if p.get('schema',{}).get('type')!='decoupe' and 'pi:3277831' in refs_of(p): err.append(f"pi:3277831 hors decoupe {p['id']}")
# textes
def phrases(t):
    # fin de phrase : . ! ? (et « … » suivi d'une majuscule)
    t=t.replace('»','').replace('«','')
    parts=re.split(r'(?<=[.!?])\s+|…\s+(?=[A-ZÉÈÀÂ])',t.strip())
    return [x for x in parts if x.strip()]
nmots=0
for p in P:
    t=p.get('texte')
    if not t: continue
    if re.search(r'\d',t): err.append(f"chiffre dans le texte {p['id']}")
    w=len(t.replace('«','').replace('»','').split()); w=len([x for x in t.split() if re.search(r'\w',x)])
    nmots+=w
    if not 6<=w<=22: err.append(f"longueur {p['id']} {w} mots")
    for ph in phrases(t):
        n=len([x for x in ph.split() if re.search(r'\w',x)])
        if n<6: err.append(f"phrase courte {p['id']} ({n}) : {ph}")
    if p.get('voix')=='sceptique' and w<8: err.append(f"sceptique trop court {p['id']}")
    if re.search(r'(^|[.!?…]\s+)(Puis|Et puis)\b',t): err.append(f"« Puis » en tête {p['id']}")
for p in P:
    if 'ambiance' not in p or p['ambiance'] not in ('tension','emotion','revelation','leger'): err.append(f"ambiance {p['id']}")
    st=p.get('schema',{}).get('type')
    if st=='devine' and (p.get('texte') or p.get('duree_min')!=5): err.append(f"devine mal formé {p['id']}")
    if st in('suspect','loupe','piece') and not re.match(r'(pi|wc):',p.get('media_ref','')): err.append(f"{st} sans photo {p['id']}")
    if p.get('sons') and not p.get('texte') and p['format']!='titre' and st!='devine' and p.get('duree_min')!=2.5: err.append(f"silence mal formé {p['id']}")
# devine -> plan suivant a un texte
for a,b in zip(P,P[1:]):
    if a.get('schema',{}).get('type')=='devine' and not b.get('texte'): err.append(f"pas de révélation après {a['id']}")
# comptes
cnt=collections.Counter()
for p in P:
    st=p.get('schema',{}).get('type')
    if st in('devine','suspect','decoupe','piece','loupe'): cnt[st]+=1
    if st=='suspect' and p['schema'].get('verdict'): cnt['suspect (verdict)']+=1
    if p.get('voix')=='sceptique': cnt['sceptique']+=1
    if not p.get('texte') and p['format']=='rush': cnt['silence']+=1
    if p.get('punch'): cnt['punch']+=1
    if p['format']=='titre': cnt['titre']+=1
fmts=collections.Counter(p['format'] for p in P)
photos=sum(1 for p in P for r in refs_of(p) if not r.startswith('pv:'))
videos=sum(1 for p in P for r in refs_of(p) if r.startswith('pv:'))
# durée
voix_s=nmots/(150*1.05)*60
sil=sum(p.get('duree_min',0) for p in P if not p.get('texte'))
resp=0.15*len(P)
print(f"plans={len(P)} mots={nmots} voix≈{voix_s:.0f}s sans-voix={sil:.1f}s resp={resp:.0f}s TOTAL≈{(voix_s+sil+resp)/60:.2f} min (+ o01/o02)")
print("moments:",dict(cnt)); print("formats:",dict(fmts)); print(f"médias: photos={photos} vidéos={videos}")
print("ERREURS:",len(err)); [print(' -',e) for e in err]
