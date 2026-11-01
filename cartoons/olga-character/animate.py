from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, subprocess, wave
import numpy as np

P=Path('/workspace/outputs/olga-character');W,H=720,900;FPS=24
FONT='/workspace/shared/fonts/CoolveticaRg-Regular.ttf'
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def mix(a,b,x):return a+(b-a)*x
def ell(d,b,c,o=None,w=1):d.ellipse(tuple(round(x) for x in b),fill=c,outline=o,width=w)
def ln(d,p,c,w):d.line([(round(x),round(y)) for x,y in p],fill=c,width=w,joint='curve')
def rr(d,b,r,c,o=None,w=1):d.rounded_rectangle(tuple(round(x) for x in b),radius=r,fill=c,outline=o,width=w)
def txt(d,s,y,size=30,color='#f9e8c3'):
 f=ImageFont.truetype(FONT,size);b=d.textbbox((0,0),s,font=f);d.text(((W-b[2])/2,y),s,font=f,fill=color)

def make_bg():
 im=Image.new('RGB',(W,H));d=ImageDraw.Draw(im)
 for y in range(H):
  u=y/H;d.line((0,y,W,y),fill=tuple(round(mix(a,b,u)) for a,b in zip((16,31,47),(47,60,70))))
 rr(d,(42,157,287,473),18,'#536f7a','#8a9e9b',3)
 for x in range(52,280):
  u=(x-52)/228;d.line((x,167,x,462),fill=(int(112+55*u),int(140+29*u),int(146+10*u)))
 d.polygon([(52,400),(105,337),(160,389),(219,310),(278,366),(278,462),(52,462)],fill='#546f71')
 ln(d,[(166,159),(166,472)],'#d7c6a2',7);ln(d,[(42,319),(287,319)],'#d7c6a2',7)
 d.polygon([(0,759),(720,759),(720,900),(0,900)],fill='#786453')
 ln(d,[(0,760),(720,760)],'#ac9273',4)
 for j in range(6):ln(d,[(j*155-130,900),(j*90+60,760)],'#8f7861',2)
 # Pendant light and warm halo.
 ln(d,[(575,0),(575,187)],'#b7a27a',3)
 for r in range(80,5,-5):ell(d,(575-r,220-r,575+r,220+r),(int(45+(80-r)*.35),int(51+(80-r)*.28),int(53+(80-r)*.14)))
 d.pieslice((521,168,629,253),180,360,fill='#cda666',outline='#eecb86',width=3)
 ell(d,(539,202,611,223),'#ffda8b')
 # Plant.
 rr(d,(643,643,695,744),9,'#c2a58a','#e7c9a7',2)
 ln(d,[(668,653),(667,480)],'#6e9b80',6)
 for y,side in [(625,-1),(594,1),(558,-1),(526,1)]:
  d.polygon([(668,y+12),(668+side*44,y-16),(668+side*36,y-42),(668+side*8,y-25)],fill='#80aa8e')
 return im
BG=make_bg()

def tablet(im,t):
 d=ImageDraw.Draw(im)
 # Independent tablet console and easel.
 rr(d,(488,666,689,688),7,'#c6aa88','#eed9b6',2)
 for x in [508,664]:rr(d,(x,687,x+10,785),4,'#ad8d69')
 ln(d,[(573,610),(537,668)],'#8c795e',8);ln(d,[(589,610),(625,668)],'#8c795e',8)
 rr(d,(475,427,687,630),20,'#111c2a','#dab471',4)
 rr(d,(489,441,673,613),10,'#2b4157')
 if t<8.1:
  # Preview frame; play button becomes pressed briefly.
  ell(d,(503,458,650,604),'#4d6875')
  for x,y in [(518,494),(638,472),(627,584)]:ell(d,(x-3,y-3,x+3,y+3),'#f6da97')
  r=29 if 7.75<t<8.1 else 33
  ell(d,(581-r,527-r,581+r,527+r),'#e3b864')
  d.polygon([(573,511),(573,543),(595,527)],fill='#253447')
 else:
  u=t-8.1
  # Original miniature animated rocket film on the screen.
  for j in range(19):
   x=499+(j*43)%165;y=450+(j*29+u*35)%137
   ell(d,(x-1,y-1,x+2,y+2),'#fff0bb')
  ell(d,(610,460,650,500),'#e1bb7a')
  rx=550+math.sin(u*1.7)*23;ry=554-u*9
  d.polygon([(rx-9,ry+19),(rx+9,ry+19),(rx,ry+45+math.sin(t*24)*6)],fill='#f5aa54')
  d.polygon([(rx-11,ry-20),(rx,ry-39),(rx+11,ry-20),(rx+11,ry+20),(rx-11,ry+20)],fill='#f4e9d4')
  ell(d,(rx-6,ry-12,rx+6,ry),'#7cb5c5','#2d566b',2)
  d.polygon([(rx-11,ry+6),(rx-24,ry+23),(rx-10,ry+20)],fill='#dc9b6d')
  d.polygon([(rx+11,ry+6),(rx+24,ry+23),(rx+10,ry+20)],fill='#dc9b6d')
  rr(d,(502,597,660,601),2,'#607489')
  rr(d,(502,597,502+min(158,u*38),601),2,'#f1ce84')
 ell(d,(577,619,584,625),'#687581')

