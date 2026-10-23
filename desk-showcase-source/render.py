from pathlib import Path
import numpy as np, moderngl, json, math, subprocess, sys, time
from PIL import Image,ImageDraw,ImageFont,ImageFilter
R=Path(__file__).resolve().parent
W,H=1920,1080;FPS=24;DURATION=30
ctx=moderngl.create_standalone_context(backend='egl');ctx.enable(moderngl.DEPTH_TEST)
VS='''#version 330
in vec3 in_pos;in vec3 in_normal;in vec2 in_uv;in vec3 in_color;in vec3 in_emit;in float in_type;in float in_rough;
uniform mat4 mvp;uniform mat4 light_mvp;
out vec3 P;out vec3 N;out vec2 UV;out vec3 C;out vec3 E;out float T;out float rough;out vec4 LP;
void main(){P=in_pos;N=in_normal;UV=in_uv;C=in_color;E=in_emit;T=in_type;rough=in_rough;LP=light_mvp*vec4(in_pos,1);gl_Position=mvp*vec4(in_pos,1);}
'''
FS='''#version 330
in vec3 P;in vec3 N;in vec2 UV;in vec3 C;in vec3 E;in float T;in float rough;in vec4 LP;
uniform sampler2D shadow_map;uniform vec3 eye;uniform float clock;uniform float alpha;
out vec4 color;
float shadow(){vec3 q=LP.xyz/LP.w*.5+.5;float s=0.;float bias=.0010;
 for(int a=-1;a<=1;a++)for(int b=-1;b<=1;b++){float z=texture(shadow_map,q.xy+vec2(a,b)/2048.).r;s+=q.z-bias>z?.40:1.;}return s/9.;}
void main(){vec3 n=normalize(N);if(!gl_FrontFacing)n=-n;vec3 v=normalize(eye-P);
 vec3 base=C;vec3 emit=E;
 if(T>0.5&&T<2.5){float u=T<1.5?P.x:P.z;float w=T<1.5?P.z:P.x;float grain=sin(w*2.7+sin(u*.035)*1.9+sin(w*.17+u*.006)*3.2);float fine=sin(w*15.+sin(u*.021)*4.);base=vec3(.34,.20,.105)*(1.+.07*grain+.025*fine);}
 if(T>4.5&&T<5.5)base=vec3(.115,.123,.125);
 if(T>5.5&&T<6.5)base=vec3(.17,.177,.178);
 if(T>6.5&&T<7.5)base=vec3(.055,.047,.040);
 if(T>2.5&&T<3.5){vec2 u=UV;float arc=sin(u.x*3.4+u.y*1.8);float band=smoothstep(.12,.35,u.y-.24*sin(u.x*4.0+1.0));float band2=smoothstep(.30,.65,u.y+.25*sin(u.x*3.+2.));base=mix(vec3(.017,.048,.065),vec3(.060,.23,.24),band);base=mix(base,vec3(.56,.32,.14),band2*.65);base+=.018*sin(u.x*12.+u.y*4.);emit=base*.7;}
 base=pow(max(base,vec3(0.)),vec3(2.2));emit=pow(max(emit,vec3(0.)),vec3(2.2));
 vec3 l=normalize(vec3(260.,420.,380.)-P);float lam=max(dot(n,l),0.);float sh=alpha<.99?1.:shadow();
 float hemi=.27+.17*max(n.y,0.);vec3 rgb=base*(hemi+lam*sh*1.30*vec3(1.0,.86,.68));
 vec3 fill=normalize(vec3(-100.,180.,20.)-P);rgb+=base*max(dot(n,fill),0.)*.37*vec3(.66,.80,1.);
 vec3 halfv=normalize(v+l);float spec=pow(max(dot(n,halfv),0.),mix(90.,12.,rough));rgb+=spec*sh*.13*(1.-rough)*vec3(1.,.91,.77);
 rgb+=emit*.75;
 float ao=1.;if(T>4.5&&T<5.5){float wallAO=smoothstep(-3.,24.,min(P.x,P.z));ao=.78+.22*wallAO;}rgb*=ao;
 rgb=rgb/(rgb+vec3(.57));rgb=pow(rgb,vec3(1./2.2));
 color=vec4(rgb,alpha);}
'''
prog=ctx.program(vertex_shader=VS,fragment_shader=FS)
items=json.loads((R/'scene.json').read_text());records=[];casts=[];glass=[];chair=[];chaircasts=[]
GLASS=[0x9f/255,0xb4/255,0xc6/255]
for index,m in enumerate(items):
 if index in [153,156]:continue   # Y60 inner plates z-fight with the case body
 is_glass=m['opacity']<.5 and max(abs(m['color'][i]-GLASS[i]) for i in range(3))<.02
 if m['opacity']<.5 and not is_glass:continue
 p=np.asarray(m['positions'],dtype='f4').reshape(-1,3);n=np.asarray(m['normals'],dtype='f4').reshape(-1,3);uv=np.asarray(m['uv'],dtype='f4').reshape(-1,2) if m['uv'] else np.zeros((len(p),2),dtype='f4')
 name=m['name'];
 if name=='wall':
  if np.ptp(p[:,2])<.01:p[:,0]=(p[:,0]-150)*6+150
  else:p[:,2]=(p[:,2]-180)*6+180
  p[:,1]*=3
 ty={'walnut':1,'walnutB':2,'floor':5,'wall':6,'alex':7,'alexF':7}.get(name,0)
 if not name and max(m['emissive'])>.01 and len(p)>100:ty=3
 color=np.tile(m['color'],(len(p),1));emit=np.tile(m['emissive'],(len(p),1));other=np.tile([ty,m['roughness']],(len(p),1))
 rec=np.concatenate([p,n,uv,color,emit,other],axis=1).astype('f4')
 if is_glass:glass.append(rec);continue
 c=(p.min(0)+p.max(0))/2;is_chair=name in('chair','mesh') or (name=='black' and abs(c[0]-108)<45 and abs(c[2]-108)<45 and c[1]<140)
 (chair if is_chair else records).append(rec)
 if m['shadow']:(chaircasts if is_chair else casts).append(p)
