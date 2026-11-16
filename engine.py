import json,os,random
import urllib.request,urllib.error
ur=urllib.request
INF=10**7
MATE=10**6
VAL=[0,100,320,330,500,990,0,0]
PB=[0,5,10,20,40,70]
PHASE=[0,0,1,1,2,4,0,0]
_S=r"AAAAIOQO?DHI>DCE=BAD>DAA=DB>AAAA*96B:>LFALONBDII@CDE>CDD=<BA7>:=>B7<;DEC@HIHABFIACCFBDEDBEDB=>?>HGEKGFLMBHGF>@EF<@@B;?@@8@A@>=BDCEGGD@F@EDGD??A@@?@@ACAA>@DB==>A=C@;A>?@?EB>=>>=9>;:>?=:BC?8AF@>AAAA`^ZYPPMLEECBBB@@AB@ABBBCAAAA49><;?=@<>AB>BDE>ADE>?AC:>?A:9>>>>@@@AA@BABAABCC@ACD?@BC>?@B>@>@CCDDBCCBBBBBBBBBAABA@A@AA@AA?B@ABDEF@FFJ@CEIEHGJBGFH@@DC=<=?;===:?A?AEFDCFGDAEFF?BEF?BDE>@BD9<>>"
MGS,EGS=_S[:192],_S[192:]
MV=[82,337,365,477,1025,0]
EV=[94,281,297,512,936,0]
_D=lambda S,t,i:((ord(S[t*32+(i>>3)*4+min(i&7,7-i&7)])-36)*6-176)
MGT=[[MV[t]+_D(MGS,t,i)for i in range(64)]for t in range(6)]
EGT=[[EV[t]+_D(EGS,t,i)for i in range(64)]for t in range(6)]
KN=(-33,-31,-18,-14,14,18,31,33)
K8=(-17,-16,-15,-1,1,15,16,17)
BD=(-17,-15,15,17)
RD=(-16,-1,1,16)
CMASK=[15]*120
for _i,_v in((0,7),(7,11),(4,3),(112,13),(119,14),(116,12)):CMASK[_i]=_v
FILES="abcdefgh"
_rng=random.Random(20240817)
ZP=[[_rng.getrandbits(64)if p else 0 for _ in range(120)]for p in range(15)]
ZC=[_rng.getrandbits(64)for _ in range(16)]
ZS=_rng.getrandbits(64)
B=[0]*120
KS=[0,0]
SIDE=0
CAST=0
EPSQ=-1
HM=0
HASH=0
NPM=[0,0]
TT={}
KILL=[[0,0]for _ in range(64)]
NODES=STOP=0
CAP=80000
def attacked(s,by):
 pp=1+(by<<3)
 for d in((15,17),(-15,-17))[by]:
  t=s+d
  if not t&0x88 and B[t]==pp:return True
 for ds,pn in((KN,2),(K8,6)):
  n=pn+(by<<3)
  for d in ds:
   t=s+d
   if not t&0x88 and B[t]==n:return True
 for ds,ty in((BD,(3,5)),(RD,(4,5))):
  for d in ds:
   t=s+d
   while not t&0x88:
    p=B[t]
    if p:
     if(p>>3)==by and(p&7)in ty:return True
     break
    t+=d
 return False
