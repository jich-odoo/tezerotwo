from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

class MotorcycleRegistry(models.Model):
    _name = "motorcycle.registry"
    _description = "Infos" 

    registry_number = fields.Char(string="Registry Number", default="MRN0001", copy=False, required=True, readonly=True)

    vin = fields.Char(string="Vin Number", required=True)
    
    first_name = fields.Char(string="First Name", required=True)
    
    last_name = fields.Char(string="Last Name", required=True)

    picture = fields.Image(string = "Picture")

    current_mileage = fields.Float(string = 'Current Mileage', digits = 'mileage')

    license_plate = fields.Char(string="License Plate")

    certificate_title = fields.Binary(string="Certificate Title")
    
    register_date = fields.Date(string="Registered Date")

    @api.constrains('vin','license_plate')

    def _check_vin(self):
        validation="^[A-Z]{2}[A-Z]{2}\d{2}([A-Z]|\d){2}\d{6}$"
        for registry in self:
            if (not re.search(validation,registry.vin)):
                raise ValidationError('The vin number must be in correct format')

    def _check_license_plate(self):
        validation="[A-Z]{1,4}\d{1-3}[A-Z]{2}|$"
        for registry in self:
            if (not re.search(validation,registry.license_plate)):
                raise ValidationError('The license plate must be in correct format')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('registry_number', ('MRN0001')) == ('MRN0001'):
                vals['registry_number'] = self.env['ir.sequence'].next_by_code('registry.number')
        return super().create(vals_list)