def mkvao(recs):return ctx.vertex_array(prog,[(ctx.buffer(np.concatenate(recs).tobytes()),'3f 3f 2f 3f 3f 1f 1f','in_pos','in_normal','in_uv','in_color','in_emit','in_type','in_rough')])
vao=mkvao(records);chairvao=mkvao(chair);gvao=mkvao(glass) if glass else None
shadowprog=ctx.program(vertex_shader='''#version 330
in vec3 position;uniform mat4 mvp;void main(){gl_Position=mvp*vec4(position,1.);}''',fragment_shader='''#version 330
void main(){}''')
def mkshadowvao(cs):return ctx.vertex_array(shadowprog,[(ctx.buffer(np.concatenate(cs).astype('f4').tobytes()),'3f','position')])
def look(eye,target):
 e=np.array(eye,dtype=float);t=np.array(target,dtype=float);z=(e-t);z/=np.linalg.norm(z);x=np.cross([0,1,0],z);x/=np.linalg.norm(x);y=np.cross(z,x);m=np.eye(4);m[:3,:3]=[x,y,z];m[:3,3]=-m[:3,:3]@e;return m

def ortho(l,r,b,t,n,f):
 a=np.eye(4);a[0,0]=2/(r-l);a[1,1]=2/(t-b);a[2,2]=-2/(f-n);a[0,3]=-(r+l)/(r-l);a[1,3]=-(t+b)/(t-b);a[2,3]=-(f+n)/(f-n);return a

def perspective(fov,aspect,n=1.,f=1800.):
 a=np.zeros((4,4));q=1/math.tan(math.radians(fov)/2);a[0,0]=q/aspect;a[1,1]=q;a[2,2]=-(f+n)/(f-n);a[2,3]=-2*f*n/(f-n);a[3,2]=-1;return a
LM=ortho(-330,330,-340,340,50,1100)@look([380,540,460],[110,40,140]);shadowprog['mvp'].write(LM.astype('f4').T.tobytes())
def mkshadow(cs):
 sd=ctx.depth_texture((4096,4096));sd.compare_func='';sd.repeat_x=False;sd.repeat_y=False;sf=ctx.framebuffer(depth_attachment=sd);sf.use();sf.clear(depth=1);mkshadowvao(cs).render();return sd
sd=mkshadow(casts+chaircasts);sd_nochair=mkshadow(casts)   # the chair is rolled away for the structural shot
tex=ctx.texture((W,H),4);dep=ctx.depth_renderbuffer((W,H));resolved=ctx.framebuffer([tex],dep);fb=ctx.framebuffer([ctx.renderbuffer((W,H),components=4,samples=4)],ctx.depth_renderbuffer((W,H),samples=4))
prog['light_mvp'].write(LM.astype('f4').T.tobytes());prog['shadow_map']=0
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fonts={k:ImageFont.truetype(bold if k in [66,32,44] else font,k) for k in [20,22,26,32,44,66]}
def ease(x):return x*x*(3-2*x)
def lerp(a,b,t):return np.array(a)+(np.array(b)-np.array(a))*t

def orbit(target,theta,phi,radius):return np.array(target)+radius*np.array([math.sin(phi)*math.sin(theta),math.cos(phi),math.sin(phi)*math.cos(theta)])
def shot(t):
 if t<7.0:
  k=t/7.0;target=[114,65,153];eye=orbit(target,.86-.18*ease(k),1.04,560-22*k)
  return eye,target,42,'L—249','SCOTT HOWSON / DESK SETUP',0,7.0
 if t<12.0:
  k=(t-7.0)/5.0;return lerp([190,157,220],[180,148,193],ease(k)),[45,108,45],43,'A place for everything.','THREE SCREENS. ONE CORNER.',7.0,12.0
 if t<17.0:
  # low pass along the front of top B, looking under the edge at the steel: rails, fittings, legs, feet in their rings
  k=(t-12.0)/5.0;eye=lerp([85,45,250],[92,44,150],ease(k));target=lerp([50,74,60],[50,75,55],ease(k))
  return eye,target,50,'Steel under the walnut.','TWO ANGLE RAILS. ONE BOLTED CORNER. NOTHING SAGS.',12.0,17.0
 if t<22.0:
  k=(t-17.0)/5.0;return lerp([262,120,172],[235,112,184],ease(k)),lerp([191,85,46],[177,86,43],k),42,'Walnut. Steel. Detail.','CUSTOM GEOMETRY / CLEAN FINISHES',17.0,22.0
 if t<27.0:
  k=(t-22.0)/5.0;target=[116,67,151];eye=orbit(target,.64+.12*ease(k),.94,540+12*k)
  return eye,target,42,'YOUR CORNER. REIMAGINED.','github.com/scotthowson/desk-setup',22.0,27.0
 k=(t-27.0)/3.0;target=[116,67,151];eye=orbit(target,.76+.03*k,.94,552)
 return eye,target,42,'','',27.0,30.0