def woman(im,t):
 d=ImageDraw.Draw(im)
 stand=smooth((t-1.8)/1.8);walk=smooth((t-3.8)/2.8)
 x=mix(192,425,walk)
 walking=3.8<t<6.6
 bob=math.sin((t-3.8)*12)*3 if walking else math.sin(t*2)*.6
 hip=mix(647,595,stand)+bob;shoulder=hip-148;head=shoulder-100
 stride=math.sin((t-3.8)*10)*29 if walking else 0
 # Ground shadow.
 ell(d,(x-63,777,x+75,794),'#594f48')
 # Chair behind seated body.
 rr(d,(109,505,230,660),22,'#57646c','#9d9c8e',3)
 ln(d,[(142,651),(135,781)],'#a89373',8);ln(d,[(220,651),(236,781)],'#a89373',8)
 # Legs interpolate from bent seated knees into standing/walking.
 for side in [-1,1]:
  hx=x+side*18; kx=mix(x+61+side*12,x+side*18+stride*side,stand)
  ky=mix(696,690,stand);footx=x+side*22-stride*side
  ln(d,[(hx,hip),(kx,ky),(footx,774)],'#d4b18a' if side==1 else '#bda07d',26)
  rr(d,(footx-13,766,footx+36,784),9,'#3b3538','#b38f63',2)
 # Hair behind shoulders: original stylized silhouette, not a photo cutout.
 ell(d,(x-60,head-69,x+60,head+103),'#8e5839','#563e32',3)
 d.polygon([(x-58,head-15),(x-64,shoulder+102),(x-22,shoulder+84),(x+40,shoulder+95),(x+63,head+5)],fill='#9d6740')
 # Jacket and shirt.
 d.polygon([(x-47,shoulder),(x+39,shoulder),(x+58,hip+11),(x-54,hip+11)],fill='#e6c8a0',outline='#a58867')
 d.polygon([(x-16,shoulder+1),(x+18,shoulder+1),(x+24,hip+3),(x-21,hip+3)],fill='#faf3e6')
 d.polygon([(x-38,shoulder),(x-10,shoulder+26),(x-26,shoulder+52),(x-8,shoulder+79),(x-18,hip+5),(x-47,hip+5)],fill='#d6b990')
 d.polygon([(x+30,shoulder),(x+9,shoulder+28),(x+26,shoulder+49),(x+13,shoulder+77),(x+20,hip+8),(x+51,hip+8)],fill='#f3d7af')
 # Neck.
 rr(d,(x-14,head+40,x+15,shoulder+15),10,'#e8ad88')
 # Relaxed left arm.
 ln(d,[(x-38,shoulder+15),(x-58,shoulder+79),(x-45,hip-5)],'#dcc099',25)
 ell(d,(x-57,hip-16,x-34,hip+15),'#efbc94','#a97559',1)
 # Face and features, angled slightly toward tablet.
 ell(d,(x-43,head-53,x+46,head+58),'#efbb94','#a77455',2)
 ell(d,(x+36,head-1,x+51,head+23),'#e9ad88')
 # Side-swept hair over forehead.
 d.polygon([(x-48,head+12),(x-48,head-34),(x-30,head-66),(x+8,head-71),(x+39,head-47),(x+43,head-22),(x+15,head-42),(x-14,head-19)],fill='#ab7447')
 for k in range(8):
  xx=x-52+k*4
  ln(d,[(xx+19,head-48),(xx,head+10),(xx-5,head+97),(xx+5,head+145)],'#c99159' if k%2 else '#e1ab70',2)
 for k in range(4):ln(d,[(x+34+k*4,head-23),(x+50+k*3,head+45),(x+40+k*5,head+125)],'#c88d54',2)
 # Eyebrows, blinking eyes, lashes.
 blink=int(t*24)%97 in (0,1,2)
 for ex in [x-13,x+22]:
  d.arc((ex-9,head-11,ex+9,head-1),185,345,fill='#825238',width=2)
  if blink:ln(d,[(ex-7,head+3),(ex+7,head+3)],'#514032',2)
  else:
   ell(d,(ex-8,head-1,ex+9,head+8),'#fff5e6')
   ell(d,(ex-1,head-1,ex+6,head+8),'#63776b')
   ell(d,(ex+1,head,ex+5,head+7),'#333a36')
   ell(d,(ex+1,head,ex+3,head+2),'white')
 ln(d,[(x+8,head+9),(x+13,head+20),(x+5,head+22)],'#cb8e6c',2)
 ell(d,(x-23,head+18,x-7,head+25),'#e69c84')
 d.arc((x-3,head+26,x+23,head+43),0,170,fill='#aa5f55',width=3)
 # Small earring and necklace.
 ell(d,(x+43,head+25,x+50,head+35),'#f6d486')
 ln(d,[(x-12,shoulder+4),(x,shoulder+31),(x+14,shoulder+4)],'#c29b54',2)
 ell(d,(x-3,shoulder+27,x+4,shoulder+34),'#e3b961')
 # Right arm reaches and taps the screen, then relaxes slightly.
 reach=smooth((t-6.6)/1.1)*(1-.36*smooth((t-8.5)/1.1))
 sx=x+37;sy=shoulder+16
 ex=mix(x+59,500,reach);ey=mix(shoulder+79,481,reach)
 wx=mix(x+46,569,reach);wy=mix(hip-8,527,reach)
 ln(d,[(sx,sy),(ex,ey)],'#ebcfa8',26)
 ln(d,[(ex,ey),(mix(ex,wx,.50),mix(ey,wy,.50))],'#ebcfa8',24)
 ln(d,[(mix(ex,wx,.45),mix(ey,wy,.45)),(wx,wy)],'#efbc94',17)
 ell(d,(wx-9,wy-9,wx+12,wy+9),'#efbc94','#ae795a',1)
 if reach>.85:ln(d,[(wx+4,wy),(wx+15,wy)],'#efbc94',8)
 # Golden watch on the animated wrist.
 bx=mix(ex,wx,.72);by=mix(ey,wy,.72)
 ell(d,(bx-8,by-9,bx+8,by+9),'#d5a34e','#f9d78d',2)
 ell(d,(bx-4,by-5,bx+4,by+5),'#f9edc7')
 return x

