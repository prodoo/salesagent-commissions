# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012 Andrea Cometa All Rights Reserved.
#                       www.andreacometa.it
#                       openerp@andreacometa.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields,orm
from openerp.tools.translate import _


#	DELETE COMMISSIONS PAYMENT FROM INVOICE
class wzd_invoice_payment_cancellation(orm.TransientModel):

    _name = "wzd.invoice_payment_cancellation"

    _columns = {
        'note_cancellation' : fields.boolean('Delete Notes'),
        }

    def annulla_pagamento(self, cr, uid, ids, context={}):
        if not 'active_ids' in context:
            raise orm.except_orm(_('Invalid Operation!'), _('Select at least one line!'))
        # ----- Seleziona l'oggetto in base al modello attivo e ne segnala il pagamento
        wizard_obj = self.browse(cr,uid,ids[0])
        invoice_obj = self.pool.get(context['active_model'])
        line_ids = []
        invoices = invoice_obj.browse(cr, uid, context['active_ids'], context)
        for invoice in invoices:
            for line in invoice.invoice_line:
                if line.commission_presence:
                    line_ids.append(line.id)
        # ----- Delete Payment
        args = {'payment_commission_date' : False,
            'paid_commission' : False,
            'paid_commission_value' : 0.0,
            'paid_commission_percentage_value':0.0}
        if wizard_obj.note_cancellation:
            args['payment_commission_note'] = ''
        self.pool.get('account.invoice.line').write(cr, uid, line_ids, args)
        return {'type': 'ir.actions.act_window_close'}
