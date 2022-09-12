from odoo import api, fields, models


class Member(models.Model):
    _name = 'djperpus.member'
    _description = 'New Description'

    name = fields.Char(string='Name')
    nim = fields.Char(string='NIM')
    poin = fields.Integer(string='Experience Point')
    level = fields.Selection([
        ('beginner', 'Beginner'), ('intermediate','Intermediate'), ('advanced','Advanced'),('master','Master'), ('grandmaster','Grandmaster')
    ], string='Level', required="True", default="beginner")
    
    
    pinjam_ids = fields.One2many(comodel_name='djperpus.pinjam', inverse_name='member_id', string='Borrowing List')

    
    
    
