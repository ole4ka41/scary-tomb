from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random, subprocess
from pathlib import Path

P=Path('/workspace/outputs/little-light/cartoon')
W,H,FPS=540,960,24
font='/workspace/shared/fonts/CoolveticaRg-Regular.ttf'
def ft(n): return ImageFont.truetype(font,n)
def lerp(a,b,u): return a+(b-a)*max(0,min(1,u))
def smooth(u): u=max(0,min(1,u)); return u*u*(3-2*u)
def ellipse(d,box,fill,outline=None,width=1): d.ellipse(tuple(int(v) for v in box),fill=fill,outline=outline,width=width)
def line(d,points,fill,width): d.line([(int(x),int(y)) for x,y in points],fill=fill,width=width,joint='curve')
def text(im,s,y,size=34,color='#fff5dd'):
 d=ImageDraw.Draw(im); f=ft(size); box=d.textbbox((0,0),s,font=f); x=(W-(box[2]-box[0]))/2
 d.text((x+1,y+3),s,font=f,fill='#172d35',stroke_width=3,stroke_fill='#172d35')
 d.text((x,y),s,font=f,fill=color)

def background(night=False,home=False):
 im=Image.new('RGB',(W,H)); pix=im.load()
 top=(18,38,64) if night else (80,120,138); bottom=(51,94,100) if night else (187,201,159)
 for y in range(H):
  c=tuple(int(lerp(top[k],bottom[k],y/H)) for k in range(3))
  ImageDraw.Draw(im).line((0,y,W,y),fill=c)
 d=ImageDraw.Draw(im)
 rng=random.Random(19)
 for j in range(11):
  x=rng.randint(-60,560); width=rng.randint(18,45)
  d.polygon([(x,0),(x+width,0),(x+width+25,730),(x-10,730)],fill='#345b65' if night else '#73948e')
 for x,y,r in [(-20,130,170),(145,-15,155),(340,20,170),(565,125,165)]:
  ellipse(d,(x-r,y-r,x+r,y+r),'#183c4c' if night else '#426d67')
  ellipse(d,(x-r+20,y-r+20,x+r-30,y+r-20),'#234957' if night else '#507d6c')
 d.polygon([(0,720),(100,678),(215,705),(345,675),(540,705),(540,960),(0,960)],fill='#244e4a' if night else '#668a64')
 ellipse(d,(-180,730,740,1240),'#315a4b' if night else '#809560')
 # Winding woodland trail.
 d.polygon([(260,690),(302,690),(340,800),(445,960),(70,960),(210,795)],fill='#666551' if night else '#b8ac83')
 for j in range(55):
  x=rng.randrange(540); y=rng.randrange(730,960)
  if abs(x-270)<75: continue
  line(d,[(x-4,y),(x,y-12),(x+2,y)],'#77a47c' if night else '#b6c18a',2)
  if j%5==0: ellipse(d,(x-3,y-15,x+3,y-9),'#b2b5a2' if night else '#e5d6a6')
 if home:
  d.polygon([(338,330),(480,280),(540,340),(540,830),(315,830)],fill='#493e3c')
  for x in (370,405,470,508):line(d,[(x,350),(x-15,580),(x+5,820)],'#625047',6)
  d.rounded_rectangle((359,598,475,827),radius=58,fill='#d99a4c',outline='#322f30',width=12)
  d.rounded_rectangle((373,612,461,826),radius=44,fill='#ffd58a')
  line(d,[(411,694),(411,819)],'#c48c52',3)
  ellipse(d,(438,740,447,749),'#63452e')
  for x,y in [(329,809),(482,815),(350,835)]:ellipse(d,(x-30,y-12,x+30,y+12),'#544943')
  text(im,'HOME',560,21,'#ffe3a0')
 return im

DAY=background(); NIGHT=background(True); HOME=background(True,True)

def glow(im,x,y,r=60,strength=180):
 lay=Image.new('RGBA',im.size); d=ImageDraw.Draw(lay)
 ellipse(d,(x-r,y-r,x+r,y+r),(255,198,72,strength))
 lay=lay.filter(ImageFilter.GaussianBlur(r*.5));im.paste(lay,(0,0),lay)

def firefly(im,x,y,t,scale=1,lit=True):
 if lit:glow(im,x,y+9*scale,36*scale,105)
 d=ImageDraw.Draw(im);s=scale
 wing=abs(math.sin(t*24))
 for sign in (-1,1):
  ellipse(d,(x+sign*11*s-13*s,y-20*s-10*s*wing,x+sign*11*s+13*s,y+5*s),'#d5e9dd', '#82b1b3',1)
 ellipse(d,(x-11*s,y-5*s,x+11*s,y+24*s),'#ffcf62' if lit else '#b4a16f','#50452e',2)
 ellipse(d,(x-12*s,y-17*s,x+12*s,y+7*s),'#345c60','#1c3c43',2)
 for dx in (-5,5):
  ellipse(d,(x+(dx-2)*s,y-10*s,x+(dx+2)*s,y-5*s),'#fff7d6')
 line(d,[(x-5*s,y-15*s),(x-9*s,y-23*s)],'#203e47',2)
 line(d,[(x+5*s,y-15*s),(x+9*s,y-23*s)],'#203e47',2)

