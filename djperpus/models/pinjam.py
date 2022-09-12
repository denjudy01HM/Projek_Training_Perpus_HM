from email.policy import default
from odoo import api, fields, models


class Pinjam(models.Model):
    _name = 'djperpus.pinjam'
    _description = 'New Description'

    name = fields.Char(string='Borrowing ID')
    tgl_pinjam = fields.Date(string='Borrowing Date', default = fields.Date.today())
    tgl_kembali = fields.Date(string='Return Date')
    denda= fields.Integer(string='Penalty', default=0)
    

    member_id = fields.Many2one(comodel_name='djperpus.member', string='Name')
    detailpinjam_ids = fields.One2many(comodel_name='djperpus.detailpinjam', inverse_name='pinjam_id', string='Borrowing List')

class DetailPinjam(models.Model):
    _name = 'djperpus.detailpinjam'
    _description = 'New Description'

    name = fields.Char(string='Borrowing ID')
    pinjam_id = fields.Many2one(comodel_name='djperpus.pinjam', string='Borrowing Detail')
    buku_id = fields.Many2one('djperpus.buku', string='Book List')
    qty = fields.Integer(string='Quantity')
    


