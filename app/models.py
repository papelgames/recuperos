
import datetime
from types import ClassMethodDescriptorType
from typing import Text

from slugify import slugify
from sqlalchemy import Column
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


from app import db

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(),\
                     onupdate=db.func.current_timestamp())

class Post(Base):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text)
    #created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image_name = db.Column(db.String)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan',
                               order_by='asc(Comment.created)')

    def __repr__(self):
        return f'<Post {self.title}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                db.session.rollback()
                db.session.add(self)
                count += 1
                self.title_slug = f'{slugify(self.title)}-{count}'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(title_slug=slug).first()

    @staticmethod
    def get_by_id(id):
        return Post.query.get(id)

    @staticmethod
    def get_all():
        return Post.query.all()

    @staticmethod
    def all_paginated(page=1, per_page=20):
        return Post.query.order_by(Post.created.asc()). \
            paginate(page=page, per_page=per_page, error_out=False)


class Comment(Base):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user_name = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text)
    #created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, content, user_id=None, user_name=user_name, post_id=None):
        self.content = content
        self.user_id = user_id
        self.user_name = user_name
        self.post_id = post_id

    def __repr__(self):
        return f'<Comment {self.content}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_post_id(post_id):
        return Comment.query.filter_by(post_id=post_id).all()

class Ofrecimientos (Base):
    __tablename__ = "ofrecimientos"
    correo_electronico = db.Column(db.String(256)) #hacerlo obligatorio
    nombre_apellido_rs = db.Column(db.String(256)) #hacerlo obligatorio
    dni = db.Column(db.Integer) #hacerlo obligatorio
    importe_ofertado = db.Column(db.String(128))
    compulsa_id = db.Column(db.Integer, db.ForeignKey('compulsas.id'), nullable=False)
    fecha_confirmacion = db.Column(db.DateTime)
    fecha_envio = db.Column(db.DateTime)
    fecha_reenvio = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    pin = db.Column(db.String(128))
    

    def set_pin(self, pin):
        self.pin = generate_password_hash(pin)

    def check_pin(self, pin):
        return check_password_hash(self.pin, pin)

    def save(self):
        if not self.id:
            db.session.add(self)
            print ("paso1")
        db.session.commit()
        
    
    @staticmethod
    def get_ofrecimientos_id(ofrecimiento_id):
        return Ofrecimientos.query.filter_by(id=ofrecimiento_id).first()

class Compulsas (Base):
    __tablename__ = "compulsas"
    bien = db.Column(db.String(256), nullable = False)
    fecha_inicio = db.Column(db.DateTime, nullable = False)
    fecha_vencimiento = db.Column(db.DateTime, nullable = False)
    siniestro = db.Column(db.Integer, nullable = False)
    patente = db.Column(db.String(7), nullable = False)
    usuario_creador = db.Column(db.Integer)
    usuario_aprobador = db.Column(db.Integer)
    ubicacion = db.Column(db.String(150), nullable = False)
    condiciones_generales = db.Column(db.Text, nullable = False)
    importe_base = db.Column(db.Integer, nullable = False)
    para_empleados = db.Column(db.Boolean, default=False)
    tipo_bien_id = db.Column(db.Integer, db.ForeignKey('tipobienes.id'), nullable=False)
    status = db.Column(db.String(20))
    ofrecimiento = db.relationship('Ofrecimientos', backref='compulsa', lazy=True, cascade='all, delete-orphan',
                               order_by='asc(Ofrecimientos.created)')
    imagenes = db.relationship('Imagenes', backref='imagen_br', lazy=True,cascade='all, delete-orphan',
                               order_by='asc(Imagenes.created)')
    

    @staticmethod
    def get_all():
        return db.session.query(Compulsas, TipoBienes).filter(Compulsas.tipo_bien_id == TipoBienes.id).all()
        #return db.session.query(Compulsas, TipoBienes).all()
    
    @staticmethod
    def get_by_compulsa_id(compulsa_id):
        return db.session.query(Compulsas, TipoBienes). \
            filter(Compulsas.tipo_bien_id == TipoBienes.id). \
            filter(Compulsas.id == compulsa_id).all()
            #filter(Compulsas.id == Imagenes.compulsa_id). \
    
    @staticmethod
    def get_by_ofrecimiento_id(ofrecimiento_id):
        return db.session.query(Compulsas, TipoBienes, Ofrecimientos). \
            filter(Compulsas.tipo_bien_id == TipoBienes.id). \
            filter(Compulsas.id == Ofrecimientos.compulsa_id). \
            filter(Ofrecimientos.id == ofrecimiento_id).filter()


    @staticmethod
    def get_activas():
        return db.session.query(Compulsas, TipoBienes). \
            filter(Compulsas.tipo_bien_id == TipoBienes.id). \
            filter(Compulsas.fecha_inicio <= datetime.datetime.now() ,Compulsas.fecha_vencimiento >= datetime.datetime.now() ).all()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Imagenes(Base):
    __tablename__ = "imagenes"
    imagen = db.Column(db.String(256), nullable = False)
    compulsa_id = db.Column(db.Integer, db.ForeignKey('compulsas.id'), nullable=False)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
   
    @staticmethod
    def get_by_imagenes_compulsa_id(compulsa_id):
        return Imagenes.query. \
            filter(Imagenes.compulsa_id == compulsa_id).all()

