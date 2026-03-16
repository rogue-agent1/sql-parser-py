#!/usr/bin/env python3
"""SQL parser — SELECT, INSERT, UPDATE, DELETE, CREATE TABLE."""
import sys,re

def tokenize(sql):
    return[t for t in re.findall(r"[A-Za-z_]\w*|[0-9]+|'[^']*'|[*,()=<>!;]|>=|<=|!=",sql) if t.strip()]

def parse(sql):
    tokens=tokenize(sql.strip().rstrip(';'))
    if not tokens:return None
    cmd=tokens[0].upper()
    if cmd=='SELECT':
        i=1;cols=[]
        while i<len(tokens) and tokens[i].upper()!='FROM':
            if tokens[i]!=',':cols.append(tokens[i])
            i+=1
        i+=1;table=tokens[i];i+=1
        where=None
        if i<len(tokens) and tokens[i].upper()=='WHERE':
            i+=1;where=(tokens[i],tokens[i+1],tokens[i+2]);i+=3
        return{'type':'SELECT','columns':cols,'table':table,'where':where}
    elif cmd=='INSERT':
        # INSERT INTO table (cols) VALUES (vals)
        i=2;table=tokens[i];i+=1
        assert tokens[i]=='(';i+=1;cols=[]
        while tokens[i]!=')':
            if tokens[i]!=',':cols.append(tokens[i])
            i+=1
        i+=1;assert tokens[i].upper()=='VALUES';i+=1
        assert tokens[i]=='(';i+=1;vals=[]
        while tokens[i]!=')':
            if tokens[i]!=',':vals.append(tokens[i].strip("'"))
            i+=1
        return{'type':'INSERT','table':table,'columns':cols,'values':vals}
    elif cmd=='CREATE':
        i=2;table=tokens[i];i+=1
        assert tokens[i]=='(';i+=1;columns=[]
        while tokens[i]!=')':
            if tokens[i]!=',':
                name=tokens[i];i+=1;dtype=tokens[i]
                columns.append((name,dtype))
            i+=1
        return{'type':'CREATE','table':table,'columns':columns}
    elif cmd=='DELETE':
        i=2;table=tokens[i];i+=1;where=None
        if i<len(tokens) and tokens[i].upper()=='WHERE':
            i+=1;where=(tokens[i],tokens[i+1],tokens[i+2])
        return{'type':'DELETE','table':table,'where':where}
    return None

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        r=parse("SELECT name, age FROM users WHERE age > 18")
        assert r['type']=='SELECT' and r['columns']==['name','age']
        assert r['table']=='users' and r['where']==('age','>','18')
        r2=parse("INSERT INTO users (name, age) VALUES ('Alice', 30)")
        assert r2['type']=='INSERT' and r2['table']=='users'
        assert r2['values']==['Alice','30']
        r3=parse("SELECT * FROM items")
        assert r3['columns']==['*'] and r3['where'] is None
        r4=parse("CREATE TABLE users (id INT, name TEXT)")
        assert r4['type']=='CREATE' and len(r4['columns'])==2
        r5=parse("DELETE FROM users WHERE id = 5")
        assert r5['type']=='DELETE' and r5['where']==('id','=','5')
        print("All tests passed!")
    else:
        sql="SELECT name, age FROM users WHERE age > 18"
        print(f"Parsed: {parse(sql)}")
if __name__=="__main__":main()
