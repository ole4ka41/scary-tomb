from pathlib import Path
import numpy as np
import wave
SR=44100; duration=38; beat=60/72
rng=np.random.default_rng(311)
out=np.zeros((SR*duration,2),dtype=np.float64)
def note(midi,start,length,amp=0.12,kind='keys',pan=0):
 n=int(length*SR); t=np.arange(n)/SR; f=440*2**((midi-69)/12)
 if kind=='bell':
  env=(1-np.exp(-t/0.006))*np.exp(-t/0.95)*np.minimum(1,(length-t)/0.15)
  y=sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t*d) for r,a,d in [(1,1,0),(2.756,.18,1),(5.404,.07,2)])*env
 elif kind=='pad':
  env=np.minimum(1,t/.7)*np.minimum(1,(length-t)/.9)
  y=(np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*(f*1.002)*t)+.12*np.sin(2*np.pi*2*f*t))*env*.6
 else:
  env=(1-np.exp(-t/.008))*np.exp(-t/1.15)*np.minimum(1,(length-t)/.18)
  y=sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t*(r-1)*.6) for r,a in [(1,1),(2,.25),(3,.10),(4,.035)])*env
 y*=amp
 i=int(start*SR); count=min(n,len(out)-i)
 if count<=0:return
 gains=np.array([np.sqrt((1-pan)/2),np.sqrt((1+pan)/2)])
 out[i:i+count]+=y[:count,None]*gains
# Eleven bars: a cautious B minor opening resolves into D major.
chords=[(47,[59,62,66]),(43,[55,59,62]),(50,[57,62,66]),(45,[57,61,64]),(47,[59,62,66]),(43,[55,59,62]),(40,[55,59,64]),(45,[57,61,64]),(50,[57,62,66]),(43,[55,59,62]),(50,[57,62,66])]
melody=[[None,78,76,74],[71,None,74,76],[78,81,78,76],[73,None,76,73],[74,78,81,78],[79,78,74,71],[76,None,79,78],[76,73,69,None],[78,81,86,83],[79,78,76,74],[78,76,74,None]]
for bar,(bass,ch) in enumerate(chords):
 start=bar*4*beat
 intensity=.72 if bar<2 else (.65 if bar in (6,7) else .9)
 if bar==10:intensity=.7
 note(bass,start,3.8*beat,.095*intensity,'keys',-.15)
 for k,m in enumerate(ch):note(m-12,start,4.1*beat,.028*intensity,'pad',(-.45,0,.45)[k])
 for k in range(8):
  m=ch[[0,1,2,1,0,2,1,2][k]]
  note(m,start+k*.5*beat,1.5*beat,.07*intensity,'keys',(-.28 if k%2 else .28))
 for k,m in enumerate(melody[bar]):
  if m is not None:note(m,start+k*beat+.025,2.0*beat,.075*intensity,'bell',.12)
# Short answering sparkles as the fireflies return.
for off,m in [(25.2,86),(25.6,90),(26.0,93),(29.2,85),(29.6,88),(30.0,90)]:note(m,off,1.6,.035,'bell',-.35)
# Resolve before the address card, with a soft tail.
for m in [50,62,66,69,74]:note(m,35,3,.045,'keys',0)
# Simple stereo room reflections.
dry=out.copy()
for sec,g in [(.071,.12),(.137,.09),(.233,.065),(.391,.045),(.613,.025)]:
 d=int(sec*SR);out[d:]+=dry[:-d,::-1]*g
fadein=np.minimum(1,np.arange(len(out))/int(.16*SR))
fadeout=np.minimum(1,(len(out)-1-np.arange(len(out)))/int(2.3*SR))
out*= (fadein*fadeout)[:,None]
peak=np.max(np.abs(out));out*=.84/max(peak,1e-9)
p=Path('/workspace/outputs/little-light/little-light-original.wav')
with wave.open(str(p),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype('<i2').tobytes())
print('Duration',len(out)/SR,'peak',float(np.max(np.abs(out))),'RMS',float(np.sqrt(np.mean(out*out))))
