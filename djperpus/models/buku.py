from odoo import api, fields, models


class Buku(models.Model):
    _name = 'djperpus.buku'
    _description = 'New Description'

    name = fields.Char(string='Title')
    buku_id = fields.Char(string='ISBN')
    buku_stok = fields.Integer(string='Item Availability')

    kategoribuku_id = fields.Many2one('djperpus.kategoribuku', string='Kategori Buku', ondelete="cascade")
    
class KategoriBuku(models.Model):
    _name = 'djperpus.kategoribuku'
    _description = 'New Description'

    name = fields.Selection([
        ('agriculuture', 'Agriculture'), ('computerscience', 'Computer Science'), ('education', 'Education'), 
        ('geography', 'Geography'), ('politicalscience', 'Political Science'),
    ], string='Categories', required="True", default="agriculuture")
    buku_rak = fields.Char(string='Book Section')
    buku_total_categ = fields.Integer(compute="_compute_total_buku", string='Books Total')
    
    buku_ids = fields.One2many(comodel_name='djperpus.buku', 
                                inverse_name='kategoribuku_id', 
                                string='List Buku')
    
    @api.depends('buku_ids')
    def _compute_total_buku(self):
        for record in self:
            record.buku_total_categ = len(self.env['djperpus.buku'].search([('kategoribuku_id', '=', record.id)]))
    
