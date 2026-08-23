export type SocialNetwork = 'vk'|'telegram'|'instagram'|'facebook'|'whatsapp'|'ok'|'zen';
export type PublishStatus = 'draft'|'review'|'scheduled'|'publishing'|'published'|'failed';
export interface Brand { id:string; name:string; toneOfVoice:string; }
export interface ContentItem { id:string; brandId:string; title:string; body:string; channels:SocialNetwork[]; status:PublishStatus; }
