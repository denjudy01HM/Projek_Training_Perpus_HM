from odoo import api, fields, models


class Perpanjang(models.TransientModel):
    _name = 'djperpus.perpanjang'

    pinjam_id = fields.Many2one('djperpus.pinjam', string='Borrow ID')
    member_id = fields.Many2one('djperpus.member', string='Member Name', readonly=True)
    tgl_baru = fields.Date(string='Renew Date')
    hide = fields.Boolean(string='Hide')
    
    def button_perpanjang(self):
        for rec in self:
            self.env['djperpus.pinjam'].search([('id','=',rec.pinjam_id.id)]).write({'tgl_batas': rec.tgl_baru})

    @api.onchange('pinjam_id','hide')
    def _onchange_member_id(self):
        for rec in self:
            if rec.pinjam_id:
                rec.member_id = rec.env['djperpus.member'].search([('pinjam_ids','=',rec.pinjam_id.id)])
                rec.hide = True
            else:
                rec.hide = False


    
