from odoo import api, fields, models


class TambahStokBuku(models.Model):
    _name = 'djperpus.tambahstokbuku'
    
    buku_id = fields.Many2one('djperpus.buku', string='Book Title')
    jml_tambahan = fields.Integer(string='Amount')

    def button_tambahstokbuku(self):
        for rec in self:
            self.env['djperpus.buku'].search([('id', '=', rec.buku_id.id)]).write({'buku_stok' : rec.buku_id.buku_stok + rec.jml_tambahan})
    
