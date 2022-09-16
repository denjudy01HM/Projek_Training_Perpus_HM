from odoo import api, fields, models

from odoo.exceptions import ValidationError

class Perpanjang(models.TransientModel):
    _name = 'djperpus.perpanjang'

    pinjam_id = fields.Many2one('djperpus.pinjam', string='Borrow ID')
    member_id = fields.Many2one('djperpus.member', string='Member Name', readonly=True, store=True)
    tgl_baru = fields.Date(string='Renew Date')
    buku_id = fields.Many2one('djperpus.buku', string='Book Name', domain="[('member_ids','=', member_id)]", store=True)
    renew_same_book = fields.Integer(string='Amount', store=True)
    hide = fields.Boolean(string='Hide')
    tipe_input = fields.Selection(string='Input TYpe', 
                                selection=[('renewdate', 'Renew Borrow Date'),
                                 ('renewbook', 'Renew Borrow Book'),], required=True, default='renewdate')
    
    
    def button_perpanjang(self):
        for rec in self:
            if rec.tipe_input == 'renewdate':
                self.env['djperpus.pinjam'].search([('id','=',rec.pinjam_id.id)]).write({'tgl_batas': rec.tgl_baru})
            elif rec.tipe_input == 'renewbook':
                a = self.env['djperpus.detailpinjam'].search([('pinjam_id','=',rec.pinjam_id.id),('buku_id','=',rec.buku_id.id)])
                b = self.env['djperpus.member'].search([('pinjam_ids','=',rec.pinjam_id.id)])
                c = self.env['djperpus.buku'].search([('id','=',rec.buku_id.id)])
                if rec.buku_id.buku_stok >= rec.renew_same_book:
                    if b.total_hold + rec.renew_same_book < b.limit :
                        c.write({'buku_stok' : rec.buku_id.buku_stok - rec.renew_same_book})
                        qty_tamp = a.qty
                        if a.total_pinjam != qty_tamp:
                            a.qty += rec.renew_same_book
                            a.total_pinjam = (a.total_pinjam-qty_tamp) + rec.renew_same_book
                        a.qty += rec.renew_same_book
                        print('========= BOOK total hold skrng', b.total_hold)
                        b.total_hold += rec.renew_same_book
                        print('========= BOOK total hold skrng', b.total_hold)
                    else:
                        raise ValidationError("Member {} can only borrow {} books because of the level limitations".format(b.name,b.limit))
                else:
                    raise ValidationError("Transaction failed, because there are only {} left on '{}'".format(rec.buku_id.buku_stok,rec.buku_id.name))   
                if rec.renew_same_book < 1:
                    raise ValidationError ("Your amount number is not valid !!!")

    @api.onchange('pinjam_id','hide')
    def _onchange_member_id(self):
        for rec in self:
            if rec.pinjam_id:
                rec.member_id = rec.env['djperpus.member'].search([('pinjam_ids','=',rec.pinjam_id.id)])
                rec.hide = True
            else:
                rec.hide = False

    


    
