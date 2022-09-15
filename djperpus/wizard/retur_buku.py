from odoo import api, fields, models
from datetime import datetime, timedelta


class ReturBuku(models.Model):
    _name = 'djperpus.returbuku'
    
    pinjam_id = fields.Many2one('djperpus.pinjam', string='Borrow ID')
    member_id = fields.Many2one('djperpus.member', string='Member Name', readonly=True)
    buku_id = fields.Many2one('djperpus.buku', string='Book Title', domain="[('member_ids','=',member_id)]")
    temp_denda = fields.Integer(string='Penalty Fee', readonly=True)
    temp_tgl_batas = fields.Date(string='Due Date', readonly=True)
    temp_tgl_kembali = fields.Date(string='Return Date', default = fields.Date.today())
    temp_qty = fields.Integer(string='Amount')
    
    
    hide = fields.Boolean(string='Hide')

    @api.onchange('pinjam_id','temp_tgl_batas','temp_tgl_kembali')
    def _onchange_denda(self):
        for rec in self:
            if rec.pinjam_id:
                due = self.env['djperpus.pinjam'].search([('id','=',rec.pinjam_id.id)])
                rec.temp_tgl_batas = due.tgl_batas
                selisih = rec.temp_tgl_kembali-rec.temp_tgl_batas
                if int(str(selisih.days)) > 0:
                    if int(str(selisih.days)) > 7:
                        persentase = int(str(selisih.days)) // 7
                        rec.temp_denda = 1000+(1000*((persentase+1)/5))
                    else:
                        rec.temp_denda = 1000
                else:
                    rec.temp_denda = 0
                rec.hide = True
            else:
                rec.hide = False
      
    
    def button_returbuku(self):
        for rec in self:
            res = self.env['djperpus.pinjam'].search([('id','=',rec.pinjam_id.id)])
            res2 = self.env['djperpus.detailpinjam'].search([('pinjam_id','=',rec.pinjam_id),('buku_id','=',rec.buku_id)])
            if rec.temp_qty <= res2.total_pinjam:
                res2.total_pinjam -= rec.temp_qty
                res2.total_balik += rec.temp_qty
                res2.buku_id.buku_stok -= rec.temp_qty
                res.write({'state': 'incomplete'})
            #kurang total hold sama unlink sama poin
            if res2.total_pinjam < 1:
                res.write({'state': 'done'})

            res.write({'tgl_kembali': rec.temp_tgl_kembali})
            res.write({'denda': rec.temp_denda})

    @api.onchange('pinjam_id','hide')
    def _onchange_member_id(self):
        for rec in self:
            if rec.pinjam_id:
                rec.member_id = rec.env['djperpus.member'].search([('pinjam_ids','=',rec.pinjam_id.id)])
                rec.hide = True
            else:
                rec.hide = False
    
    
