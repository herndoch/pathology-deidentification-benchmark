"""Phase 4 text candidate.  Detector functions receive text and base masks only.

No annotation file, synthetic truth label, corpus manifest, or scoring result is
imported here.  The parser deliberately uses source offsets without whitespace
normalisation so a continuation cannot shift a downstream mask.
"""
import re
from methods import bools, intervals
from methods_v4 import COORDS, detect as v4_detect

LABEL = r'(?:patient(?:\s+(?:name|identification|identifier))?|name|mrn|medical\s+record(?:\s+(?:no\.?|number))?|record\s+(?:id|identifier)|dob|date\s+of\s+birth|birth\s+date|(?:related\s+|parent\s+)?accession(?:\s+(?:no\.?|number))?|laboratory\s+case\s+id|case\s+(?:no\.?|number)|ordering\s+provider|referring\s+clinician|requested\s+by)'
# A label may appear at the beginning of a physical line or as the first cell
# after a pipe/semicolon.  Tab or pipe separators support plain-text tables.
FIELD_START = re.compile(r'(?:^|[;|])\s*'+LABEL+r'\s*(?:[:=]|\||\t)\s*', re.I)
NEXT_FIELD = re.compile(r'(?:^|[;|])\s*'+LABEL+r'\s*(?:[:=]|\||\t)', re.I)
SECTION = re.compile(r'^(?:final\s+diagnosis|comment(?:s)?|clinical\s+history|microscopic\s+description|molecular\s+(?:results|interpretation)|results|interpretation|addendum(?:\s+(?:result|comment))?|gross\s+description|synoptic(?:\s+(?:report|summary))?|test\s+results)\s*:?[ \t]*$', re.I)

# These additions repair the Phase 3 table/prose clinical-context gap.  They are
# local expressions, not number allowlists, and all remain subordinate to a hard
# identity field detected by hard_field_spans().
EXPANDED_COORDS = [
    re.compile(r'\bchromosome\s+(?:chr)?(?:[1-9]|1\d|2[0-2]|X|Y|M)\s*[,;]\s*(?:genomic\s+)?position\s*[:=]?\s*\d{4,10}\b', re.I),
    re.compile(r'\b(?:genomic\s+)?position\s*[:=]\s*\d{4,10}\s*\(\s*(?:chr(?:omosome)?\s*)?(?:[1-9]|1\d|2[0-2]|X|Y|M)\s*\)', re.I),
    re.compile(r'(?im)^\s*(?:chromosome|chr)\s*[|\t]\s*(?:genomic\s+)?position\s*\r?\n\s*(?:chr)?(?:[1-9]|1\d|2[0-2]|X|Y|M)\s*[|\t]\s*\d{4,10}\b'),
    re.compile(r'(?im)^\s*(?:genomic\s+)?position\s*[|\t]\s*(?:chromosome|chr)\s*\r?\n\s*\d{4,10}\s*[|\t]\s*(?:chr)?(?:[1-9]|1\d|2[0-2]|X|Y|M)\b'),
]

def _lines(text):
    """Return physical line (start, end_without_newline, content) triples."""
    out=[]; pos=0
    for keep in text.splitlines(keepends=True):
        content=keep[:-2] if keep.endswith('\r\n') else keep[:-1] if keep.endswith('\n') or keep.endswith('\r') else keep
        out.append((pos, pos+len(content), content)); pos+=len(keep)
    if not out or pos < len(text): out.append((pos,len(text),text[pos:]))
    return out

def _section_or_new_field(content):
    stripped=content.strip()
    return bool(SECTION.fullmatch(stripped) or NEXT_FIELD.search(content))

def hard_field_spans(text):
    """Return value spans for identity fields, including conservative continuations.

    A continuation may be unindented (the Phase 3 counterexample), tabular, or
    follow one empty line when the labelled value was empty.  It ends at a new
    hard label, a known report section, or an ordinary blank boundary.  This is
    intentionally safety-biased: an ambiguous immediate continuation remains
    inside the identity field rather than restoring a number based on its shape.
    """
    lines=_lines(text); out=[]
    for i,(start,end,content) in enumerate(lines):
        for match in FIELD_START.finditer(content):
            value_start=start+match.end(); value_end=end
            j=i+1; blank_used=False; continuation_count=0
            initial_empty=not content[match.end():].strip()
            while j < len(lines) and continuation_count < 5:
                nstart,nend,ncontent=lines[j]
                if _section_or_new_field(ncontent): break
                if not ncontent.strip():
                    if initial_empty and not blank_used:
                        blank_used=True; j+=1; continue
                    break
                # The next physical non-section line is a continuation.  This
                # covers wrapping without indentation and rows of a plain-text
                # table while retaining original character coordinates.
                value_end=nend; continuation_count+=1; j+=1
            if value_start < value_end: out.append((value_start,value_end))
    return out

def _candidate_spans(text, expanded):
    spans=[]
    for pat in COORDS:
        for match in pat.finditer(text): spans.append(match.span(1) if match.lastindex else match.span())
    if expanded:
        for pat in EXPANDED_COORDS:
            spans.extend(match.span() for match in pat.finditer(text))
    return spans

def detect(text, base, linked_texts=(), mode='v5'):
    """Return masking spans for v5 or the boundary-only ablation."""
    if mode not in {'v5','v5_boundary_only'}: raise ValueError(mode)
    old=v4_detect(text,base,linked_texts,'v3')
    old_mask=bools(text,old)
    candidate_mask=bools(text,_candidate_spans(text,expanded=mode=='v5'))
    hard_mask=bools(text,hard_field_spans(text))
    return intervals([(masked and not candidate) or hard for masked,candidate,hard in zip(old_mask,candidate_mask,hard_mask)])
