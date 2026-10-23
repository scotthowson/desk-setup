from pathlib import Path
import numpy as np,wave
R=Path(__file__).resolve().parent;sr=48000;dur=30;t=np.arange(sr*dur)/sr;music=np.zeros(len(t));rng=np.random.default_rng(37)
# Original ambient cue: slowly overlapping voicings, a soft sub and four transition swells.
chords=[([110,220,261.626,329.628,493.883],0,8),([87.307,174.614,220,261.626,329.628],6.4,7),([130.813,196,246.942,293.665,391.995],11.4,7),([97.999,196,261.626,293.665,440],16.4,7),([110,220,261.626,329.628,493.883],21.4,7),([87.307,174.614,220,261.626,329.628],26.4,3.6)]
for notes,start,length in chords:
 u=t-start;env=np.clip(u/1.5,0,1)*np.clip((length-u)/2,0,1);env[(u<0)|(u>length)]=0
 for j,f in enumerate(notes):
  phase=j*.7;sig=np.sin(2*np.pi*f*t+phase)+.17*np.sin(2*np.pi*2*f*t+.12*np.sin(t*.4))+ .04*np.sin(2*np.pi*3*f*t)
  music+=.013*sig*env*(.9+.1*np.sin(2*np.pi*.1*t+j))
for st in [0,7,12,17,22,27]:
 u=t-st;env=np.exp(-np.maximum(u,0)*1.4)*(u>=0);music+=.025*np.sin(2*np.pi*(55*t+3*np.exp(-np.maximum(u,0)*6)))*env
 # nearly inaudible filtered air at the cuts
 noise=rng.normal(0,1,len(t));noise=np.convolve(noise,np.ones(90)/90,mode='same');music+=noise*.045*np.exp(-((u+.04)/.18)**2)
fade=np.clip(t/1.6,0,1)*np.clip((30-t)/2.2,0,1);music*=fade
stereo=np.stack([music,music*.97+.004*np.sin(2*np.pi*220.2*t)*fade],axis=1);stereo=np.clip(stereo,-.9,.9)
with wave.open(str(R/'ambient-score.wav'),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((stereo*32767).astype('<i2').tobytes())
print('Original ambient score ready')
