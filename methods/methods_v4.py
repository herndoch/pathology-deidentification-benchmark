"""Frozen exploratory numerical-context revision; annotation-free detector."""
import re
from methods import bools,intervals
from methods_v3 import detect as v3
# Local expression roles, not global exemptions for values found elsewhere.
COORDS=[re.compile(r'\bchr(?:[1-9]|1\d|2[0-2]|X|Y|M):\s*\d{4,10}(?:\s*[-_]\s*\d{4,10})?\b',re.I),re.compile(r'\b(?:(?:NC|NG|NM|NR)_\d+\.\d+:)?g\.\d+(?:_\d+)?(?:[ACGT]+>[ACGT]+|del(?:[ACGT]+)?|dup(?:[ACGT]+)?|ins[ACGT]+)?',re.I),re.compile(r'\b(?:genomic\s+(?:position|coordinate)|genome\s+position)\s*[:=]\s*(\d{4,10})\b',re.I),re.compile(r'\b(?:NC|NG|NM|NR)_\d+\.\d+\b')]
HARD_FIELD=re.compile(r'(?:^|[;|])\s*(?:patient(?:\s+(?:name|identification|identifier))?|name|mrn|medical\s+record(?:\s+(?:no\.?|number))?|record\s+(?:id|identifier)|dob|date\s+of\s+birth|birth\s+date|(?:related\s+|parent\s+)?accession(?:\s+(?:no\.?|number))?|laboratory\s+case\s+id|case\s+(?:no\.?|number)|ordering\s+provider|referring\s+clinician|requested\s+by)\s*[:=]\s*([^;|\n]+)',re.M|re.I)
def detect(text,base,linked_texts=(),mode='v4'):
    old=v3(text,base,linked_texts);m=bools(text,old)
    if mode=='v3':return old
    candidates=[]
    for pat in COORDS:
        for match in pat.finditer(text):candidates.append(match.span(1) if match.lastindex else match.span())
    cm=bools(text,candidates)
    if mode=='permissive_numeric':return intervals([a and not b for a,b in zip(m,cm)])
    # Numeric values are not globally propagated: the same digits can have different roles.
    hard=bools(text,[x.span(1) for x in HARD_FIELD.finditer(text)])
    return intervals([(a and not b) or h for a,b,h in zip(m,cm,hard)])
