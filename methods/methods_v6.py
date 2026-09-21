"""Single bounded boundary repair; input text and baseline masks only."""
import re
from methods import bools,intervals
from methods_v4 import detect as prior_detect
from methods_v5 import LABEL,SECTION,_lines,_candidate_spans

# Only known development repairs: parentheses and repeated footer labels.
FIELD=re.compile(r'(?:^|[;|])[ \t]*\(?[ \t]*(?:footer[ \t]+(?:reference[ \t]+)?)?'+LABEL+r'[ \t]*(?:[:=]|\||\t)[ \t]*',re.I)

def hard_field_spans(text):
    lines=_lines(text);out=[]
    for i,(start,end,content) in enumerate(lines):
        for match in FIELD.finditer(content):
            a=start+match.end();b=end;blank_used=False;continuations=0
            for _,nend,ncontent in lines[i+1:]:
                if continuations>=5 or SECTION.fullmatch(ncontent.strip()) or FIELD.search(ncontent):break
                if not ncontent.strip():
                    # A single blank no longer terminates a populated identity field.
                    if blank_used:break
                    blank_used=True;continue
                b=nend;continuations+=1
            if a<b:out.append((a,b))
    return out

def detect(text,base,linked_texts=()):
    original=bools(text,prior_detect(text,base,linked_texts,'v3'))
    clinical=bools(text,_candidate_spans(text,expanded=True))
    hard=bools(text,hard_field_spans(text))
    return intervals([(a and not c) or h for a,c,h in zip(original,clinical,hard)])
