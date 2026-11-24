"""Metadatos mínimos para identificar la sala pedida; no consulta stock/recetas."""
import os
from pathlib import Path
import sys
import json

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
os.environ['CLINITENS_READ_ENV']='0'
os.environ['DJANGO_SETTINGS_MODULE']='core.local_runtime'
import django
django.setup()
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from FarmaTEFApp.models import Medicamento, SalaFarmacia, UbicacionMedicamento
from core.permissions import es_docente_de_area
from UsuarioApp.models import AreaDocente

ids=set(Medicamento.objects.order_by().values_list('creado_por_id',flat=True).distinct())
ids.update(SalaFarmacia.objects.values_list('propietario_id',flat=True))
rows=[]
for owner in get_user_model().objects.filter(pk__in=ids,is_active=True).select_related('profile__position_FK'):
    if not es_docente_de_area(owner,AreaDocente.FARMACIA):
        continue
    sala=SalaFarmacia.objects.filter(propietario=owner).first()
    rows.append({'propietario_id':owner.pk,'usuario':owner.username,'sala_id':sala.pk if sala else None,
                 'version':sala.version if sala else 0,'muebles':sala.muebles.count() if sala else 0,
                 'ubicaciones':UbicacionMedicamento.objects.filter(mueble__sala=sala).count() if sala else 0})
print(json.dumps(rows,ensure_ascii=False))
