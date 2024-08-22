from AashikaMusic.core.bot import Aashika
from AashikaMusic.core.dir import dirr
from AashikaMusic.core.git import git
from AashikaMusic.core.userbot import Userbot
from AashikaMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Aashika()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
