from odoo import api, fields, models
from odoo.exceptions import ValidationError

class MotorcycleRegistry(models.Model):
    _name = "motorcycle.registry"
    _description = "Infos" 

    registry_number = fields.Char(string="Registry Number", default="MRN0001", copy=False, required=True, readonly=True)

    vin = fields.Char(string="Vin Number", required=True)
    
    #first_name = fields.Char(string="First Name", required=True)
    
    #last_name = fields.Char(string="Last Name", required=True)

    picture = fields.Image(string = "Picture")

    current_mileage = fields.Float(string = 'Current Mileage', digits = 'mileage')

    license_plate = fields.Char(string="License Plate")

    certificate_title = fields.Binary(string="Certificate Title")
    
    register_date = fields.Date(string="Registered Date")

    brand = fields.Char(compute='_compute_from_vin')
    make = fields.Char(compute='_compute_from_vin')
    model = fields.Char(compute='_compute_from_vin')
    
    owner_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict')
    owner_phone = fields.Char(related='owner_id.phone')
    owner_email = fields.Char(related='owner_id.email')


    @api.constrains('vin')
    def _check_vin(self):
        for motorcycle_registry in self:       
            vin_num = motorcycle_registry.vin

            if (len(vin_num) != 14):
                raise ValidationError('The vin number must be in correct format')

            make = vin_num[0:2]
            model = vin_num[2:4]
            year = vin_num[4:6]
            battery_capacity = vin_num[6:8]
            serial_number = vin_num[8:]

            if not (make.isupper() and 
                    model.isupper() and 
                    year.isdigit() and 
                    (battery_capacity.isdigit() or battery_capacity.isupper()) and
                    serial_number.isdigit()):
                raise ValidationError('The vin number must be in correct format')
            
            duplicates = self.search([('vin', '=', vin_num)])


            if (len(duplicates) > 1):
                raise ValidationError('The vin number must not be identical')
            


    @api.constrains('license_plate')
    def _check_license_plate(self):
    
        for registry in self:
            plate = registry.license_plate
            if plate:
                plate_len = len(plate)
                if (plate_len < 2 or plate_len > 9):
                    raise ValidationError('The license plate must be in correct format')

                
                upper_count = 0
                digit_count = 0
                optional_count = 0
                for c in plate:
                    if c.isupper():
                        if digit_count > 0 and optional_count < 2:
                            optional_count += 1
                        elif digit_count == 0 and upper_count < 4:
                            upper_count += 1
                        else:
                            raise ValidationError('The license plate must be in correct format')

                        
                    elif c.isdigit() and upper_count > 0 and digit_count < 3: 
                        digit_count += 1
                    else:
                        raise ValidationError('The license plate must be in correct format')

                
                if digit_count == 0:
                    raise ValidationError('The license plate must be in correct format')


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('registry_number', ('MRN0001')) == ('MRN0001'):
                vals['registry_number'] = self.env['ir.sequence'].next_by_code('registry.number')
        return super().create(vals_list)

    @api.depends('vin')
    def _compute_from_vin(self):
        for registry in self:
            registry.brand = registry.vin[:2]
            registry.make = registry.vin[2:4]
            registry.model = registry.vin[4:6]
