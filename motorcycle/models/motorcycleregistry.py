from odoo import models, fields

class MotorcycleRegistry(models.Model):
    _name = "motorcycle.registry"
    _description = "Infos" 

    registry_number = fields.Char(string="Registery Number", required=True)

    vin = fields.Char(string="Vin Number", required=True)
    
    first_name = fields.Char(string="First Name", required=True)
    
    last_name = fields.Char(string="Last Name", required=True)

    picture = fields.Image(string = "Picture")

    current_mileage = fields.Float(string = 'Current Mileage', digits = 'mileage')

    license_plate = fields.Char(string="License Plate")

    certificate_title = fields.Binary(string="Certificate Title")
    
    register_date = fields.Date(string="Registered Date")