def hedgehog(im,x,y,t,pose='stand',scale=1):
 # Draw at fixed local coordinates, then scale as a whole for consistent design.
 layer=Image.new('RGBA',(270,275));d=ImageDraw.Draw(layer)
 ellipse(d,(32,226,232,256),(15,30,25,45))
 bob=math.sin(t*8)*3 if pose=='walk' else math.sin(t*2)*1.4
 cy=137+bob
 ellipse(d,(31,64+bob,193,235+bob),'#775044','#453b36',3)
 for k in range(33):
  a=math.radians(92+k*6);cx=113; rr=85
  px=cx+math.cos(a)*rr;py=cy+math.sin(a)*rr
  qx=cx+math.cos(a-.10)*(rr-17);qy=cy+math.sin(a-.10)*(rr-17)
  rx=cx+math.cos(a+.10)*(rr-17);ry=cy+math.sin(a+.10)*(rr-17)
  d.polygon([(int(qx),int(qy)),(int(px+math.cos(a)*14),int(py+math.sin(a)*14)),(int(rx),int(ry))],fill='#b28a65',outline='#604639')
 for j in range(17):
  a=j*.73;xx=70+((j*37)%89);yy=93+((j*29)%96)
  line(d,[(xx,yy),(xx-7,yy+12)],'#c6a17a',2)
 step=math.sin(t*9)*8 if pose=='walk' else 0
 ellipse(d,(67+step,220,111+step,246),'#c9a17d','#5b4435',2)
 ellipse(d,(137-step,220,180-step,246),'#c9a17d','#5b4435',2)
 # Face and rounded ear.
 ellipse(d,(138,73+bob,184,121+bob),'#d3ad84','#684c3e',2)
 ellipse(d,(149,84+bob,175,110+bob),'#b98270')
 ellipse(d,(118,100+bob,215,212+bob),'#e9c89c','#735441',2)
 d.polygon([(177,144+bob),(242,173+bob),(200,195+bob)],fill='#e9c89c')
 ellipse(d,(226,164+bob,245,181+bob),'#3e3434')
 blink=(int(t*24)%101 in (0,1,2))
 if blink:line(d,[(176,135+bob),(190,136+bob)],'#332b2c',3)
 else:
  ellipse(d,(174,124+bob,193,146+bob),'#302d30')
  ellipse(d,(178,127+bob,184,133+bob),'#fff7e1')
 ellipse(d,(190,158+bob,207,168+bob),'#d8957e')
 if pose=='sad':line(d,[(204,185+bob),(215,181+bob)],'#735040',2)
 else:d.arc((195,172+bob,221,189+bob),0,100,fill='#735040',width=2)
 d.rounded_rectangle((122,193+bob,204,211+bob),radius=8,fill='#538d78',outline='#315d53',width=2)
 d.polygon([(135,208+bob),(157,208+bob),(147,239),(128,231)],fill='#65a189')
 if pose in ('reach','umbrella'):
  line(d,[(154,207),(186,184),(215,161 if pose=='umbrella' else 189)],'#d6b18b',17)
  ellipse(d,(202,151 if pose=='umbrella' else 179,224,173 if pose=='umbrella' else 201),'#e8c497','#735441',2)
 else:ellipse(d,(147,205,176,228),'#e8c497','#735441',2)
 layer=layer.resize((int(270*scale),int(275*scale)),Image.Resampling.LANCZOS)
 im.paste(layer,(int(x-135*scale),int(y-245*scale)),layer)

def leaf(im,x,y,s=1):
 d=ImageDraw.Draw(im)
 pts=[(x-80*s,y+5*s),(x-60*s,y-35*s),(x-15*s,y-54*s),(x+42*s,y-39*s),(x+88*s,y+2*s),(x+20*s,y+20*s),(x-30*s,y+19*s)]
 d.polygon([(int(a),int(b)) for a,b in pts],fill='#69aa77',outline='#315e54')
 line(d,[(x-75*s,y+4*s),(x+80*s,y+1*s)],'#b8d691',3)
 for a in (-45,-15,15,45):line(d,[(x+a*s,y+3*s),(x+(a-12)*s,y-25*s)],'#91bf83',2)

def rain(im,t,amount):
 d=ImageDraw.Draw(im)
 for j in range(amount):
  x=(j*73+t*76)%590-25;y=(j*137+t*450)%1020-30
  line(d,[(x,y),(x-8,y+25)],'#c3d7d5',1)