def frame(t,overlay=True):
 eye,target,fov,title,sub,start,end=shot(t);fb.use();fb.clear(.055,.06,.064,1,depth=1);prog['mvp'].write((perspective(fov,W/H)@look(eye,target)).astype('f4').T.tobytes());prog['eye']=tuple(eye);prog['alpha']=1.0;nochair=12.0<=t<17.0;(sd_nochair if nochair else sd).use(0);vao.render()
 if not nochair:chairvao.render()
 if gvao is not None:
  ctx.enable(moderngl.BLEND);ctx.blend_func=moderngl.SRC_ALPHA,moderngl.ONE_MINUS_SRC_ALPHA;ctx.depth_mask=False;prog['alpha']=.2;gvao.render();ctx.depth_mask=True;ctx.disable(moderngl.BLEND)
 ctx.copy_framebuffer(resolved,fb)
 im=Image.frombytes('RGBA',(W,H),resolved.read(components=4)).transpose(Image.Transpose.FLIP_TOP_BOTTOM).convert('RGB')
 # quiet cinematic treatment: shaded lower edge, fine letterbox framing and restrained type
 arr=np.asarray(im).astype('f4');yy=np.linspace(0,1,H)[:,None];shade=np.clip((yy-.58)/.42,0,1)*.64;arr*=1-shade[:,:,None];im=Image.fromarray(np.uint8(arr.clip(0,255)))
 if overlay and t<27.0:
  layer=Image.new('RGBA',(W,H));dr=ImageDraw.Draw(layer);a=min(1,max(0,(t-start-.20)/.7),max(0,(end-t-.18)/.5));alpha=int(a*255)
  dr.line((86,898,132,898),fill=(201,159,102,alpha),width=2)
  dr.text((86,920),title,font=fonts[66] if start==0 else fonts[32],fill=(241,237,228,alpha))
  dr.text((88,1004),sub,font=fonts[22],fill=(188,186,177,alpha))
  dr.text((W-228,58),'HOWSON',font=fonts[22],fill=(230,226,215,170))
  im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
 if t>=27.0:
  # end card over the dimmed last orbit
  k=min(1,(t-27.0)/.8);im=Image.blend(im,Image.new('RGB',(W,H),(11,13,14)),.78*k);layer=Image.new('RGBA',(W,H));dr=ImageDraw.Draw(layer);alpha=int(255*min(1,max(0,(t-27.3)/.7)))
  dr.line((W//2-28,398,W//2+28,398),fill=(201,159,102,alpha),width=2)
  dr.text((W//2,470),'L—249',font=fonts[66],fill=(241,237,228,alpha),anchor='mm')
  dr.text((W//2,548),'A corner desk you can build from the manual.',font=fonts[26],fill=(205,202,193,alpha),anchor='mm')
  dr.text((W//2,612),'github.com/scotthowson/desk-setup',font=fonts[26],fill=(201,159,102,alpha),anchor='mm')
  dr.text((W//2,664),'Manual · 1:1 templates · checklist · v1.0-assembly-ready',font=fonts[22],fill=(160,158,150,alpha),anchor='mm')
  im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
 # fades hide cuts while preserving calm continuous movement inside each shot
 fade=min(1,t/.65,(30-t)/1.2)
 for cut in [7.0,12.0,17.0,22.0]:fade=min(fade,.15+.85*min(1,abs(t-cut)/.18))
 if fade<1:im=Image.blend(Image.new('RGB',(W,H),(11,13,14)),im,max(0,fade))
 return im
if '--preview' in sys.argv:
 for t in [2,9,14.5,19,24,28.5]:frame(t).save(R/f'preview-{t}.jpg',quality=94)
 print('Preview frames ready',flush=True)
else:
 out=R/'desk-showcase-silent.mp4';cmd=['ffmpeg','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=open(R/'encode.log','w'));tick=time.time()
 for i in range(DURATION*FPS):
  proc.stdin.write(frame(i/FPS).tobytes())
  if i%48==0:print(f'{i}/{DURATION*FPS} frames / {time.time()-tick:.1f}s',flush=True)
 proc.stdin.close();assert proc.wait()==0;print('Rendered',out,flush=True)
