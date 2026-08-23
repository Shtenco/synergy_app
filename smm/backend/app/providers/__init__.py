from .vk import VKProvider
from .meta import MetaProvider
from .instagram import InstagramProvider
from .telegram import TelegramProvider
from .whatsapp import WhatsAppProvider
PROVIDERS={"vk":VKProvider(),"meta":MetaProvider(),"facebook":MetaProvider(),"instagram":InstagramProvider(),"telegram":TelegramProvider(),"whatsapp":WhatsAppProvider()}
