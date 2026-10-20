import io,sys,psycopg
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
DSN="postgresql://postgres:admin123@127.0.0.1:5432/msgo"
with psycopg.connect(DSN,autocommit=True) as c:
    cur=c.cursor()
    cur.execute("delete from meta.cfg_manifest where file='GMTEST_TMP'")
    print("deleted manifest:",cur.rowcount)
    cur.execute("delete from meta.cfg_table_def where table_name='GMTEST_TMP'")
    print("deleted table_def:",cur.rowcount)
    cur.execute("select count(*) from meta.cfg_manifest")
    print("manifest now:",cur.fetchone()[0])