def gen_moves(caps_only=False):
 out=[]
 ap=out.append
 for s in range(120):
  if s&0x88:continue
  p=B[s]
  if not p or(p>>3)!=SIDE:continue
  pt=p&7
  if pt==1:
   fw,cap,home,last=16*(2*SIDE-1),((15,17)if SIDE else(-17,-15)),6-5*SIDE,7*SIDE
   for d in cap:
    t=s+d
    if t&0x88:continue
    q=B[t]
    if(q and(q>>3)!=SIDE)or t==EPSQ:
     if(t>>4)==last:
      for pr in(5,4,3,2):ap(s|t<<7|pr<<14)
     else:
      ap(s|t<<7)
   t=s+fw
   if not B[t]:
    if(t>>4)==last:
     for pr in(5,4,3,2):ap(s|t<<7|pr<<14)
    elif not caps_only:
     ap(s|t<<7)
     if(s>>4)==home and not B[s+2*fw]:
      ap(s|(s+2*fw)<<7)
  elif pt in(2,6):
   for d in(KN if pt==2 else K8):
    t=s+d
    if not t&0x88:
     q=B[t]
     if q:
      if(q>>3)!=SIDE:ap(s|t<<7)
     elif not caps_only:
      ap(s|t<<7)
  else:
   dirs=BD if pt==3 else RD if pt==4 else K8
   for d in dirs:
    t=s+d
    while not t&0x88:
     q=B[t]
     if not q:
      if not caps_only:ap(s|t<<7)
     else:
      if(q>>3)!=SIDE:ap(s|t<<7)
      break
     t+=d
 if not caps_only:
  for ksq,bit,e1,e2,extra,enemy in((116,1,117,118,0,1),(116,2,115,114,113,1),(4,4,5,6,0,0),(4,8,3,2,1,0)):
   if(ksq==116)==(SIDE==0)and CAST&bit and B[ksq]==6+(SIDE<<3)and not B[e1]and not B[e2]and not(extra and B[extra])and not attacked(ksq,enemy)and not attacked(e1,enemy)and not attacked(e2,enemy):
    ap(ksq|e2<<7)
 return out
def make(m):
 global SIDE,CAST,EPSQ,HM,HASH
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7
 p=B[f];pt=p&7
 cap=B[t]
 ep_cap=0
 undo=(cap,CAST,EPSQ,HM,HASH,0)
 HASH^=ZC[CAST]^ZS
 if pt==1 and t==EPSQ and cap==0 and(f&7)!=(t&7):
  cs=t+16 if SIDE==0 else t-16
  ep_cap=B[cs]
  B[cs]=0
  HASH^=ZP[ep_cap][cs]
  undo=(cap,CAST,EPSQ,HM,undo[4],ep_cap)
 B[f]=0
 B[t]=(SIDE<<3)+pr if pr else p
 HASH^=ZP[p][f]^ZP[B[t]][t]
 if cap:
  HASH^=ZP[cap][t]
  if(cap&7)>1:NPM[SIDE^1]-=1
 if pr:NPM[SIDE]+=1
 if pt==6:
  KS[SIDE]=t
  if abs(t-f)==2:
   d=1 if t>f else-1
   rf,rt=f+(3 if d>0 else-4),f+d
   B[rt]=B[rf];B[rf]=0
   HASH^=ZP[B[rt]][rf]^ZP[B[rt]][rt]
 CAST&=CMASK[f]&CMASK[t]
 HASH^=ZC[CAST]
 EPSQ=(f+t)//2 if pt==1 and abs(t-f)==32 else-1
 HM=0 if pt==1 or cap or ep_cap else HM+1
 SIDE^=1
 return undo
def unmake(m,undo):
 global SIDE,CAST,EPSQ,HM,HASH
 cap,CAST,EPSQ,HM,HASH,ep_cap=undo
 SIDE^=1
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7
 p=B[t]
 if pr:
  p=(SIDE<<3)+1
  NPM[SIDE]-=1
 B[f]=p
 B[t]=cap
 if cap and(cap&7)>1:NPM[SIDE^1]+=1
 if(p&7)==6:
  KS[SIDE]=f
  if abs(t-f)==2:
   d=1 if t>f else-1
   B[f+(3 if d>0 else-4)]=B[f+d];B[f+d]=0
 if ep_cap:
  cs=t+16 if SIDE==0 else t-16
  B[cs]=ep_cap
  B[t]=0
def evaluate():
 mg=0;eg=0;ph=0
 pawns=[[],[]]
 for s in range(120):
  if s&0x88:continue
  p=B[s]
  if not p:continue
  pt=p&7;c=p>>3
  ph+=PHASE[pt]
  r=s>>4;fi=s&7
  if pt==1:pawns[c].append(r*8+fi)
  i=r*8+fi if c==0 else(7-r)*8+fi
  if c:
   mg-=MGT[pt-1][i];eg-=EGT[pt-1][i]
  else:
   mg+=MGT[pt-1][i];eg+=EGT[pt-1][i]
 ph=min(ph,24)
 sc=(mg*ph+eg*(24-ph))//24
 for c in(0,1):
  sg=1-2*c
  foe=pawns[c^1]
  for i in pawns[c]:
   r=i>>3;f=i&7
   if all(abs((j&7)-f)>1 or((j>>3)-r)*sg>=0 for j in foe):
    sc+=sg*(PB[6-r]if c==0 else PB[r-1])
 return sc if SIDE==0 else-sc
