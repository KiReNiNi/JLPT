function artifactMock(){
 const copy=v=>v===undefined?undefined:JSON.parse(JSON.stringify(v));let cache=new Map(),listeners=[];
 const docSnapshot=path=>({exists:cache.has(path),id:path.split('/').at(-1),data:()=>copy(cache.get(path))});
 const collectionSnapshot=name=>({docs:[...cache.keys()].filter(p=>p.startsWith(name+'/')).map(docSnapshot),metadata:{fromCache:false}});
 const emit=()=>{for(const l of listeners)l.fn(l.kind==='doc'?docSnapshot(l.path):collectionSnapshot(l.path))};
 async function write(op){const result=await window.__qaSave(op);cache=new Map(result.docs);emit();return result.id?{id:result.id}:undefined}
 const db={doc:path=>({set:v=>write({type:'set',path,value:v}),delete:()=>write({type:'delete',path}),get:async()=>docSnapshot(path),onSnapshot:fn=>{listeners.push({kind:'doc',path,fn});queueMicrotask(()=>fn(docSnapshot(path)));return()=>{}}}),collection:name=>({add:v=>write({type:'add',path:name,value:v}),onSnapshot:fn=>{listeners.push({kind:'collection',path:name,fn});queueMicrotask(()=>fn(collectionSnapshot(name)));return()=>{}}})};
 window.claude={use:async name=>{if(name!=='db')throw Error('Unexpected service');cache=new Map(await window.__qaLoad());return db}};
 window.__qaRngReads=0;const random=Math.random;Math.random=()=>{window.__qaRngReads++;return random()};
 try{localStorage.setItem('n1skin',JSON.stringify({skin:'orchard',bg:'2'}))}catch{}
}

module.exports=artifactMock;
