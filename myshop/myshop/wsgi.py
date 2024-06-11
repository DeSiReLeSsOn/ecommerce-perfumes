import os
import sys
from pathlib import Path



project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

from django.core.wsgi import get_wsgi_application



application = get_wsgi_application()