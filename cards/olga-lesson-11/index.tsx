import React from 'react';
import {AbsoluteFill, Audio, Composition, Img, interpolate, registerRoot, staticFile, useCurrentFrame} from 'remotion';

const Spark: React.FC<{x:number;y:number;t:number;delay:number}>=({x,y,t,delay})=>{
 const phase=(t+delay)%3.8;
 const pulse=Math.pow(Math.max(0,Math.sin(phase/3.8*Math.PI)),8);
 return <g transform={`translate(${x},${y}) rotate(${t*9})`} opacity={pulse*.85}>
  <path d="M0 -23 L4 -4 L23 0 L4 4 L0 23 L-4 4 L-23 0 L-4 -4Z" fill="#fff5c0"/>
  <circle r="4" fill="white"/>
 </g>;
};

const Card:React.FC=()=>{
 const f=useCurrentFrame(),t=f/30;
 // Full original image always stays within frame: no clipping of headings or face.
 const z=interpolate(f,[0,210,419],[.965,.99,.965]);
 const reveal=interpolate(f,[0,18],[0,1],{extrapolateRight:'clamp'});
 return <AbsoluteFill style={{backgroundColor:'#111521'}}>
  <Img src={staticFile('card.png')} style={{position:'absolute',width:'100%',height:'100%',objectFit:'fill',filter:'blur(25px) brightness(.52)',transform:'scale(1.08)'}}/>
  <AbsoluteFill style={{transform:`scale(${z})`,opacity:reveal}}>
   <Img src={staticFile('card.png')} style={{width:'100%',height:'100%'}}/>
   <svg viewBox="0 0 1200 1312" style={{position:'absolute',inset:0,width:'100%',height:'100%'}}>
    <defs>
     <filter id="gold"><feGaussianBlur stdDeviation="5"/></filter>
     <linearGradient id="sheen"><stop offset="0" stopColor="#ffe2a0" stopOpacity="0"/><stop offset=".5" stopColor="#fff3bf" stopOpacity=".28"/><stop offset="1" stopColor="#ffe2a0" stopOpacity="0"/></linearGradient>
     <clipPath id="banner"><rect x="570" y="17" width="513" height="60" rx="30"/></clipPath>
    </defs>
    <g clipPath="url(#banner)"><rect x={interpolate((t%7),[0,7],[340,1250])} y="17" width="160" height="60" fill="url(#sheen)" transform="skewX(-15)"/></g>
    {[35,272,498,723].map((x,i)=>{
      const local=t-(2.1+i*2.0);
      const opacity=local<0||local>2?0:Math.sin(local/2*Math.PI)*.7;
      return <g key={x} opacity={opacity}>
       <rect x={x} y="887" width={i===0?204:191} height="210" rx="37" fill="none" stroke="#ffc85e" strokeWidth="15" filter="url(#gold)"/>
       <rect x={x} y="887" width={i===0?204:191} height="210" rx="37" fill="none" stroke="#fff0b4" strokeWidth="3"/>
      </g>;
    })}
    {[[1122,107],[1133,153],[1167,421],[642,428],[967,816],[111,640],[68,1127]].map(([x,y],i)=><Spark key={i} x={x} y={y} t={t} delay={i*.47}/>)}
    <rect x="969" y="153" width="168" height="95" rx="25" fill="none" stroke="#ffe6a5" strokeWidth="3" opacity={.12+.18*Math.sin(t*2.1)}/>
   </svg>
  </AbsoluteFill>
  <Audio src={staticFile('music.m4a')}/>
 </AbsoluteFill>;
};
registerRoot(()=> <Composition id="OlgaCard" component={Card} width={1200} height={1312} fps={30} durationInFrames={420}/>);