def order_moves(moves,tt_move,ply):
 k1,k2=KILL[ply]if ply<64 else(0,0)
 def key(m):
  if m==tt_move:return 1<<30
  cap=B[(m>>7)&127]
  if cap:return(1<<24)+VAL[cap&7]*16-VAL[B[m&127]&7]
  pr=(m>>14)&7
  if pr:return(1<<23)+VAL[pr]
  if m==k1:return 1<<22
  if m==k2:return(1<<22)-1
  return 0
 moves.sort(key=key,reverse=True)
def qsearch(alpha,beta,ply):
 global NODES,STOP
 NODES+=1
 if NODES>=CAP:STOP=True
 if STOP:return alpha
 if HM>=100:return 0
 in_chk=attacked(KS[SIDE],SIDE^1)
 if in_chk:
  moves=gen_moves()
 else:
  stand=evaluate()
  if stand>=beta:return beta
  if stand>alpha:alpha=stand
  moves=gen_moves(True)
 order_moves(moves,0,ply)
 legal=False
 for m in moves:
  undo=make(m)
  if attacked(KS[SIDE^1],SIDE):
   unmake(m,undo);continue
  legal=True
  sc=-qsearch(-beta,-alpha,ply+1)
  unmake(m,undo)
  if STOP:return alpha
  if sc>=beta:return beta
  if sc>alpha:alpha=sc
 if in_chk and not legal:return-MATE+ply
 return alpha
def search(depth,alpha,beta,ply):
 global NODES,STOP,SIDE,EPSQ,HASH
 if depth<=0:return qsearch(alpha,beta,ply)
 NODES+=1
 if NODES>=CAP:STOP=True
 if STOP:return alpha
 if HM>=100:return 0
 alpha0=alpha
 in_chk=attacked(KS[SIDE],SIDE^1)
 if in_chk:depth+=1
 tt=TT.get(HASH)
 tt_move=0
 if tt:
  tt_move=tt[3]
  if tt[0]>=depth:
   if tt[1]==0:return tt[2]
   if tt[1]==1:alpha=max(alpha,tt[2])
   else:beta=min(beta,tt[2])
   if alpha>=beta:return tt[2]
 if depth>=3 and not in_chk and beta-alpha==1 and abs(beta)<MATE-1000 and NPM[SIDE]>0:
  save_ep,save_hash=EPSQ,HASH
  EPSQ=-1
  HASH^=ZS
  SIDE^=1
  sc=-search(depth-3,-beta,-beta+1,ply+1)
  SIDE^=1
  EPSQ,HASH=save_ep,save_hash
  if STOP:return alpha
  if sc>=beta:return beta
 moves=gen_moves()
 order_moves(moves,tt_move,ply)
 best=-INF;best_m=0
 n_legal=0
 for i,m in enumerate(moves):
  undo=make(m)
  if attacked(KS[SIDE^1],SIDE):
   unmake(m,undo);continue
  n_legal+=1
  cap=undo[0]or undo[5]
  quiet=not cap and not((m>>14)&7)
  if n_legal==1:
   sc=-search(depth-1,-beta,-alpha,ply+1)
  else:
   red=1 if depth>=3 and i>=3 and quiet and not in_chk else 0
   sc=-search(depth-1-red,-alpha-1,-alpha,ply+1)
   if red and sc>alpha:
    sc=-search(depth-1,-alpha-1,-alpha,ply+1)
   if alpha<sc<beta:
    sc=-search(depth-1,-beta,-alpha,ply+1)
  unmake(m,undo)
  if STOP:return alpha
  if sc>best:
   best=sc;best_m=m
  if sc>alpha:alpha=sc
  if alpha>=beta:
   if quiet:
    if ply<64 and KILL[ply][0]!=m:
     KILL[ply][1]=KILL[ply][0];KILL[ply][0]=m
   break
 if n_legal==0:
  return-MATE+ply if in_chk else 0
 flag=1 if best>=beta else 0 if best>alpha0 else 2
 TT[HASH]=(depth,flag,best,best_m)
 return best
