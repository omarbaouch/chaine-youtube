# Fusionne les choix de repérage (rep/choix-tous.json + rep/choix-G.json) dans videos/chocolat/_workspace/reglages.json puis montage.json
import json, sys, subprocess
D='/tmp/claude-0/-home-claude-chaine-youtube/2312ac68-f703-51cc-be05-364b21395f6f/scratchpad/rep/'
R='/home/claude/chaine-youtube/'
plans=json.load(open(R+'videos/chocolat/plans.json'))
c=json.load(open(D+'choix-tous.json'))
try:
    g=json.load(open(D+'choix-G.json'))
    for k,v in g.items():
        if not v.get('ko'): c[k]={**v, 'video_g': True}
except FileNotFoundError: pass
corr=json.load(open(R+'videos/chocolat/_workspace/corrections_monteur.json'))
reg={"_episode":{"titre":"Chocolat : le cacao s'effondre, ta tablette non",
  "voix":{"moteur":"edge","locuteur":"fr-FR-VivienneMultilingualNeural","debit":"+5%","pause_phrase":0.15,"voix_secondaires":{"sceptique":"fr-FR-RemyMultilingualNeural"}},
  "musique":{"fichier":"../../public/sfx/musique-enquete.wav","volume":0.22},"respiration":0.15,
  "musiques":{"tension":"public/musique/tension.mp3","emotion":"public/musique/emotion.mp3","revelation":"public/musique/revelation.mp3","leger":"public/musique/leger.mp3"},
  "rushes_a_refaire":[]}}
for s in plans:
    v=c.get(s['id'],{}); r={}
    if v.get('media_ref'):
        r['media_ref']=v['media_ref']
    if v.get('medias'):
        refs=[m if isinstance(m,str) else m.get('media_ref') for m in v['medias']]
        if s['format']=='mosaique':
            leg=[m.get('legende') for m in s.get('medias',[])]
            r['medias']=[{k:x for k,x in {'media_ref':ref,'legende':(leg[i] if i<len(leg) else None)}.items() if x} for i,ref in enumerate(refs)]
        else:
            r['media_ref']=refs[0]
    if 'zone' in v and s.get('schema',{}).get('type') in ('decoupe','piece'):
        r['schema']={**s['schema'],'zone':v['zone'],'zone_y':v.get('zone_y')}
    r.update(corr.get(s['id'],{}))
    reg[s['id']]=r
json.dump(reg,open(R+'videos/chocolat/_workspace/reglages.json','w'),ensure_ascii=False,indent=1)
subprocess.run(['python3','scripts/plans_vers_montage.py','chocolat','videos/chocolat/_workspace/reglages.json'],cwd=R,check=True)
m=json.load(open(R+'episodes/chocolat/montage.json'))
manque=[x['id'] for x in m['scenes'] if not x.get('media_ref') and not x.get('medias') and not x.get('fichier')]
from collections import Counter
refs=[x.get('media_ref') for x in m['scenes'] if x.get('media_ref')]+[y.get('media_ref') for x in m['scenes'] for y in x.get('medias',[])]
print('sans média:',manque); print('doublons:',[k for k,n in Counter(refs).items() if n>1])
vid=sum(1 for r in refs if r.startswith('pv:') or r.lower().endswith(('.webm','.ogv','.mp4')))
print(f'vidéos {vid}/{len(refs)}')
