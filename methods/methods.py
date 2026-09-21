"""Development detectors. No annotation or manifest access is allowed here."""
import re
GENES='ALK ARID1A ATRX BRAF BRCA1 BRCA2 CDH1 EGFR ERBB2 ETV6 IDH1 IDH2 KIT KRAS MET MLH1 MSH2 MSH6 MTOR NF1 NTRK1 NTRK2 NTRK3 PALB2 PDGFRA PMS2 PTEN RB1 RET ROS1 SDHB SMAD4 STK11 TERT TP53 VHL'.split()
GP=re.compile(r'\b(?:'+ '|'.join(GENES)+r')\b')
DATE=re.compile(r'\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})\b')
HEAD=re.compile(r'^(?:Name|Patient|MRN|DOB|Accession|Ordering Provider|Ordering provider):\s*(.+)$',re.M)
AUTHOR=re.compile(r'(?:Report finalized by|Finalized by|Grossing performed by|Gross examination performed by)\s+(.+?)(?=,| on |\.|$)',re.M)
SECTIONS={'FINAL DIAGNOSIS','COMMENT','COMMENTS','CLINICAL HISTORY','MICROSCOPIC DESCRIPTION','MOLECULAR RESULTS','RESULTS','INTERPRETATION','MOLECULAR INTERPRETATION','ADDENDUM RESULT','ADDENDUM COMMENT','GROSS DESCRIPTION','SYNOPTIC REPORT','SYNOPTIC SUMMARY','INTRAOPERATIVE CONSULTATION','TEST RESULTS'}
IDENT_LINE=re.compile(r'^(?:Name|Patient|MRN|DOB|Accession|Ordering|Collected|Received|Reported|Report finalized|Finalized|Grossing performed|Gross examination performed)|\|.*\|',re.I)
VAR=re.compile(r'\b[pc]\.[A-Za-z0-9_*+>:=?()\-]+|\b[A-Z][A-Z0-9]+::[A-Z][A-Z0-9]+\b|\b\d+(?:\.\d+)?\s*%|\b\d+(?:\.\d+)?\s*(?:mutations/Mb|mut/Mb|copies)\b')
def bools(text,spans):
    m=[False]*len(text)
    for a,b in spans:m[a:b]=[True]*(b-a)
    return m
def intervals(mask):
    out=[];start=None
    for i,x in enumerate(mask+[False]):
        if x and start is None:start=i
        elif not x and start is not None:out.append((start,i));start=None
    return out
def structured(text,propagate=True):
    spans=[];values=[]
    for pat in (HEAD,AUTHOR):
        for m in pat.finditer(text):
            a,b=m.span(1); v=text[a:b].strip(); b=a+len(v)
            if v:spans.append((a,b));values.append(v)
    if propagate:
        for v in set(values):
            for m in re.finditer(r'(?<!\w)'+re.escape(v)+r'(?!\w)',text):spans.append(m.span())
    spans.extend(m.span() for m in DATE.finditer(text))
    spans.extend(m.span() for m in re.finditer(r'\b\d{8}\b',text))
    return spans
def clinical_candidates(text):
    out=[];section='';pos=0
    for line in text.splitlines(keepends=True):
        stripped=line.strip()
        if stripped in SECTIONS:section=stripped
        if not IDENT_LINE.search(stripped) and (section in SECTIONS or re.search(r'\b(?:VAF|variant|fusion|mutation|copy.number|detected|amplification)\b',line,re.I)):
            out.extend((pos+m.start(),pos+m.end()) for p in (GP,VAR) for m in p.finditer(line))
        pos+=len(line)
    return out
def run(text,base,mode):
    b=bools(text,base); ids=bools(text,structured(text)); c=bools(text,clinical_candidates(text))
    if mode=='philter':return base
    if mode=='structured_rules':return intervals(ids)
    if mode=='philter_plus_identifiers':return intervals([x or y for x,y in zip(b,ids)])
    if mode=='philter_plus_context':return intervals([x and not y for x,y in zip(b,c)])
    if mode=='pathology_hybrid':return intervals([(x and not z) or y for x,y,z in zip(b,ids,c)])
    if mode=='naive_gene_allowlist':
        c=bools(text,[m.span() for m in GP.finditer(text)])
        return intervals([(x or y) and not z for x,y,z in zip(b,ids,c)])
    raise ValueError(mode)
def masked(text,spans):
    m=bools(text,spans)
    return ''.join('*' if m[i] and not ch.isspace() else ch for i,ch in enumerate(text))
