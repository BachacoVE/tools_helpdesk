# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
# Generated by the OpenERP plugin for Dia !

from openerp.osv import fields, osv
from openerp import api, fields, models
from datetime import date, datetime, timedelta
import smtplib
import re
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError

class tools_helpdesk_incidencia(models.Model):
    _name = 'tools.helpdesk.incidencia'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'codigo'
    _description = 'Incidencia'
    
    
    codigo = fields.Char('Código', size=10, help="Código de la Incidencia")
    solicitante_id = fields.Many2one('res.users', string="Solicitante", help='Nombre Completo del Solicitante de la Incidencia',states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    res_partner_id = fields.Many2one(related='solicitante_id.res_partner_id', string='Organización')
    contexto_nivel1_id = fields.Many2one('tools.helpdesk.contexto_nivel1','Aplicación',states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    contexto_nivel2_id = fields.Many2one('tools.helpdesk.contexto_nivel2','Módulo',states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    contexto_nivel3_id = fields.Many2one('tools.helpdesk.contexto_nivel3','Operación',states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    categoria_incidencia_id = fields.Many2one('tools.helpdesk.categoria_incidencia', string="Categoría de Incidencia",states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    tipo_incidencia_id = fields.Many2one('tools.helpdesk.tipo_incidencia', 'Tipo de Incidencia',states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    state = fields.Selection([('registrado','Registrado'),('recibido','Recibido'),('asignado','Asignado'),('proceso','En Proceso'),('atendido','Atendido'),('resuelto','Resuelto'),('anulado','Anulado')], "Status")
    observacion_ids = fields.One2many('tools.helpdesk.observacion', 'incidencia_id', string="Observaciones", help='Observaciones de una incidencia',states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    autorizado = fields.Char('Autorizado por:', size=30, help='Colocar el Nombre y Apellido del autorizante')
    asignacion = fields.Many2one('res.users', 'Asignado a:',states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    denominacion = fields.Char('Descripción Corta', size=90,states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    prioridad = fields.Selection([('0','Ninguna'),('1','Baja'), ('2', 'Media'),('3','Urgente')],'Prioridad', default='0',states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    fecha_actual = fields.Datetime('Fecha de la solicitud',  help='Fecha cuando se reporto la incidencia', default=datetime.today())
    #memo = fields.Boolean('Memo')
    #correo = fields.Boolean('Correo Electrónico')
    #llamada = fields.Boolean('Llamada Telefonica')
    #presencial = fields.Boolean('Presencial')
    #gestion = fields.Boolean('Gestion Documental')
    #n_memo = fields.Char('Número de Memo')
    #Para adjuntar los documentos a enviar.
    adjunto_ids = fields.One2many('tools.helpdesk.adjuntos', 'incidencia_id', string ="Adjuntos", help='Documentos adicionales, Respaldos Fisicos',states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    #Fin del adjunto
    descripcion = fields.Text('Descripción',states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    procedimiento = fields.Text('Procedimiento en la Solución',states={'anulado':[('readonly',True)],'resuelto':[('readonly',True)]})
    fecha_creacion = fields.Datetime('Fecha de Creación', default=0)
    fecha_recibido = fields.Datetime('Fecha de Recibido')
    fecha_asignado_a = fields.Datetime('Fecha Asignado a')
    fecha_proceso = fields.Datetime('Fecha Proceso')
    fecha_atendido = fields.Datetime('Fecha Atendido')
    fecha_solucion = fields.Datetime('Fecha Resuelto')
    # dia_creacion = fields.Char('Días de Creado')
    dia_recibido = fields.Char('Días Intervalo Creado a Recibido')
    dia_asignado_a = fields.Char('Días Intervalo Recibido a Asignado')
    dia_proceso = fields.Char('Días Intervalo Asignado a Proceso')
    dia_atendido = fields.Char('Días Intervalo Proceso a Atendido')
    dia_solucion = fields.Char('Días Intervalo Atendido a Resuelto')
    # retraso = fields.Integer('Dias Transcurridos', help="Conteo de dias a partir de la fecha de entrega", readonly="True", compute="_compute_calculo_dias", store="False")
    retraso = fields.Integer('Dias Transcurridos hasta Atendido', help="Conteo de dias a partir de la fecha de creación hasta la atención de la Incidencia", readonly=True, compute="_compute_calculo_dias", store=False)
    transcurrido_resuelto = fields.Integer('Dias Transcurridos hasta Resuelto',
        help="Conteo de dias a partir de la fecha de creación hasta la la confirmación de Resuelto por parte del Cliente",
        readonly=True, compute="_compute_calculo_dias_resuelto", store=False)


    _defaults = {
        'solicitante_id': lambda self, cr, uid, ctx=None: uid
    }


    #@api.onchange('solicitante_id')
    #def actualizar_organizacion_solicitante(self):
    #    self.res_partner_id = self.solicitante_id.res_partner_id.id

    #def onchange_solicitante(self, cr, uid, ids):
    #    return {'value':{'solicitante_id': uid}}

    _order='codigo desc'  #PARA ORDENAR POR CODICO DE MAYOR A MENOR

    def create(self, cr, uid, vals, context=None):
        #vals['solicitante_id'] = uid
        vals.update({'codigo':self.pool.get('ir.sequence').get(cr, uid, 'tools.helpdesk.incidencia')}) 
        vals.update({'fecha_creacion':datetime.today()})
        new_id = super(tools_helpdesk_incidencia, self).create(cr, uid, vals, context=None)
        return new_id
    
    # Accion para Botones en el proceso Workflow

    def enviar_mensaje_status(self):
        """Método utilizado para definir el mensaje junto al status
        que se enviará en el mensaje dentro de openchatter"""
        message = "El estatus ha sido cambiado a <strong><em>%s</em></strong>" % self.state
        self.message_post(body=message,type='email', subtype='mail.mt_comment')

    @api.one
    def action_registrado(self):
        self.state='registrado'
        self.message_subscribe_users(user_ids=[1,self.solicitante_id.id])

    @api.one
    def action_recibido(self):
        self.fecha_recibido=datetime.today()
        diferencia=self.calcular_dias(self.fecha_creacion, self.fecha_recibido)
        self.dia_recibido=diferencia.days
        self.state='recibido'
        self.enviar_mensaje_status()
        

    @api.one
    def action_asignado(self):
        if not self.asignacion:
            raise osv.except_osv(('Error'),('Debes llenar el campo: asignado a'))
        self.fecha_asignado_a=datetime.today()
        diferencia=self.calcular_dias(self.fecha_recibido, self.fecha_asignado_a)
        self.dia_asignado_a=diferencia.days
        self.state='asignado'
        self.enviar_mensaje_status()
        self.message_subscribe_users(user_ids=[self.asignacion.id])


    # PARA ENVIAR E-MAIL            
        cuerpo_mensaje = """Se le ha asignado una Ticket en Help Desk:<br>
        Codigo: %s,<br>
        Asunto: %s,<br>
        Descripcion: %s,<br> """ % (self.codigo, self.denominacion, self.descripcion)
        const_mail = {'email_from' : self.solicitante_id.email,
                      'email_to' : self.asignacion.login,
                      #'partner_ids' : [(0,0,{'res_partner_id':self.asignacion.partner_id, 'mail_message_id': ids_mail})],
                      'subject' : "Re: %s" % self.codigo,
                      'body_html' : cuerpo_mensaje}
        ids_mail = self.env['mail.mail'].create(const_mail).send()
        return True 
    # FIN DE EMAIL

    @api.one
    def action_proceso(self):
        self.fecha_proceso=datetime.today()
        diferencia=self.calcular_dias(self.fecha_asignado_a, self.fecha_proceso)
        self.dia_proceso=diferencia.days
        self.state='proceso'
        self.enviar_mensaje_status()

    @api.one
    def action_atendido(self):
        self.fecha_atendido=datetime.today()
        diferencia=self.calcular_dias(self.fecha_proceso, self.fecha_atendido)
        self.dia_atendido=diferencia.days
        self.state='atendido'
        self.enviar_mensaje_status()



        # PARA ENVIAR E-MAIL AL SOLICITANTE           
        cuerpo_mensaje = """

        Estimado usuario,<br>
        Le informamos que su REQUERIMIENTO DE SOPORTE, bajo el ticket No. <strong>%s</strong>,<br>
        ha sido procesado satisfactoriamente, por el Departamento de HELPDESK.<br>
        Su estatus actual es: <strong>ATENDIDO</strong><br>
        El asunto de su Ticket es: <em>%s</em><br>
        La Descripcion de su Ticket es: <em>%s</em><br>
        <br>
        Por favor, confirme que fue solucionado su requerimiento cambiando el estatus a RESUELTO<br>
        Puede seguir su ticket a traves de la direccion http://ovniticket.ovnicom.com:8069<br>
        """ % (self.codigo, self.denominacion, self.descripcion)

        const_mail = {'email_from' : self.asignacion.login,
                      'email_to' : self.solicitante_id.email,                      
                      #'partner_ids' : [(0,0,{'res_partner_id':self.asignacion.partner_id, 'mail_message_id': ids_mail})],
                      'subject' : "Re: %s" % self.codigo,
                      'body_html' : cuerpo_mensaje}

        ids_mail = self.env['mail.mail'].create(const_mail).send()



    @api.one
    def action_resuelto(self):
        self.fecha_solucion=datetime.today()
        diferencia=self.calcular_dias(self.fecha_atendido, self.fecha_solucion)
        self.dia_solucion=diferencia.days
        self.state='resuelto'
        self.enviar_mensaje_status()
       
        return True 

    @api.one
    def action_anulado(self):
        self.state='anulado'
        self.enviar_mensaje_status()

    #Fin de las acciones en los botones


    # PARA CALCULAR LOS DIAS DE UN PROCESO A OTRO  
    def calcular_dias(self, fecha_primera, fecha_segunda):
        formato_fecha = "%Y-%m-%d"
        fc = datetime.strptime(fecha_primera, "%Y-%m-%d %H:%M:%S")
        fh = datetime.strptime(fecha_segunda, "%Y-%m-%d %H:%M:%S")
        """
        fecha_hoy = datetime.strftime(fh, formato_fecha)
        fecha_creado = datetime.strftime(fc, formato_fecha)
        diferencia = datetime.strptime(fecha_hoy, formato_fecha) - datetime.strptime(fecha_creado, formato_fecha) #fecha_hoy - fecha_creado
        """
        diferencia = fh - fc #fecha_hoy - fecha_creado

        return diferencia
    #FIN DEL CALCULO PARA LOS DIAS DE UN PROCESO A OTRO

    #CALCULA LOS DIAS TRANSCURRIDOS

    @api.one
    @api.depends('fecha_actual')
    def _compute_calculo_dias(self):
        if self.state not in ('atendido','resuelto','anulado'):
            carga = datetime.strptime(self.fecha_actual,'%Y-%m-%d %H:%M:%S')
            dias = datetime.today() - carga
            self.retraso = dias.days
        elif self.state not in ('anulado'):
            diferencia=self.calcular_dias(self.fecha_actual, (self.fecha_atendido or datetime.today()))
            self.retraso=diferencia.days
        return True

    @api.one
    @api.depends('fecha_actual')
    def _compute_calculo_dias_resuelto(self):
        if self.state not in ('resuelto','anulado'):
            carga = datetime.strptime(self.fecha_actual,'%Y-%m-%d %H:%M:%S')
            dias = datetime.today() - carga
            self.transcurrido_resuelto = dias.days
        elif self.state not in ('anulado'):
            diferencia=self.calcular_dias(self.fecha_actual, (self.fecha_solucion or datetime.today()))
            self.transcurrido_resuelto=diferencia.days
        return True



#class tools_helpdesk_solicitante(models.Model):
#    """Debería ser una Extensión de la clase hr.employee. Esta clase debe ir en tools.base"""
#    _name = 'tools.helpdesk.solicitante'
#    _rec_name = 'cedula'
#    _columns = {
#        'cedula': fields.integer(string="Cédula", help='Cedula de Identidad del Solicitante'),
#        'nombres': fields.char(string="Nombres", size=60, help='Nombres del Solicitante'),
#        'apellidos': fields.char(string="Apellidos", size=60, help='Apellidos del Solicitante'),
#        'estado_id': fields.Many2one('estado', string="Estados", help='Estado donde trabaja el solicitante'),
#        'regional': fields.boolean("Inces Regional"),
#        'rector': fields.boolean("Inces Rector"),
#        'cargo': fields.many2one('tools.base.hr_cargo', string="Cargo", help='Cargo del Solicitante'),
#        'dependencia_direccion_id': fields.many2one('tools.base.dependencia_direccion', string="Dirección"),
#        'dependencia_gerencia_id': fields.many2one('tools.base.dependencia_gerencia', string="Gerencia", help='Gerencia General o Regional a la que pertenece el solicitante'),
#        'dependencia_gerencia_linea_id': fields.many2one('tools.base.dependencia_gerencia_linea', string="Gerencia de Línea", help='Gerencia de Línea a la que pertenece el solicitante (En caso de Gerencia General)'),
#        'dependencia_cfs_id': fields.many2one('tools.base.dependencia_cfs', string="C.F.S.", help='C.F.S al que pertenece el solicitante (En caso de Gerencia Regional)'),
#        'dependencia_division_id': fields.many2one('tools.base.dependencia_division', string="División", help='División a la que pertenece el solicitante'),
#        'dependencia_coordinacion_id': fields.many2one('tools.base.dependencia_coordinacion', string="Coordinación", help='Coordinación a la que pertenece el solicitante'),
#        'email': fields.char(string="Correo Institucional", size=100, help='Correo Electrónico Institucional del solicitante'),
#        'ext_telefono1': fields.char(string="Extensión 1", size=5, help='Extensión Telefónica del Solicitante: Ej: 2066'),
#        'ext_telefono2': fields.char(string="Extensión 2", size=5, help='Extensión Telefónica del Solicitante: Ej: 2066'),
#        'telefono_personal': fields.char(string="Teléfono Personal", size=11, help='Telefóno Personal del Solicitante. Ej: 04261231234'),
#        'incidencia_ids': fields.one2many('tools.helpdesk.incidencia', 'solicitante_id', 'Incidencias Asociadas'),
#    }
#
#    _sql_constraints = [('cedula_solicitante_uniq', 'unique(cedula)', 'Este solicitante ya ha sido registrado en el sistema (cedula repetida)')]
#
#
#
#    @api.constrains('ext_telefono1','telefono_personal')
#    def validar_numerico(self):
#        if not self.ext_telefono1.isdigit():
#            raise osv.except_osv(('Error'),('La extensión debe contender solo numeros'))
#
#        if not self.telefono_personal.isdigit():
#            raise osv.except_osv(('Error'),('El teléfono debe contender solo numeros'))
#    
#    def name_get(self, cr, uid, ids, context=None):
#        res = []
#        solicitantes = self.browse(cr, uid, ids, context)
#        for solicitante in solicitantes:
#            res.append((solicitante.id, str(solicitante.cedula) + ' - ' + solicitante.nombres + ' ' + solicitante.apellidos))
#        return res
#
#    def create(self, cr, uid, vals, context=None):   #esta campo actualiza el registro
#        vals['cedula'] = uid
#        vals['nombres'] = uid
#        vals['apellidos'] = uid
#        result = super(tools.helpdesk.solicitante, self).create(cr, uid, vals, context=context)
#        return result
#tools_helpdesk_solicitante()

class tools_helpdesk_categoria_incidencia(models.Model):
    """Especificación de la Categoría de la Incidencia,. Ej: Error, Mejora, Nueva, Asistencia"""
    _name = 'tools.helpdesk.categoria_incidencia'
    _rec_name = 'nombre'
    
    codigo = fields.Char('Código', size=10, help='Código de esta Categoría de incidencias')
    nombre = fields.Char('Nombre', size=60, help='Nombre de esta Categoría de Incidencia')
    descripcion = fields.Text('Descripción')
    tipo_incidencia = fields.One2many('tools.helpdesk.tipo_incidencia', 'categoria_incidencia_id', string="tipos de Incidencia", help='Tipos de incidencias que pertenecen a esta Categoría')
    #dependencia_id = fields.many2one('tools.base.dependencia_gerencia','Dependencia')
    

class tools_helpdesk_tipo_incidencia(models.Model):
    """Especificación del tipo de Incidencia, depende de la categoría de incidencia. Ej: Sistema X, Sistema Y, Consumibles, Impresora, Soporte Técnico, Correo, Acceso a Internet, Telefonía, Etc"""
    _name = 'tools.helpdesk.tipo_incidencia'
    _rec_name = 'nombre'
    
    codigo = fields.Char('Código', size=10, help='Código de este tipo de incidencia')
    nombre = fields.Char('Nombre', size=60, help='Nombre de este tipo de incidencia')
    incidencia_ids = fields.One2many('tools.helpdesk.incidencia', 'tipo_incidencia_id', string="Incidencias", help='Incidencias realizadas para este tipo de incidencia')
    categoria_incidencia_id = fields.Many2one('tools.helpdesk.categoria_incidencia', string="Categoría de Incidencia", help='Categoría de la Incidencia a la que pertenece este tipo')
    descripcion = fields.Text('Descripción')
    


class tools_helpdesk_observacion(models.Model):
    _name = 'tools.helpdesk.observacion'

    observacion = fields.Text(string="Observación")
    state = fields.Selection([('registrado','Registrado'),('recibido','Recibido'),('asignado','Asignado'),('proceso','En Proceso'),('atendido','Atendido'),('resuelto','Resuelto')], string="Status", help='Status que tiene la incidencia al momento de hacer la observación')
    incidencia_id = fields.Many2one('tools.helpdesk.incidencia', help='Relación Inversa del One2many')
    

class res_users_helpdesk_inherit(models.Model):
    _inherit= 'res.users'
    _name= 'res.users'
    
    res_partner_id = fields.Many2one('res.partner','Organización', help="Organización a la que pertenece el usuario. Necesario para HelpDesk")
#        'dependencia_id':fields.many2one('tools.base.dependencia_gerencia','Gerencia'),
#        'categoria_incidencia_id':fields.many2one('tools.helpdesk.categoria_incidencia','Area'),
#       'cedula': fields.char(string="Cédula", size=9, help='Cedula de Identidad del Solicitante'),
#        'nombres': fields.char(string="Nombres", size=60, help='Nombres del Solicitante'),
#        'apellidos': fields.char(string="Apellidos", size=60, help='Apellidos del Solicitante'),
#        'estado_id': fields.many2one('estado', string="Estados", help='Estado donde trabaja el solicitante'),
#        'regional': fields.boolean("Inces Regional"),
#        'rector': fields.boolean("Inces Rector"),
#        'cargo': fields.many2one('tools.base.hr_cargo', string="Cargo", help='Cargo del Solicitante'),
#        'dependencia_direccion_id': fields.many2one('tools.base.dependencia_direccion', string="Dirección"),
#       'dependencia_gerencia_id': fields.many2one('tools.base.dependencia_gerencia', string="Gerencia", help='Gerencia General o Regional a la que pertenece el solicitante'),
#        'dependencia_gerencia_linea_id': fields.many2one('tools.base.dependencia_gerencia_linea', string="Gerencia de Línea", help='Gerencia de Línea a la que pertenece el solicitante (En caso de Gerencia General)'),
#        'dependencia_cfs_id': fields.many2one('tools.base.dependencia_cfs', string="C.F.S.", help='C.F.S al que pertenece el solicitante (En caso de Gerencia Regional)'),
#        'dependencia_division_id': fields.many2one('tools.base.dependencia_division', string="División", help='División a la que pertenece el solicitante'),
#        'dependencia_coordinacion_id': fields.many2one('tools.base.dependencia_coordinacion', string="Coordinación", help='Coordinación a la que pertenece el solicitante'),
#        'email': fields.char(string="Correo Institucional", size=100, help='Correo Electrónico Institucional del solicitante'),
#        'ext_telefono1': fields.char(string="Extensión 1", size=5, help='Extensión Telefónica del Solicitante: Ej: 2066'),
#        'ext_telefono2': fields.char(string="Extensión 2", size=5, help='Extensión Telefónica del Solicitante: Ej: 2066'),
#        'telefono_personal': fields.char(string="Teléfono Personal", size=11, help='Telefóno Personal del Solicitante. Ej: 04261231234'),
#        'incidencia_ids': fields.one2many('tools.helpdesk.incidencia', 'solicitante_id', 'Incidencias Asociadas'),

#    _sql_constraints = [('cedula_solicitante_uniq', 'unique(cedula)', 'Este solicitante ya ha sido registrado en el sistema (cedula repetida)')]
##    def onchange_validar_caracter(self, uid, cr, ids, nombres):
##    	v={'value':{}}
##    	if nombres:
##    		if not re.math('^[a-zA-Z\D, ]*$', nombres):
##    			v['value']['nombres']=''
##    			v['warning']={'title':'Error', 'message':'ERROR: Este campo no puede llevar numeros ni caraceres especiales: %s' % nombres}
##    		return v
#    def onchange_validar_numero(self, cr, uid, ids, digito):
#        v = {'value':{}}
#        if digito:
#            if not re.match("^[0-9]*$", digito):
#                v['value']['digito']=''
#                v['warning']={'title':"Error", 'message':"ERROR: Este campo no puede llevar letras ni caracteres especiales: %s" % digito }
#            return v	
##    def name_get(self, cr, uid, ids, context=None):
##        res = []
##        solicitantes = self.browse(cr, uid, ids, context)
##        for solicitante in solicitantes:
##            res.append((solicitante.id, +solicitante.cedula + ' - ' + solicitante.nombres + ' ' + solicitante.apellidos))
##        return res
#    def create(self, cr, uid, vals, context=None):   #esta campo actualiza el registro
#        vals['cedula'] = uid
#        vals['nombres'] = uid
#        vals['apellidos'] = uid
#        result = super(res_users_inherit, self).create(cr, uid, vals, context=context)
#        return result

#nueva clase para adjuntar mas de un documento a la incidencia.
class tools_helpdesk_adjuntos(models.Model):
    _name = 'tools.helpdesk.adjuntos'
    #_rec_name = 'nombre'

    @api.one
    def obtenerNombreArchivo(self):
        """ Esta función agrega el nombre del adjunto (binario) en el campo 'nombre' """
        if self.nombre:
            self.nombre = self.adjunto

    nombre = fields.Char('Nombre del Archivo', store=True, compute ='obtenerNombreArchivo')
    adjunto = fields.Binary(string="Adjuntos", attachment=True, help='Se suben los archivos adicionales que guardan relacion con el documento', filters="*.png,*.svg,*.jpg,*jpeg,*.pdf,*.ods,*.xls,*.xlsx,*.odt,*.doc,*.docx,*.ppt,*.pptx,*.odp")
    observacion = fields.Text(string="Descripción", size=50, help='Breve nota sobre el archivo que se adjunta')
    incidencia_id = fields.Many2one('tools.helpdesk.incidencia', 'incidencia')

#Fin de la clase

#class tools_helpdesk_contexto_nivel1(models.Model):
#    """Estructura de Dependencias Administrativas"""
#    _name = 'tools.helpdesk.contexto_nivel1'
#    _rec_name = 'nombre'
#    _columns = {
#        'codigo': fields.char(string="Código", size=20, help='Código de la Organización'),
#        'nombre': fields.char(string="Nombre", size=60, help='Nombre de la Organización'),
#        'descripcion': fields.text(string="Descripción", help='Descripción de la Organización'),
#       'contexto_nivel2_ids': fields.one2many('tools.helpdesk.contexto_nivel2', 'contexto_nivel1_id', string="Aplicaciones", help='Aplicaciones Soportadas para esta Organización'),
#    }
#tools_helpdesk_contexto_nivel1()

class tools_helpdesk_contexto_nivel1(models.Model):
    """Estructura de Dependencias Administrativas"""
    _name = 'tools.helpdesk.contexto_nivel1'
    _rec_name = 'nombre'
    
    codigo = fields.Char(string="Código", size=20, help='Código de la Aplicación')
    nombre = fields.Char(string="Nombre", size=60, help='Nombre de la Aplicación')
    descripcion = fields.Text(string="Descripción", help='Descripción de la Aplicación')
    res_partner_ids = fields.Many2many('res.partner','respartner_aplicacion_rel','contexto_nivel1_id','res_partner_id', string="Organización", help='Organización que implementa esta aplicación')
    contexto_nivel2_ids = fields.One2many('tools.helpdesk.contexto_nivel2','contexto_nivel1_id', string="Módulo", help='Módulos que pertenecen a esta Aplicación')

class tools_helpdesk_contexto_nivel2(models.Model):
    _name = 'tools.helpdesk.contexto_nivel2'
    _rec_name = 'nombre'

    codigo = fields.Char(string="Código", size=20, help='Código del Módulo')
    nombre = fields.Char(string="Nombre", size=60, help='Nombre del Módulo')
    descripcion = fields.Text(string="Descripción", help='Descripción del Módulo')
    contexto_nivel1_id = fields.Many2one('tools.helpdesk.contexto_nivel1', string="Aplicación", help='Aplicación que implementa este módulo')
    contexto_nivel3_ids = fields.One2many('tools.helpdesk.contexto_nivel3', 'contexto_nivel2_id', string="Operaciones", help='Operaciones disponibles en este Módulo')

class tools_helpdesk_contexto_nivel3(models.Model):
    _name = 'tools.helpdesk.contexto_nivel3'
    _rec_name = 'nombre'

    codigo = fields.Char(string="Código", size=20, help='Código de la Operación')
    nombre = fields.Char(string="Nombre", size=60, help='Nombre de la Operación')
    descripcion = fields.Text(string="Descripción", help='Descripción de la Operación')
    contexto_nivel2_id = fields.Many2one('tools.helpdesk.contexto_nivel2', string="Módulo", help='Módulo que implementa esta operación')
