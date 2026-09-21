"""Run cached public Philter only on hash-bound synthetic pilot requests."""
import contextlib, hashlib, json, os, re, sys, time, warnings
from pathlib import Path

PUBLIC=Path(__file__).resolve().parents[1]/'vendor/philter'
NLTK=PUBLIC.parent/'nltk_data'
SUPPORTED={'regex':'map_regex','set':'map_set','regex_context':'map_regex_context','pos_matcher':'map_pos'}
def sha256_bytes(x): return hashlib.sha256(x).hexdigest()
def sha256_file(p): return sha256_bytes(Path(p).read_bytes())
def require(ok,msg):
    if not ok: raise RuntimeError('PHILTER_SYNTHETIC_CONTRACT: '+msg)
def ascii_maskable(c): return ('A'<=c<='Z') or ('a'<=c<='z') or ('0'<=c<='9')

def main():
    import nltk
    nltk.data.path[:]=[str(NLTK)]; sys.path.insert(0,str(PUBLIC)); os.chdir(PUBLIC)
    from philter import Philter
    from coordinate_map import CoordinateMap
    class CompatPhilter(Philter):
        def precompile(self,filepath):
            exp=Path(filepath).read_text(encoding='utf-8').strip(); flags=''.join(sorted(set(''.join(re.findall(r'\(\?([aiLmsux]+)\)',exp)))))
            return re.compile(('(?'+flags+')' if flags else '')+re.sub(r'\(\?[aiLmsux]+\)','',exp))
    request_path=REQUEST; output=OUTPUT; requests=json.loads(request_path.read_text(encoding='utf-8'))
    require(isinstance(requests,list) and requests,'request list is empty'); ids=[r.get('id') for r in requests]
    require(all(isinstance(x,str) and x for x in ids) and len(ids)==len(set(ids)),'request IDs missing or non-unique')
    for r in requests:
        require(r.get('synthetic') is True and isinstance(r.get('text'),str),'request must be marked synthetic and contain text')
        require(r.get('text_sha256')==sha256_bytes(r['text'].encode('utf-8')),'text hash mismatch: '+r['id'])
        require(isinstance(r.get('input_contract_sha256'),str) and isinstance(r.get('run_manifest_sha256'),str),'missing pilot provenance: '+r['id'])
    contracts={r['input_contract_sha256'] for r in requests}; manifests={r['run_manifest_sha256'] for r in requests}; require(len(contracts)==1 and len(manifests)==1,'request batch mixes input provenance')
    outputs=[]
    for r in requests:
        text=r['text']; started=time.perf_counter()
        with open(os.devnull,'w') as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink), warnings.catch_warnings():
            warnings.simplefilter('ignore'); engine=CompatPhilter({'filters':str(PUBLIC/'configs/philter_delta.json'),'verbose':False,'run_eval':False,'cachepos':None})
            unsupported=sorted({p.get('type') for p in engine.patterns}-set(SUPPORTED)); require(not unsupported,'unsupported upstream pattern type(s): '+', '.join(str(x) for x in unsupported))
            key=str(PUBLIC/'LICENSE'); engine.data_all_files[key]={'text':text,'phi':[],'non-phi':[]}; engine.include_map.add_file(key); engine.exclude_map.add_file(key)
            for typ in engine.phi_type_list: engine.phi_type_dict[typ][0].add_file(key)
            for i,p in enumerate(engine.patterns):
                p['coordinate_map']=CoordinateMap(); getattr(engine,SUPPORTED[p['type']])(filename=key,text=text,pattern_index=i); engine.get_exclude_include_maps(key,p,text)
            keep=[False]*len(text)
            for start,stop in engine.include_map.filecoords(key): keep[start:stop]=[True]*(stop-start)
            # Upstream asterisk mode changes only ASCII letters/digits outside final include_map.
            # Punctuation and an existing literal '*' are preserved byte-for-byte.
            mask=[not keep[i] and ascii_maskable(c) for i,c in enumerate(text)]; spans=[]; i=0
            actual=engine.transform_text_asterisk(text,key)
            reconstructed=''.join('*' if mask[j] else c for j,c in enumerate(text))
            require(actual==reconstructed,'adapter differs from upstream transform: '+r['id'])
            while i<len(text):
                if not mask[i]: i+=1; continue
                start=i
                while i<len(text) and mask[i]: i+=1
                spans.append([start,i])
        outputs.append({'id':r['id'],'text_sha256':r['text_sha256'],'spans':spans,'latency_seconds':time.perf_counter()-started,'n_filters':len(engine.patterns)})
        print(json.dumps({'completed':len(outputs),'total':len(requests),'id':r['id']}),flush=True)
    output.write_text(json.dumps(outputs,indent=2),encoding='utf-8')
    provenance={'method':'UCSF Philter Delta compatibility adapter; final include-map complement to ASCII asterisk-change spans','python':sys.version,'request_sha256':sha256_file(request_path),'output_sha256':sha256_file(output),'input_contract_sha256':next(iter(contracts)),'run_manifest_sha256':next(iter(manifests)),'config_sha256':sha256_file(PUBLIC/'configs/philter_delta.json'),'philter_sha256':sha256_file(PUBLIC/'philter.py'),'regex_compatibility':'global inline flags normalized to front for Python3.12; fixture equivalence required for config changes','supported_pattern_types':sorted(SUPPORTED),'asterisk_semantics':'included intervals preserved; outside them spans mark only upstream ASCII asterisk changes [A-Za-z0-9], preserving punctuation and literal asterisk','upstream_url':'https://github.com/BCHSI/philter-ucsf','synthetic_only':True}
    output.with_suffix('.provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
if __name__=='__main__':
    REQUEST=Path(sys.argv[1]).resolve(); OUTPUT=Path(sys.argv[2]).resolve()
    if OUTPUT.exists():raise SystemExit('Refusing to overwrite predictions')
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    main()