class TipoBienes(Base):
    __tablename__ = "tipobienes"
    tipo_bien = db.Column(db.String(50), nullable = False)
    es_restos = db.Column(db.Boolean, default=False)
    es_vehiculo = db.Column(db.Boolean, default=False)
    compulsa = db.relationship('Compulsas', backref='compulsa_br', lazy=True)

    @staticmethod
    def get_all():
        return TipoBienes.query.all()
        #return db.session.query(TipoBienes,Compulsas).filter(TipoBienes.id == Compulsas.tipo_bien_id).all()
'''
Session.query(User,Document,DocumentPermissions)
    .filter(User.email == Document.author)
    .filter(Document.name == DocumentPermissions.document)
    .filter(User.email == 'someemail')
    .all()
'''
class CorreosElectronicos (Base):
    __tablename__ = "correoselectronicos"
    correo = db.Column(db.String(256), unique=True, nullable=False)
    nombre = db.Column(db.String(256), nullable=False)
    empleado = db.Column(db.Boolean, default=False)
    desarmadero = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=False)
    fecha_baja = db.Column(db.DateTime)
    quien_baja = db.Column(db.String(256))

class Recuperos (Base):
    __tablename__ = "recuperos"
    rama = db.Column(db.Integer)
    siniestro = db.Column(db.Integer)
    fe_ocurrencia = db.Column(db.DateTime)
    fe_denuncia = db.Column(db.DateTime)
    fe_pago = db.Column(db.DateTime)
    fe_aviso_aparicion = db.Column(db.DateTime)
    fe_ingreso_deposito = db.Column(db.DateTime)
    importe_pagado = db.Column(db.Float())
    vehiculo = db.Column(db.String(75))
    compania = db.Column(db.Integer) #tabla companias
    comprador = db.Column(db.Integer) #tabla comprador
    estado = db.Column(db.Integer()) #tabla estados <parametro tabla recuperos>
    desc_siniestro = db.Column(db.Text())
    tercero = db.Column(db.String(50))
    tel_tercero = db.Column(db.String(50))
    mail_tercero = db.Column(db.String(50))
    asegurado = db.Column(db.String(50))
    poliza = db.Column(db.Integer)
    monto_franquicia = db.Column(db.Float)
    responsabilidad = db.Column(db.Integer()) #tabla respondabilidades
    analista_siniestro = db.Column(db.String(4)) #alfanumerico de GLM 
    modulo = db.Column(db.String(50))
    usuario_responsable = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    tareas_pendientes = db.relationship ("TareasPendientes")
    cobros = db.relationship ("Cobros")
    observacion = db.relationship("Observaciones")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()


