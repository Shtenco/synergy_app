from dataclasses import dataclass
@dataclass
class Workspace: id:str; name:str
@dataclass
class Brand: id:str; workspace_id:str; name:str; tone_of_voice:str=""
@dataclass
class SocialAccount: id:str; brand_id:str; network:str; external_id:str
@dataclass
class ContentItem: id:str; brand_id:str; title:str; body:str; status:str="draft"
@dataclass
class Lead: id:str; workspace_id:str; source:str; stage:str="new"; score:int=0