def desk(im):
 d=ImageDraw.Draw(im)
 for x in [48,307]:rr(d,(x,628,x+14,787),4,'#b29673')
 rr(d,(22,604,345,632),8,'#d0b291','#efdab9',2)
 # Open laptop.
 d.polygon([(60,602),(45,511),(173,511),(193,602)],fill='#68727b',outline='#b1b9b7')
 ell(d,(97,546,130,578),'#d6b77d')
 f=ImageFont.truetype(FONT,22);d.text((102,549),'AI',font=f,fill='#fff2cb')
 d.polygon([(57,601),(192,601),(232,613),(80,613)],fill='#b6b8b2')
 rr(d,(260,574,301,604),8,'#fff2d8','#dec59e',2)
 d.arc((290,577,315,600),270,90,fill='#e6cba6',width=5)
 ell(d,(247,600,314,610),'#e7d0aa')

def frame(t):
 im=BG.copy();d=ImageDraw.Draw(im)
 txt(d,'LET’S BRING IDEAS TO LIFE.',68,35)
 ln(d,[(191,118),(529,118)],'#d4b270',2)
 tablet(im,t);woman(im,t);desk(im)
 if 7.8<t<8.6:
  u=(t-7.8)/.8;r=15+u*35
  d=ImageDraw.Draw(im);d.ellipse((581-r,527-r,581+r,527+r),outline='#ffe3a0',width=2)
 if t>9.5:
  d=ImageDraw.Draw(im);txt(d,'YOUR STORY. IN MOTION.',818,31)
  txt(d,'instagram.com/ole4ka.ivanowa',858,20,'#e6c68c')
 # Fade in/out; no changes to source photograph are used.
 fac=min(1,t/.35,(12-t)/.5)
 if fac<1:im=Image.blend(Image.new('RGB',(W,H),'#101f2f'),im,max(0,fac))
 return im

if __name__=='__main__':
 for t in [1,3.5,5.5,7.8,10.5]:frame(t).save(P/f'preview-{t}.jpg')
 # Original music excerpt plus a soft synthesized touch confirmation.
 with wave.open('/workspace/outputs/little-light/little-light-original.wav','rb') as r:
  sr=r.getframerate();audio=np.frombuffer(r.readframes(sr*12),dtype='<i2').reshape(-1,2).astype(float)/32768
 n=int(.23*sr);s=np.arange(n)/sr;ping=.08*np.sin(2*np.pi*880*s)*np.exp(-s*18)*np.minimum(1,s/.008)
 start=int(8.02*sr);audio[start:start+n]+=ping[:,None]
 fade=np.minimum(1,np.arange(len(audio))/(sr*.4))*np.minimum(1,(len(audio)-1-np.arange(len(audio)))/(sr*1.2))
 audio*=fade[:,None]*.8
 with wave.open(str(P/'sound.wav'),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
 cmd=['ffmpeg','-y','-v','warning','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(P/'sound.wav'),'-vf','scale=1080:1350:flags=lanczos','-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-pix_fmt','yuv420p','-t','12','-movflags','+faststart','-threads','4',str(P/'olga-character-animation.mp4')]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for i in range(12*FPS):
   proc.stdin.write(frame(i/FPS).tobytes())
   if i%(3*FPS)==0:print('Rendered',i//FPS,'seconds',flush=True)
 finally:proc.stdin.close()
 if proc.wait():raise SystemExit('Encoding failed')
 print('Done',flush=True)