class Acciones (Base):
    __tablename__ = "acciones"
    descripcion = db.Column(db.String(50), nullable=False)
    estado_recupero = db.Column(db.Integer)
    envia_correo = db.Column(db.String(2))
    destinatario_correo = db.Column(db.String(2))
    id_tarea_siguiente = db.Column(db.Integer)
    programa = db.Column(db.String(50))
    finaliza = db.Column(db.Boolean, default=False)
    tareas = db.relationship("Tareas", secondary = "tareasacciones", backref = "ta", lazy="dynamic")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Acciones.query.get(id)
    
    @staticmethod
    def get_all():
        return Acciones.query.all()

class Tareas (Base):
    __tablename__ = "tareas"
    descripcion = db.Column(db.String(50), nullable=False)
    vencimiento = db.Column(db.Integer, nullable=False)
    modulo_inicial = db.Column(db.String(50))
    acciones = db.relationship("Acciones", secondary="tareasacciones", backref="ta", lazy= "dynamic")
    tareas_pendientes = db.relationship ("TareasPendientes")
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id):
        return Tareas.query.get(id)
    
    @staticmethod
    def get_by_modulo_inicial(modulo):
        return Tareas.query.filter_by(modulo_inicial=modulo).first()
    

    @staticmethod
    def get_all():
        return Tareas.query.all()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class TareasAcciones (Base):
    __tablename__ = "tareasacciones"
    id_tarea = db.Column(db.Integer, db.ForeignKey("tareas.id"))
    id_accion = db.Column(db.Integer, db.ForeignKey("acciones.id"))

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class TareasPendientes (Base):
    __tablename__ = "tareaspendientes"
    id_tarea = db.Column(db.Integer, db.ForeignKey("tareas.id"), nullable=False)
    id_recupero = db.Column(db.Integer, db.ForeignKey("recuperos.id"), nullable=False)
    fe_vencimiento = db.Column(db.DateTime, nullable = False)
    fe_fin = db.Column(db.DateTime)
    observacion = db.relationship("Observaciones")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Cobros (Base):
    __tablename__ = "cobros"
    pagador = db.Column(db.String(50), nullable = False)
    factura_nacion = db.Column(db.String(13))
    cantidad_cuotas = db.Column(db.Integer)
    importe_total = db.Column(db.Float)
    id_recupero = db.Column(db.Integer, db.ForeignKey("recuperos.id"), nullable=False)
    importes_cobros = db.relationship("ImportesCobros")
    observacion = db.relationship("Observaciones")

class ImportesCobros (Base):
    __tablename__ = "importescobros"    
    estado_cobro = db.Column(db.Integer)
    fe_probable_cobro = db.Column(db.DateTime)
    fe_cobro = db.Column(db.DateTime)
    cuenta_bancaria = db.Column(db.String(50))
    numero_cuota = db.Column(db.Integer)
    importe_cuota = db.Column(db.Float)
    id_cobro = db.Column(db.Integer, db.ForeignKey("cobros.id"),  nullable = False)
    
class Observaciones (Base):
    __tablename__ = "observaciones"
    titulo = db.Column(db.String(50))
    observacion = db.Column(db.Text)
    id_recupero = db.Column(db.Integer, db.ForeignKey("recuperos.id"))
    id_cobros = db.Column(db.Integer, db.ForeignKey("cobros.id"))
    id_tarea_pendiente = db.Column(db.Integer, db.ForeignKey("tareaspendientes.id"))
    id_user = db.Column(db.Integer, nullable = False)

class Estados (Base):
    __tablename__ = "estados"
    desc_estado = db.Column(db.String(15), nullable = False)
    estado_tabla = db.Column(db.String(30), nullable = False)
    sub_codigo = db.Column(db.String(2), unique=True)

    @staticmethod
    def get_by_estado_tabla(tabla):
        return Estados.query.filter_by(estado_tabla=tabla).all()
    
    @staticmethod
    def get_all():
        return Estados.query.all()