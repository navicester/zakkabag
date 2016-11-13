from .base import *

heroku = False
mysql = True
sae = False


if 'SERVER_SOFTWARE' in os.environ: 
	from .sae import *
elif sae:
	from .sae import *
elif mysql:
	from .mysql import *	
elif heroku:
	from .production import *	
else:
	pass