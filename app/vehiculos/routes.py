import logging
import os

from flask import render_template, redirect, url_for, abort, current_app
from flask.helpers import flash
from flask_login import login_required, current_user
from rsa.key import PrivateKey
from werkzeug.utils import secure_filename

from app.auth.decorators import admin_required
from app.auth.models import User
from app.models import Compulsas, Imagenes, Ofrecimientos, Recuperos, TareasPendientes, Tareas
from . import vehiculos_bp
from .forms import AltaVehiculosForm

from app.common.mail import send_email

from datetime import datetime, time, timedelta

logger = logging.getLogger(__name__)


@vehiculos_bp.route("/vehiculos/alta", methods = ['GET', 'POST'])
@login_required
def alta():
    form = AltaVehiculosForm()
    tarea_inicial = Tareas.get_by_modulo_inicial('vehiculos')

    if form.validate_on_submit():
        vehiculo = form.vehiculo.data
        rama = form.rama.data
        siniestro = form.siniestro.data
        fe_ocurrencia = form.fe_ocurrencia.data
        fe_pago = form.fe_pago.data
        fe_aviso_aparicion = form.fe_aviso_aparicion.data
        importe_pagado = form.importe_pagado.data
        asegurado = form.asegurado.data
        
        alta = Recuperos(vehiculo=vehiculo,
                         rama = rama,
                         siniestro=siniestro,
                         fe_ocurrencia=fe_ocurrencia,
                         fe_pago=fe_pago,
                         fe_aviso_aparicion=fe_aviso_aparicion,
                         importe_pagado=importe_pagado,
                         asegurado=asegurado, 
                         modulo = 'vehiculo'
                         )
        alta.save()
        tareaInicial = TareasPendientes (id_tarea =tarea_inicial.id,
                                         id_recupero = alta.id,
                                         fe_vencimiento = datetime.now() + timedelta(tarea_inicial.vencimiento)
                                         )
        
        tareaInicial.save() 

        flash ("Se ha guardado correctamente", "alert-success")
        return redirect(url_for("vehiculos.alta"))
         
    return render_template("vehiculos/alta.html", form = form)
