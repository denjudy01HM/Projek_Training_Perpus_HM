# -*- coding: utf-8 -*-
# from odoo import http


# class Djperpus(http.Controller):
#     @http.route('/djperpus/djperpus', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/djperpus/djperpus/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('djperpus.listing', {
#             'root': '/djperpus/djperpus',
#             'objects': http.request.env['djperpus.djperpus'].search([]),
#         })

#     @http.route('/djperpus/djperpus/objects/<model("djperpus.djperpus"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('djperpus.object', {
#             'object': obj
#         })
