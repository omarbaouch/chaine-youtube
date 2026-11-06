# Construit episodes/capsules/montage.json à partir de capsules_scenes.py + choix des rushes (choix_capsules.json)
import json, copy, sys, importlib
sys.path.insert(0, '/tmp/claude-0/-home-claude/3e299887-a5a8-5943-804a-16a7d66faba1/scratchpad')
import capsules_scenes as c
choix = json.load(open('/tmp/claude-0/-home-claude/3e299887-a5a8-5943-804a-16a7d66faba1/scratchpad/choix_capsules.json'))
ess = json.load(open('/home/claude/chaine-youtube/episodes/essence/montage.json'))
m = {k: v for k, v in ess.items() if k != 'scenes'}
m['titre'] = "Capsule de café : combien tu la paies au kilo, et qui garde l'argent"
vus, scenes, manque = {}, [], []
for s in c.S:
    s = copy.deepcopy(s)
    ref = choix.get(s['id'])
    if s['format'] == 'mosaique':
        refs = ref or []
        if len(refs) < len(s['medias']): manque.append(s['id'])
        for i, med in enumerate(s['medias']):
            med.pop('pool', None)
            if i < len(refs):
                r = refs[i]
                if isinstance(r, dict): med.update(r)
                else: med['media_ref'] = r
                rr = med['media_ref']; vus.setdefault(rr, []).append(s['id'])
        s['medias'] = [m_ for m_ in s['medias'] if 'media_ref' in m_]
    else:
        if ref:
            if isinstance(ref, dict): s.update(ref)
            else: s['media_ref'] = ref
            vus.setdefault(s['media_ref'], []).append(s['id'])
        else: manque.append(s['id'])
    s.pop('pool', None)
    s.setdefault('transition', 'coupe')
    # bandes cinéma seulement sur les plans pleins (pas de texte de schéma caché)
    if s.get('look') == 'bijou' and s['format'] not in ('rush', 'titre'): s.pop('look')
    # le punch joue déjà son impact
    if s.get('punch'): s['sons'] = [x for x in s.get('sons', []) if not (x['nom'] == 'impact' and abs(x['a'] - s['punch']['a']) < 0.3)]
    if 'sons' in s and not s['sons']: s.pop('sons')
    scenes.append(s)
m['scenes'] = scenes
doubles = {k: v for k, v in vus.items() if len(v) > 1}
print('manque', manque); print('doublons', doubles)
json.dump(m, open('/home/claude/chaine-youtube/episodes/capsules/montage.json', 'w'), ensure_ascii=False, indent=1)
print(len(scenes), 'scènes écrites')
