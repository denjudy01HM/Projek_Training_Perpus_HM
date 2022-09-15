from odoo import api, fields, models


class Member(models.Model):
    _name = 'djperpus.member'
    _description = 'New Description'

    name = fields.Char(string='Name')
    nim = fields.Char(string='NIM')
    no_telp = fields.Char(string='Phone Number')
    alamat = fields.Text('Address')
    poin = fields.Integer(string='Experience Point', default=0)
    level = fields.Char(string='Level', compute="_compute_level")
    limit = fields.Integer(string='Borrow Limit', compute="_compute_limit")
    total_hold = fields.Integer(string='Books Hold Total', default=0,store=True,
                                 compute="_compute_total_hold", readonly=False)
    temp_total_hold = fields.Integer(string='Temp total hold', store=True,default=0)
    
    pinjam_ids = fields.One2many(comodel_name='djperpus.pinjam',
                                 inverse_name='member_id', string='Borrowing List')
    buku_ids = fields.Many2many('djperpus.buku', string='Holdings')
    detailpinjam_ids = fields.One2many(comodel_name='djperpus.detailpinjam', inverse_name='member_id', string='Reff DTL')

    @api.depends('detailpinjam_ids','total_hold','temp_total_hold')
    def _compute_total_hold(self):
        for rec in self:
            a = self.env['djperpus.detailpinjam'].search([('member_id','=',rec.id)])
            print(">>>>>>==========",a)
            rec.temp_total_hold = 0
            for ob in a:
                if ob.total_pinjam:
                    print("==========>>>>>>>",rec.total_hold)
                    rec.temp_total_hold += ob.total_pinjam
                    rec.total_hold = rec.temp_total_hold
            
    

    @api.depends('poin')
    def _compute_level(self):
        for rec in self:
            if (rec.poin >= 10 and rec.poin < 20):
                rec.level = 'Intermediate'
            elif (rec.poin >= 20 and rec.poin < 30):
                rec.level = 'Advanced'
            elif (rec.poin >= 30 and rec.poin < 40):
                rec.level = 'Master'
            elif (rec.poin >= 40):
                rec.level = 'Grandmaster'
            else:
                rec.level = 'Beginner'

    @api.depends('level')
    def _compute_limit(self):
        for rec in self:
            if rec.level == 'Beginner':
                rec.limit = 5
            elif rec.level == 'Intermediate':
                rec.level = 6
            elif rec.level == "Advanced":
                rec.level = 7
            elif rec.level == "Master":
                rec.level = 8
            elif rec.level == 'Grandmaster':
                rec.level = 10
    
    
    # for rec in self:
        #     a = self.env['djperpus.pinjam'].search([('member_id','=',rec.id)])
        #     print("++++==========",a)
        #     rec.total_hold = 0
        #     for recs in a:
        #         b = self.env['djperpus.detailpinjam'].search([('pinjam_id','=',recs.id)])
        #     print(">>>>>>==========",b)
        #     for recs in b:
        #         c = self.env['djperpus.detailpinjam'].search([('pinjam_id','=',recs.id)])
        #         for obs in c:
        #             if obs.total_pinjam:
        #                 rec.total_hold += obs.total_pinjam
        # a = []
        # for rec in self:
