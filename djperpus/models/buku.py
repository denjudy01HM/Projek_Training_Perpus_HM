from odoo import api, fields, models


class Buku(models.Model):
    _name = 'djperpus.buku'
    _description = 'New Description'

    name = fields.Char(string='Title')
    buku_id = fields.Char(string='ISBN')
    buku_stok = fields.Char(string='Item Availability')

    kategoribuku_id = fields.Many2one('djperpus.kategoribuku', string='Kategori Buku')
    
class KategoriBuku(models.Model):
    _name = 'djperpus.kategoribuku'
    _description = 'New Description'

    # name = fields.Selection([
    #     ('agriculuture', 'Agriculture'), ('computerscience', 'Computer Science'), ('education', 'Education'), 
    #     ('geography', 'Geography'), ('politicalscience', 'Political Science'),
    # ], string='Categories')
    nama = fields.Char(string='Category')
    
    
    buku_ids = fields.One2many(comodel_name='djperpus.buku', 
                                inverse_name='kategoribuku_id', 
                                string='List Buku')
    