def frame(t):
 scene=min(6,int(t/5));u=(t%5)/5
 if t>=35:
  im=HOME.copy();hedgehog(im,295,805,34,'stand',.72)
  for j in range(9):firefly(im,115+j*35,450+math.sin(j+t)*25,t,.35)
  shade=Image.new('RGB',(W,H),'#102b34');im=Image.blend(im,shade,.83)
  d=ImageDraw.Draw(im);line(d,[(65,384),(475,384)],'#f6ce78',2)
  text(im,'A LITTLE LIGHT.',416,40,'#ffe5a6');text(im,'A BIG DIFFERENCE.',465,34)
  text(im,'Follow for more little stories',552,23)
  text(im,'instagram.com/ole4ka.ivanowa',602,25,'#f5cf7f')
  if t>37.5: im=Image.blend(im,Image.new('RGB',(W,H),'#101e29'),smooth((t-37.5)/.5))
  return im
 night=smooth((t-20)/5)
 im=Image.blend(DAY,NIGHT,night) if scene<6 else HOME.copy()
 d=ImageDraw.Draw(im)
 if scene<=3:
  ellipse(d,(228,650,548,811),'#89b8bd','#5d8f9d',3)
  for j in range(4):d.arc((258-j*5,690-j*9,493+j*7,780+j*9),0,180,fill='#b0d1ca',width=2)
  ellipse(d,(362,683,421,714),'#6e7d80','#495f67',2)
  ellipse(d,(368,683,416,701),'#acb3a4')
 if scene==0:
  hedgehog(im,127,757,t,'sad')
  firefly(im,391,663+math.sin(t*3)*2,t,.8,True)
  if t<.65:
   yy=lerp(240,697,t/.65);ellipse(d,(330,yy-18,344,yy+9),'#d5e8df')
  else:
   r=20+((t-.65)*50)%55
   d.arc((337-r,698-r/3,337+r,698+r/3),0,360,fill='#d6e9da',width=2)
  if t<3.8:
   d.rounded_rectangle((34,145,506,262),radius=23,fill='#234853')
   text(im,'EVEN TINY HEROES',166,34);text(im,'NEED HELP.',210,38,'#f9d47d')
 elif scene==1:
  hedgehog(im,146,757,t,'reach')
  leaf(im,272+smooth(u)*20,682,.54)
  firefly(im,391,663,t,.8)
 elif scene==2:
  hedgehog(im,150,757,t,'reach')
  endx=lerp(272,389,smooth(u*1.8));endy=lerp(602,700,smooth(u*1.8))
  line(d,[(248,739),(endx,endy)],'#755743',10);line(d,[(248,736),(endx,endy-3)],'#bfa177',3)
  firefly(im,391,663,t,.8)
 elif scene==3:
  line(d,[(248,739),(389,700)],'#755743',10);line(d,[(248,736),(389,697)],'#bfa177',3)
  hedgehog(im,150,757,t,'umbrella')
  q=smooth(u*1.5);firefly(im,lerp(391,235,q),lerp(663,705,q),t,.8)
  line(d,[(232,676),(247,574)],'#5c7850',5);leaf(im,247,568,.95)
 elif scene==4:
  hedgehog(im,181,767,t,'sad')
  firefly(im,lerp(265,610,smooth(u)),lerp(620,350,smooth(u)),t,.8)
  # Fork signs communicate that the hedgehog is lost.
  line(d,[(366,609),(366,760)],'#755e49',10)
  d.polygon([(312,600),(394,600),(416,616),(394,632),(312,632)],fill='#a08c66')
  d.polygon([(334,644),(411,644),(411,674),(334,674),(315,660)],fill='#a08c66')
  if u>.6:text(im,'?',471,60,'#f4d78f')
 elif scene==5:
  hedgehog(im,181,767,t,'stand')
  fx=lerp(585,307,smooth(u*1.7));fy=lerp(426,588,smooth(u*1.7))
  for j in range(12):
   x=fx+45+j*12;y=fy-40-math.sin(j*.8+t*2)*35
   firefly(im,x,y,t,.25+(j%3)*.06)
  firefly(im,fx,fy+math.sin(t*4)*7,t,.85)
 elif scene==6:
  q=smooth(u);hx=lerp(115,290,q);hy=lerp(831,806,q)
  hedgehog(im,hx,hy,t,'walk' if u<.85 else 'stand',.78)
  for j in range(10):
   x=lerp(hx+80,425,j/10);y=660-math.sin(j/10*math.pi)*65+math.sin(t*3+j)*8
   firefly(im,x,y,t,.32)
  firefly(im,hx+90,665+math.sin(t*4)*9,t,.7)
  if u>.55:text(im,'Kindness finds its way back.',310,28,'#ffe1a0')
 if t<19.5:rain(im,t,65 if t<5 else 40)
 # Subtle cinematic vignette; keep the character area clear.
 return im

if __name__=='__main__':
 for sec in [1,8,13,18,23,28,33,36]:frame(sec).save(P/f'frame-{sec}.jpg')
 cmd=['ffmpeg','-y','-v','warning','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i','/workspace/outputs/little-light/little-light-original.wav','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-af','afade=t=out:st=36:d=2','-t','38','-movflags','+faststart','-threads','4',str(P/'little-light-cartoon.mp4')]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for i in range(38*FPS):
   proc.stdin.write(frame(i/FPS).tobytes())
   if i%(5*FPS)==0:print('Rendered',i//FPS,'seconds',flush=True)
 finally:proc.stdin.close()
 if proc.wait():raise SystemExit('Encoding failed')
 print('Done',flush=True)
