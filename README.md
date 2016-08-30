## Módulo: tools_helpdesk
Para los permisos de acceso revisar archivo “Matriz CRUD”

### Reglas de Acceso (security/ir.rule.xml)
* El Analista de soporte puede ver todas las Incidencias, de todas las organizaciones
* El Supervisor organizacional solo puede ver las incidencias de su organización
  * <field name="domain_force">[('res_partner_id','=',user.res_partner_id.id)]</field>
* El Usuario solo puede ver sus propias incidencias
  * <field name="domain_force">[('solicitante_id','=',user.id)]</field>


### Campos Filtrados (domain):
* El usuario solo verá las aplicaciones que estén relacionadas con su organización
* El usuario solo verá los módulos relacionados a la aplicación seleccionada
* El usuario solo verá las operaciones relacionadas al módulo seleccionado

### Reglas de Negocio
* El código de la incidencia se autogenera luego crear la incidencia y no es modificable
* El Analista puede elegir cualquier solicitante al registrar una incidencia
* El Supervisor puede elegir cualquier solicitante al registrar una incidencia
* El usuario no puede modificar el solicitante al registrar una incidencia. Tendrá precargado su usuario (ver más abajo cómo)
* El workflow es manipulado solo por el Analista

### Nomenclatura de Colores de la vista lista de incidencia

* Registrado: Naranja
* Recibido: Rojo
* Asignado: Azul
* En Proceso: Marrón
* Atendido: Oliva
* Resulto: Verde

```
<tree string="tools.helpdesk.incidencia" 
         colors= "orange:state=='registrado';
                  red:state=='recibido';
                  blue:state=='asignado';
                  brown:state=='proceso';
                  green:state=='resuelto';
                  olive:state=='atendido'">
      
      <!-- Aquí van los campos del tree -->
    
    </tree>
```

### Cómo bloquear (Solo lectura) un campo según el grupo del usuario conectado
 
En el view.xml
```
<record id="incidicendia_extended_view_form" model="ir.ui.view">
            <field name="name">tools.helpdesk.incidencia.form.inherit</field>
            <field name="model">tools.helpdesk.incidencia</field>
            <field name="inherit_id" ref="view_tools_helpdesk_incidencia_form" />
            <field name="groups_id" eval="[(6,0, [ref('tools_helpdesk.group_help_desk_Usuario')])]"/>
            <field name="arch" type="xml">                
                <field name="solicitante_id" position="attributes">
                   <attribute name="attrs">{'readonly':True}</attribute>                   
                </field>                
            </field>
</record>   
```

### Cómo cambiar el tamaño máximo para un archivo en un campo Binary

En el archivo: .../addons/web/static/src/js/view_form.js (en mi versión del archivo, línea 5620)
En el atributo `this.max_upload_size = 25 * 1024 * 1024; // 25Mo` establece
  `this.max_upload_size = 5 * 1024 * 1024; // 5Mo`


### Enviar un correo a través de un email.template

Creamos nuestro método
```
    @api.cr_uid_id_context
    def send_mail(self, cr, uid, ids, context=None, template=''):
       for object in self.browse(cr, uid, ids, context=context):
            template_id = self.pool.get('email.template').search(cr, uid, [("name","=",template)])
            if template_id:
                mail_message = self.pool.get('email.template').send_mail(cr,uid,template_id[0],object.id)
```

Y lo invocamos de la siguiente manera:
```
    self.send_mail(template='ticket_asignado')
```


