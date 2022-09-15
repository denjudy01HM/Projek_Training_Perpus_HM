from odoo import api, fields, models


class Member(models.Model):
    _name = 'djperpus.member'
    _description = 'New Description'

    name = fields.Char(string='Name')
    nim = fields.Char(string='NIM')
    no_telp = fields.Char(string='Phone Number')
    alamat = fields.Text('Address')
    poin = fields.Integer(string='Experience Point', default=0, store=True)
    level = fields.Char(string='Level', compute="_compute_level")
    limit = fields.Integer(string='Borrow Limit', compute="_compute_limit")
    total_hold = fields.Integer(string='Books Hold Total', default=0,store=True,
                                 compute="_compute_total_hold", readonly=False)
    temp_total_hold = fields.Integer(string='Temp total hold', store=True,default=0)
    
    pinjam_ids = fields.One2many(comodel_name='djperpus.pinjam',
                                 inverse_name='member_id', string='Borrowing List')
    buku_ids = fields.Many2many('djperpus.buku', string='Holdings')
    detailpinjam_ids = fields.One2many(comodel_name='djperpus.detailpinjam', inverse_name='dtlmember_id', string='Reff DTL')
    

    @api.depends('detailpinjam_ids','pinjam_ids')
    def _compute_total_hold(self):
        for rec in self:
            a = self.env['djperpus.detailpinjam'].search([('dtlmember_id','=',rec.id)])
            # res4 = sum(self.env['djperpus.pinjam'].search([('member_id','=',tamp)]).mapped('total_pinjem'))
            rec.temp_total_hold = 0
            tamp = []
            tamps = 0
            tamps_final=0
            for ob in a: 
                if ob.buku_id in tamp:
                    print("==========>>>>>>> HOLD di set ",rec.total_hold)
                    tamps += ob.total_pinjam
                tamp.append(ob.buku_id)
                rec.temp_total_hold += ob.total_pinjam
                print("==========>>>>>>>",ob.total_pinjam)
                rec.total_hold = rec.temp_total_hold
            # tamps_final = tamps
            # rec.total_hold += tamps_final
            print("==========>>>>>>> HOLD",rec.total_hold)
            print("==========>>>>>>> Tamps",tamps_final)
            
    

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
                rec.limit = 6
            elif rec.level == "Advanced":
                rec.limit = 7
            elif rec.level == "Master":
                rec.limit = 8
            elif rec.level == 'Grandmaster':
                rec.limit = 10
    
    
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
