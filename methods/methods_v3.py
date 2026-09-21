"""Frozen phase-two addition: independent identifier shape + flexible field roles.

No annotation or case-manifest access. This deliberately preserves v2's clinical
allowances to isolate identifier handling. Frozen before new-case evaluation.
"""
import re
from methods import bools,intervals
from methods_v2 import detect as v2
ACCESSION=re.compile(r'\b(?:[A-Z]{1,4}\s*[-.]?\s*\d{2,4}|\d{2,4}\s*[-.]?\s*[A-Z]{1,4})\s*[-.]\s*\d{4,10}\b')
FIELDS=re.compile(r'^[ \t]*(?:patient(?:\s+(?:name|identification))?|name|mrn|medical\s+record(?:\s+(?:no\.?|number))?|dob|date\s+of\s+birth|(?:(?:related|parent)\s+)?accession(?:\s+(?:no\.?|number))?|case\s+(?:no\.?|number)|ordering\s+provider|requested\s+by)\s*[:=]\s*([^\n|;]+)',re.M|re.I)
SIGNATURE=re.compile(r'\b(?:electronically\s+signed\s+by|signed\s+out\s+by|prosected\s+by|grossed\s+by)\s+([^,\n]+?)(?=,|\s+on\s+|$)',re.M|re.I)
def detect(text,base,linked_texts=(),mode='v3'):
    spans=v2(text,base,linked_texts)
    if mode=='v2':return spans
    if mode in ('v3','v3_shape_only'):spans+= [m.span() for m in ACCESSION.finditer(text)]
    if mode in ('v3','v3_label_only'):
        values=set()
        for source in [text,*linked_texts]:
            for p in (FIELDS,SIGNATURE):values.update(m.group(1).strip() for m in p.finditer(source))
        for val in values:
            # Tolerate wrapping between words, with coordinates on the original input.
            pat=r'(?<!\w)'+r'\s+'.join(re.escape(w) for w in val.split())+r'(?!\w)'
            if val:spans += [m.span() for m in re.finditer(pat,text)]
    return intervals(bools(text,spans))
