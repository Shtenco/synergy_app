const API=process.env.EXPO_PUBLIC_API_URL || 'http://127.0.0.1:8000/v1';
let token='';
export function setToken(v:string){token=v}
export async function api<T>(path:string,init:RequestInit={}):Promise<T>{const headers:any={'Content-Type':'application/json',...(init.headers||{})}; if(token) headers.Authorization=`Bearer ${token}`; const r=await fetch(API+path,{...init,headers}); if(!r.ok) throw new Error((await r.text())||`HTTP ${r.status}`); return r.json()}
export const endpoints={dashboard:()=>api<any>('/dashboard'),content:()=>api<any[]>('/content'),calendar:()=>api<any[]>('/calendar'),inbox:()=>api<any[]>('/inbox'),leads:()=>api<any[]>('/leads'),brands:()=>api<any[]>('/brands')};
