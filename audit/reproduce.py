"""Python 3, standard library only. No network, credentials, or model calls."""
from pathlib import Path
from collections import defaultdict
from itertools import product
from math import comb,isclose
import json, hashlib
import frozen_scorer
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def outcomes(gold,answers,arm):
 rows,issues=frozen_scorer.analyze(gold,answers,arm)
 assert not issues and len(rows)==len(gold) and all(r['status']=='completed' for r in rows)
 pairs=defaultdict(list)
 for r in rows:pairs[r['case_id']].append(r)
 for rs in pairs.values():assert len(rs)==2 and {r['role'] for r in rs}=={'clinical','identity_control'}
 joint={c:(rs[0]['family'],int(all(not r['any_variable_identity_exposure'] if r['role']=='identity_control' else r['clinical_expressions']>0 and r['clinical_expression_fully_retained']==r['clinical_expressions'] for r in rs))) for c,rs in pairs.items()}
 identity=[r for r in rows if r['role']=='identity_control'];clinical=[r for r in rows if r['role']=='clinical']
 summary={'identity_exposed':sum(r['any_variable_identity_exposure'] for r in identity),'clinical_retained':sum(r['clinical_expressions']>0 and r['clinical_expression_fully_retained']==r['clinical_expressions'] for r in clinical),'pair_success':sum(x[1] for x in joint.values()),'complete_pairs':len(joint)}
 return summary,joint,rows
def contrast(a,b):
 assert set(a)==set(b)
 ds=[a[c][1]-b[c][1] for c in a];w=ds.count(1);l=ds.count(-1);n=w+l
 exact=min(1,2*sum(comb(n,i) for i in range(min(w,l)+1))/2**n) if n else 1
 blocks=defaultdict(int)
 for c in a:assert a[c][0]==b[c][0];blocks[a[c][0]]+=a[c][1]-b[c][1]
 values=[v for v in blocks.values() if v];observed=abs(sum(values))
 perm=sum(abs(sum(v*s for v,s in zip(values,signs)))>=observed for signs in product([-1,1],repeat=len(values)))/2**len(values)
 return dict(wins=w,losses=l,effect_pp=sum(ds)/len(ds)*100,case_p=exact,family_p=perm)
def main():
 manifest=ROOT/'MANIFEST.json'
 if manifest.exists():
  for f in read(manifest)['files']:
   p=ROOT/f['path'];assert p.stat().st_size==f['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],f['path']
 labels=read(ROOT/'data/labels.json');gold=read(ROOT/'data/main/gold.json');data={};results={}
 assert len(gold)==len({d['opaque_id'] for d in gold})==400
 for arm in labels:
  summary,pairs,rows=outcomes(gold,read(ROOT/f'data/main/{arm}_outputs.json'),arm);data[arm]=pairs;results[arm]=summary
  saved={r['id']:r for r in read(ROOT/f'data/main/{arm}_scores.json')}
  for r in rows:assert all(r[k]==saved[r['id']][k] for k in r),(arm,r['id'])
  expected=next(r for r in read(ROOT/'data/main/summary.json') if r['arm']==arm)
  assert all(summary[k]==expected[k] for k in summary)
 tests=read(ROOT/'data/main/statistics.json');fresh=[]
 for t in tests:
  c=contrast(data[t['a']],data[t['b']]);assert all(isclose(c[k],t[k],rel_tol=1e-12,abs_tol=1e-50) for k in c);fresh.append(c)
 for key in ['case_p','family_p']:
  running=0
  for rank,i in enumerate(sorted(range(len(tests)),key=lambda i:fresh[i][key])):
   running=max(running,min(1,(len(tests)-rank)*fresh[i][key]));assert isclose(running,tests[i][key+'_holm'],rel_tol=1e-12,abs_tol=1e-50)
 for row in read(ROOT/'data/paired_outcome_counts.json')['rows']:
  a=data[row['arm']];b=data['local_v5'];counts=[0,0,0,0]
  for c in a:counts[{(1,1):0,(1,0):1,(0,1):2,(0,0):3}[(a[c][1],b[c][1])]]+=1
  assert counts==row['counts'] and sum(counts)==200
 example=read(ROOT/'data/braf_worked_example.json');original=example['document']['text']
 assert 'BRAF p.V600E is detected.' in original
 assert 'BRAF p.***** is detected.' in example['outputs']['philter']['text']
 assert 'BRAF p.V600E is detected.' in example['outputs']['philter_plus_context']['text']
 for answer in example['outputs'].values():
  assert len(answer['text'])==len(original)
  assert all(x==y or y=='*' for x,y in zip(original,answer['text']))
 lg=read(ROOT/'data/local/gold.json');local={};local_pairs={}
 assert len(lg)==len({d['opaque_id'] for d in lg})==len({d['text'] for d in lg})==400
 assert len({d['case_id'] for d in lg})==200
 for arm in ['philter','v5','v6']:
  s,p,rs=outcomes(lg,read(ROOT/f'data/local/{arm}_outputs.json'),arm);local[arm]=s;local_pairs[arm]=p
  saved={r['id']:r for r in read(ROOT/f'data/local/{arm}_scores.json')}
  for r in rs:assert all(r[k]==saved[r['id']][k] for k in r),(arm,r['id'])
 assert [(local[a]['identity_exposed'],local[a]['clinical_retained'],local[a]['pair_success']) for a in local]==[(0,0,0),(100,200,100),(50,200,150)]
 refinement=contrast(local_pairs['v6'],local_pairs['v5']);assert refinement['family_p']==.5 and refinement['effect_pp']==25
 saved_refinement=read(ROOT/'data/local/statistics.json')['contrasts'][0]
 assert all(isclose(v,saved_refinement[k],rel_tol=1e-12,abs_tol=1e-50) for k,v in refinement.items())
 print(json.dumps({'status':'PASS','main':results,'separate_local':local,'main_contrasts_and_Holm_adjustments_match':True,'local_refinement':refinement,'new_model_calls':0},indent=2))
if __name__=='__main__':main()
