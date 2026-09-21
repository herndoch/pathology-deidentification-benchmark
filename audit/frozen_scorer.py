"""Score aligned masks against synthetic Phase 4 gold; never infer safety from invalid output."""
from pathlib import Path
import argparse, collections, csv, json

ROOT=Path(__file__).resolve().parent

def positions(spans, alnum=False):
    return [i for s in spans for i,c in enumerate(s['text'],s['start']) if not alnum or c.isalnum()]

def analyze(gold, responses, run_label):
    expected={d['opaque_id']:d for d in gold}; by=collections.defaultdict(list); issues=[]
    for r in responses:
        if not isinstance(r,dict) or not isinstance(r.get('id'),str):
            issues.append('Response without a valid string id'); continue
        by[r['id']].append(r)
        if r['id'] not in expected: issues.append('Unexpected id: '+r['id'])
    rows=[]
    for oid,d in expected.items():
        row={k:d[k] for k in ['batch_id','case_id','family','split','role']}
        row.update(id=oid,source_id=d['id'],run_label=run_label,status='invalid',reason='',joint_annotated_pass=False)
        matches=by.get(oid,[])
        if len(matches)!=1:
            row['reason']='missing' if not matches else 'duplicate'; rows.append(row); continue
        r=matches[0]
        if set(r)!={'id','status','redacted_text'}:
            row['reason']='unexpected_or_missing_fields'; rows.append(row); continue
        if r['status']=='needs_review' and r['redacted_text'] is None:
            row.update(status='deferred',reason='explicit_review_request'); rows.append(row); continue
        text=d['text']; out=r['redacted_text']
        if r['status']!='completed' or not isinstance(out,str):
            row['reason']='invalid_status_or_output_type'; rows.append(row); continue
        if len(out)!=len(text):
            row['reason']='length_mismatch'; rows.append(row); continue
        if any((a in '\r\n' and b!=a) or (b!=a and b!='*') for a,b in zip(text,out)):
            row['reason']='not_a_character_aligned_mask'; rows.append(row); continue
        if '*' in text:
            row['reason']='source_asterisk_requires_adjudication'; rows.append(row); continue
        mask=[b=='*' for b in out]
        ident=positions(d['identifiers'],True); variable=positions(d['variable_numbers']); clinical=positions(d['clinical'])
        expressions=[s for s in d['clinical'] if s['type']=='clinical genomic expression']
        digits=[i for s in expressions for i,c in enumerate(s['text'],s['start']) if c.isdigit()]
        rem=sum(not mask[i] for i in ident); removed=sum(mask[i] for i in clinical)
        exposed=sum(not mask[i] for i in variable if text[i].isdigit())
        row.update(status='completed',reason='',identifier_alnum=len(ident),identifier_alnum_remaining=rem,
            variable_identity_digits=sum(text[i].isdigit() for i in variable),variable_identity_digits_exposed=exposed,
            any_variable_identity_exposure=bool(exposed),clinical_characters=len(clinical),clinical_characters_removed=removed,
            clinical_expressions=len(expressions),clinical_expression_fully_retained=sum(not any(mask[i] for i in range(s['start'],s['end'])) for s in expressions),
            clinical_expression_digits=len(digits),clinical_expression_digits_retained=sum(not mask[i] for i in digits),
            joint_annotated_pass=rem==0 and removed==0)
        rows.append(row)
    return rows,issues

def summarize(rows, keys):
    groups=collections.defaultdict(list)
    for r in rows: groups[tuple(r[k] for k in keys)].append(r)
    out=[]
    sums=['identifier_alnum','identifier_alnum_remaining','variable_identity_digits','variable_identity_digits_exposed','clinical_characters','clinical_characters_removed','clinical_expressions','clinical_expression_fully_retained','clinical_expression_digits','clinical_expression_digits_retained']
    for key,rs in sorted(groups.items()):
        valid=[r for r in rs if r['status']=='completed']
        item=dict(zip(keys,key)); item.update(expected_documents=len(rs),completed_alignable=len(valid),deferred=sum(r['status']=='deferred' for r in rs),invalid=sum(r['status']=='invalid' for r in rs),joint_annotated_pass=sum(r['joint_annotated_pass'] for r in rs))
        item.update({k:sum(r[k] for r in valid) for k in sums})
        item.update(documents_with_variable_exposure=sum(r['any_variable_identity_exposure'] for r in valid),documents_with_broad_residual=sum(r['identifier_alnum_remaining']>0 for r in valid))
        out.append(item)
    return out

def main():
    p=argparse.ArgumentParser(); p.add_argument('--responses',type=Path,required=True); p.add_argument('--batch',required=True); p.add_argument('--run-label',required=True); p.add_argument('--out',type=Path,required=True); a=p.parse_args()
    gold=json.loads((ROOT/'gold_documents.json').read_text())
    if a.batch!='all': gold=[d for d in gold if d['batch_id']==a.batch]
    if not gold: p.error('Unknown batch')
    files=sorted(a.responses.glob('*.json')) if a.responses.is_dir() else [a.responses]
    if not files: p.error('No response JSON files')
    responses=[]
    for f in files:
        data=json.loads(f.read_text(encoding='utf-8-sig'))
        if not isinstance(data,list): raise ValueError(str(f)+': expected a JSON array; preserve raw output and record delivery failure')
        responses.extend(data)
    rows,issues=analyze(gold,responses,a.run_label)
    result={'run_label':a.run_label,'batch':a.batch,'expected_records':len(gold),'submitted_records':len(responses),'delivery_issues':issues,'complete_alignable_delivery':not issues and all(r['status']=='completed' for r in rows),'interpretation':'Aligned endpoint metrics apply only to completed records. Invalid/deferred outputs are not privacy passes. No clinical generalization.','summary':summarize(rows,['split','role']),'by_family':summarize(rows,['split','family','role'])}
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (a.out/'per_document.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    columns=list(dict.fromkeys(k for r in rows for k in r))
    with (a.out/'per_document.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=columns); w.writeheader(); w.writerows(rows)
    print(json.dumps({'output':str(a.out),'expected':len(gold),'completed_alignable':sum(r['status']=='completed' for r in rows),'deferred':sum(r['status']=='deferred' for r in rows),'invalid':sum(r['status']=='invalid' for r in rows),'delivery_issues':issues},indent=2))

if __name__=='__main__': main()
