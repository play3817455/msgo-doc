import io,sys,psycopg,json,os
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
DSN="postgresql://postgres:admin123@127.0.0.1:5432/msgo"
p="server/datafiles/lounge/module/module.csv"
seed=open(p,"rb").read()
def datablock(raw):
    out=[]
    for line in raw.decode("utf-8","replace").split("\r\n"):
        s=line.strip()
        if s and not s.startswith("#"): out.append(line)
    return out
sd=datablock(seed)
with psycopg.connect(DSN) as c:
    cur=c.cursor()
    cur.execute("select row_count, raw_csv from meta.cfg_manifest where file='MODULE'")
    n,raw=cur.fetchone()
    md=datablock(raw)
    print("seed rows",len(sd),"manifest rows",n,"block rows",len(md))
    for i,(a,b) in enumerate(zip(sd,md)):
        if a!=b: print("DIFF row",i); print("  seed:",a); print("  mani:",b)
    cur.execute('select count(*) from cfg."MODULE"')
    print("db rows",cur.fetchone()[0])
sch=json.load(open("serverv/static/cfg_schema.json",encoding="utf-8"))
def find(o,name):
    if isinstance(o,dict):
        if o.get("table")==name or o.get("id")==name or o.get("name")==name: return o
        for v in o.values():
            r=find(v,name)
            if r: return r
    elif isinstance(o,list):
        for v in o:
            r=find(v,name)
            if r: return r
    return None
t=find(sch,"MODULE")
if t:
    cols=t.get("columns") or t.get("column_defs") or []
    print("cfg_schema MODULE cols:",len(cols))
    for c in cols:
        if isinstance(c,dict): print("   ",c.get("csv_index"),c.get("name"),c.get("status",""))
else:
    print("cfg_schema: MODULE not found; top keys:",list(sch.keys())[:10] if isinstance(sch,dict) else type(sch))