def set_fen(fen):
 global SIDE,CAST,EPSQ,HM,HASH
 parts=fen.split()
 rows=parts[0].split("/")
 for i in range(120):B[i]=0
 NPM[0]=NPM[1]=0
 for r,row in enumerate(rows):
  f=0
  for ch in row:
   if ch.isdigit():
    f+=int(ch)
   else:
    p="pnbrqk".index(ch.lower())+1+(0 if ch.isupper()else 8)
    B[r*16+f]=p
    if p==6:KS[0]=r*16+f
    if p==14:KS[1]=r*16+f
    if(p&7)in(2,3,4,5):NPM[p>>3]+=1
    f+=1
 SIDE=0 if len(parts)<2 or parts[1]=="w"else 1
 CAST=0
 if len(parts)>2:
  CAST=sum((1<<i)for i,ch in enumerate("KQkq")if ch in parts[2])
 EPSQ=-1
 if len(parts)>3 and parts[3]!="-":
  EPSQ=(8-int(parts[3][1]))*16+FILES.index(parts[3][0])
 HM=int(parts[4])if len(parts)>4 else 0
 HASH=0
 for s in range(120):
  if not s&0x88 and B[s]:HASH^=ZP[B[s]][s]
 HASH^=ZC[CAST]
 if SIDE:HASH^=ZS
def to_uci(m):
 u="".join(FILES[x&7]+str(8-(x>>4))for x in(m&127,(m>>7)&127))
 pr=(m>>14)&7
 if pr:u+="nbrq"[pr-2]
 return u
def greedy(fen,legal):
 set_fen(fen)
 gm={to_uci(m):m for m in gen_moves()}
 def rank(u):
  m=gm[u]
  return(-VAL[B[(m>>7)&127]&7],-VAL[(m>>14)&7],u)
 return min(legal,key=rank)
def pick_move(fen,legal):
 global NODES,STOP
 set_fen(fen)
 if len(TT)>250000:TT.clear()
 NODES=0;STOP=False
 moves=gen_moves()
 legal_moves=[]
 for m in moves:
  undo=make(m)
  if not attacked(KS[SIDE^1],SIDE):legal_moves.append(m)
  unmake(m,undo)
 if not legal_moves:return legal[0]
 fb=greedy(fen,legal)
 best=next((m for m in legal_moves if to_uci(m)==fb),legal_moves[0])
 depth=1
 while not STOP:
  cur=best;cur_sc=-INF;alpha=-INF
  order_moves(legal_moves,best,0)
  for m in legal_moves:
   undo=make(m)
   sc=-search(depth-1,-INF,-alpha,1)
   unmake(m,undo)
   if STOP:break
   if sc>cur_sc:
    cur_sc=sc;cur=m
   if sc>alpha:alpha=sc
  if not STOP:best=cur
  depth+=1
 u=to_uci(best)
 return u if u in legal else fb
ENV_URL=os.getenv("MAKEFUN_ENV_URL","")
def post(path,body):
 req=ur.Request(ENV_URL+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
 try:
  with ur.urlopen(req)as res:
   return res.status,json.load(res)
 except urllib.error.HTTPError as e:
  return e.code,{}
def main():
 while True:
  st,g=post("/game",{})
  while g.get("status")=="your_move":
   legal=g["legal_moves"]
   try:
    mv=pick_move(g["fen"],legal)
   except Exception:
    mv=greedy(g["fen"],legal)
   for cand in(mv,greedy(g["fen"],legal),legal[0]):
    st,g2=post("/move",{"game":g["game"],"move":cand})
    if st!=400:break
   g=g2
   if g.get("status")not in("your_move","over"):
    break
  if g.get("status")=="done":break
if ENV_URL:
 main()
