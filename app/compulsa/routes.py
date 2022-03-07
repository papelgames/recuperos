import logging
from operator import setitem
import os
from datetime import date, datetime

from flask import render_template, redirect, url_for, abort, current_app, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.auth.decorators import admin_required
from app.auth.models import User
from app.models import Compulsas, Imagenes, TipoBienes
from . import compulsa_bp
from .forms import AltaCompulsaForm, ImagenesBienesForm

logger = logging.getLogger(__name__)

def tipo_bien_select():
    tipo_bienes = TipoBienes.get_all()
    select_tipo_bien =[( '','Seleccionar tipo de bien')]
    for rs in tipo_bienes:
        sub_select_tipo_bien = (str(rs.id), rs.tipo_bien)
        select_tipo_bien.append(sub_select_tipo_bien)
    return select_tipo_bien


@compulsa_bp.route("/compulsas/")
@login_required
#@admin_required
def index():
    return render_template("compulsa/index.html")

@compulsa_bp.route("/compulsas/alta", methods = ['GET', 'POST'])
@login_required
#@admin_required
def compulsas_alta():
    form = AltaCompulsaForm()

    form.tipo_bien.choices = tipo_bien_select()

    if form.validate_on_submit():
        bien = form.bien.data
        siniestro = form.siniestro.data
        patente = form.patente.data
        fecha_inicio = form.fecha_inicio.data 
        fecha_vencimiento = form.fecha_vencimiento.data
        ubicacion = form.ubicacion.data
        condiciones_generales = form.condiciones_generales.data
        importe_base = form.importe_base.data
        para_empleados = form.para_empleados.data
        tipo_bien_id = form.tipo_bien.data
        usuario_creador = current_user.id
        status = "alta"
        
        compulsa = Compulsas(bien = bien, 
                             siniestro = siniestro,
                             patente = patente,
                             fecha_inicio = fecha_inicio,
                             fecha_vencimiento = fecha_vencimiento,
                             ubicacion = ubicacion,
                             condiciones_generales= condiciones_generales,
                             importe_base= importe_base,
                             para_empleados = para_empleados,
                             tipo_bien_id = tipo_bien_id,
                             usuario_creador = usuario_creador,
                             status= status
                             )
        
        compulsa.save()
        logger.info(f'Guardando nuevo post {bien}')
        flash("Se han guardado los cambios correctamente", "alert-success")
        return redirect(url_for("compulsa.imagenes_de_bienes", id_compulsa = compulsa.id))

    return render_template("compulsa/abm_compulsa.html", form = form)

@compulsa_bp.route("/compulsas/imagenes/<int:id_compulsa>", methods = ['GET','POST'])
@login_required
#@admin_required
def imagenes_de_bienes(id_compulsa):
    form = ImagenesBienesForm()

    if form.validate_on_submit():
        imagen = form.imagenes_bienes.data
        if imagen:
            image_name = secure_filename(imagen.filename)
            images_dir = current_app.config['POSTS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            imagen.save(file_path)
        
            imagenes = Imagenes(imagen = image_name,
                                compulsa_id = id_compulsa)
            imagenes.save()

    return render_template("compulsa/imagenes_bienes.html", form = form)

@compulsa_bp.route("/compulsas/modificacion")
@login_required
#@admin_required
def compulsas_modificacion():
    return render_template("compulsa/abm_compulsa.html")

@compulsa_bp.route("/compulsas/activas")
#@login_required
#@admin_required
def activas():
    hoy = datetime.now()
    #compulsas_activas = Compulsas.query.filter(Compulsas.fecha_inicio <= hoy,Compulsas.fecha_vencimiento >= hoy ).all()
    compulsas_activas = Compulsas.get_activas()
    
    
    return render_template("compulsa/listado_activas.html", compulsas_activas = compulsas_activas)

@compulsa_bp.route("/compulsas/historicas")
@login_required
#@admin_required
def historicas():
    compulsas_historicas = Compulsas.get_all()
    for i in compulsas_historicas:
        print(i.TipoBienes.tipo_bien)
    return render_template("compulsa/listado.html", compulsas_historicas = compulsas_historicas)