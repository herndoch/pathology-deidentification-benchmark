"""Second development iteration, after v1 failure inspection. No label input."""
import re
from methods import bools,intervals,structured,clinical_candidates,IDENT_LINE
TIMESTAMP=re.compile(r'\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})\s+(?:at\s+)?\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?\b',re.I)
# Role-conditioned symbols, including ones absent from the fixed gene vocabulary.
ROLE_PATTERNS=[re.compile(r'\b(?:variant|mutation|alteration)\s+(?:detected\s+)?in\s+([A-Z][A-Z0-9]{1,11})\b'),re.compile(r'\b([A-Z][A-Z0-9]{1,11})\s+(?:in situ hybridization|immunohistochemistry|p\.|c\.|amplification|rearrangement|fusion|mutation|variant)\b'),re.compile(r'\bNo\s+(?:reportable\s+)?([A-Z][A-Z0-9]{1,11})\s+(?:alteration|mutation|variant|copy.number|amplification)\b')]
def detect(text,base,linked_texts=()):
    ids=structured(text)+[m.span() for m in TIMESTAMP.finditer(text)]
    # Header-derived full accessions are available locally across this linked bundle.
    values=set()
    for source in [text,*linked_texts]:
        values.update(m.group(1).strip() for m in re.finditer(r'^(?:Accession|Related accession|Parent accession):\s*(.+)$',source,re.M|re.I))
    for v in values:
        ids.extend(m.span() for m in re.finditer(r'(?<!\w)'+re.escape(v)+r'(?!\w)',text))
    c=clinical_candidates(text);pos=0
    for line in text.splitlines(keepends=True):
        if not IDENT_LINE.search(line.strip()):
            c.extend((pos+m.start(1),pos+m.end(1)) for pat in ROLE_PATTERNS for m in pat.finditer(line))
        pos+=len(line)
    b=bools(text,base);im=bools(text,ids);cm=bools(text,c)
    return intervals([(x and not z) or y for x,y,z in zip(b,im,cm)])
