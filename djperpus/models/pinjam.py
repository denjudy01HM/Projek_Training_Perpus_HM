from datetime import datetime, timedelta
from email.policy import default
# from re import A
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Pinjam(models.Model):
    _name = 'djperpus.pinjam'
    _description = 'New Description'

    name = fields.Char(string='Borrowing ID')
    tgl_pinjam = fields.Date(string='Borrowing Date', default = fields.Date.today())
    tgl_batas = fields.Date(string='Due Date', readonly=True)
    tgl_kembali = fields.Date(string='Return Date')
    denda= fields.Integer(string='Penalty', default=0)
    state = fields.Selection(string="Status", selection=[('draft','Draft'),
                                                            ('borrowed','Borrowed'),
                                                            ('incomplete','Incomplete'),
                                                            ('done','Done')], 
                                                            required=True, readonly=True, default='draft')

    member_id = fields.Many2one(comodel_name='djperpus.member', string='Name')
    detailpinjam_ids = fields.One2many(comodel_name='djperpus.detailpinjam', inverse_name='pinjam_id', string='Borrowing List', store=True)
    total_pinjem = fields.Integer(string='Amount', compute="_compute_total_pinjem", store=True)
    

    @api.depends('detailpinjam_ids')
    def _compute_total_pinjem(self):
        for rec in self:
            a = sum(self.env['djperpus.detailpinjam'].search([('pinjam_id','=',rec.id)]).mapped('total_pinjam'))
            rec.total_pinjem = a
            print('===========>>>>',rec.total_pinjem)

    @api.depends('detailpinjam_ids')
    @api.constrains('detailpinjam_ids')
    def _check_buku_lines(self):
        for record in self:
            if len(record.detailpinjam_ids) > 1:
                raise ValidationError('You only can add one kind of book at time !!') 
            if len(record.detailpinjam_ids) < 1:
                raise ValidationError('Please input at least 1 book!!') 
            
            

    @api.onchange('tgl_pinjam')
    def _onchange_duedate(self):
        for rec in self:
            rec.tgl_batas = rec.tgl_pinjam + timedelta(days=14)


    def unlink(self):
        if self.detailpinjam_ids:
            pinjam = []
            holding = []
            total = []
            for record in self:
                pinjam.append(self.env['djperpus.detailpinjam'].search(
                    [('pinjam_id', '=', record.id)]))
                holding.append(self.env['djperpus.pinjam'].search(
                    [('id', '=', record.id)]))
                total.append(self.env['djperpus.member'].search(
                    [('id', '=', record.member_id.id)]))
                print(pinjam)
                print(holding)
                print(total)
                
            for ob in pinjam:
                for rec in ob:
                    print(rec.buku_id.buku_stok, ' ', str(rec.qty))
                    rec.buku_id.buku_stok += rec.qty
            
            for obj in holding:
                self.env['djperpus.buku'].search([('member_ids','=',obj.member_id.id)]
                ).write({'member_ids':[(3,obj.member_id.id)]})

            # for objj in total:
            #     print(objj.total_hold, ' ', str(ob.qty))
            #     objj.total_hold -= ob.qty

        record = super(Pinjam, self).unlink()

    _sql_constraints = [
        ('unik_trx','unique (name)','Borrow ID is available !!')
    ]


class DetailPinjam(models.Model): 
    _name = 'djperpus.detailpinjam'
    _description = 'New Description'

    name = fields.Char(string='Borrowing ID')
    pinjam_id = fields.Many2one(comodel_name='djperpus.pinjam', string='Borrowing Detail', ondelete="cascade")
    buku_id = fields.Many2one('djperpus.buku', string='Book List')
    qty = fields.Integer(string='Quantity')
    total_balik = fields.Integer(string='Return', default=0)
    total_pinjam = fields.Integer(string='Total Book Holds', compute="_compute_total_pinjam", store=True, readonly=True)
    dtlmember_id = fields.Many2one(comodel_name='djperpus.member', string='member')
    

    @api.depends('qty')
    def _compute_total_pinjam(self):
        for rec in self:
            rec.total_pinjam = rec.qty
        
    @api.model
    def create(self, values):
        # Add code here
        record = super(DetailPinjam, self).create(values)
        if record.qty:
            res = self.env['djperpus.buku'].search([('id','=',record.buku_id.id)])
            res2 = self.env['djperpus.pinjam'].search([('id','=',record.pinjam_id.id)])
            # record.member_id = res2.member_id
            res3 = self.env['djperpus.member'].search([('pinjam_ids','=',record.pinjam_id.id)])
            res.write({'buku_stok' : record.buku_id.buku_stok - record.qty})
            res.write({'member_ids': [(4,record.pinjam_id.member_id.id)]})                          
            res.write({'pinjam_id': record.pinjam_id})                      
            res2.write({'state' : 'borrowed'})
            for rec in record.pinjam_id.detailpinjam_ids:
                res3.write({'detailpinjam_ids': [(4,rec.id)]})

        return record
    
    @api.constrains('qty')
    def _check_qty(self):
        for rec in self:
            
            if rec.qty <1 :
                raise ValidationError("Transaction failed \nYou must add '{}' at least one".format(rec.buku_id.name))
            elif (rec.buku_id.buku_stok < rec.qty):
                raise ValidationError("Transaction failed, because there are only {} left on '{}'".format(rec.buku_id.buku_stok,rec.buku_id.name))   
        b = self.env['djperpus.member'].search([('id','=',self.pinjam_id.member_id.id)])
        c = self.env['djperpus.pinjam'].search([('id','=',self.pinjam_id.id)])
        print("+++++++++++>>>>>> TOTAL PINJEM",c.total_pinjem)
        tamps = 0
        if b.total_hold < 1:
            tamps = c.total_pinjem
        print("=======>>>>>> TOTAL HOLD",b.total_hold)
        print("+++++++++++>>>>>> TOTAL PINJEM",c.total_pinjem)
        if b.total_hold+tamps > b.limit :
            raise ValidationError("Member {} can only borrow {} books because of the level limitations".format(b.name,b.limit))
            
    # @api.constrains('field_name')
    # def _check_field_name(self):
    #     a = self.env['djperpus.detailpinjam'].search([('pinjam_id','=',record.id),('dtlmember_id','=',record.member_id.id)])
    #         print("========== THIS IS A",a)
    #         raise ValidationError()
       
    

