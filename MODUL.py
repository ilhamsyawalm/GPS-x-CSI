from odoo import api, fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    csi_new = fields.Char("CSI New", store=True, readonly=False)
    csi_old = fields.Char(string='CSI', store=True, readonly=False, compute='compute_csi_old')

    @api.depends('partner_id')
    def compute_csi_old(self):
        for task in self:
            if task.partner_id:
                task.csi_old = task.partner_id.csi_old
            else:
                task.csi_old = False

    def update_partner_location(self):
        partners = self.env['res.partner'].search([])
        for partner in partners:
            task = self.search([('partner_id', '=', partner.id)], limit=1, order='write_date desc')
            if task:
                partner.write({
                    'partner_longitude': 0.00,
                    'partner_latitude': 0.00,
                })
                if task.x_longitude and task.x_latitude:
                    partner.write({
                        'partner_longitude': task.x_longitude,
                        'partner_latitude': task.x_latitude,
})

class Customers(models.Model):
    _inherit = 'res.partner'
    
    csi_old = fields.Char('CSI Old', store=True)

class HelpdeskTickets(models.Model):
    _inherit = 'helpdesk.ticket'
    
    csi_old = fields.Char("CSI", store=True, compute='compute_csi')
        
    @api.depends('partner_id')
    def compute_csi(self):
        for task in self:
            if task.partner_id:
                task.csi_old = task.partner_id.x_csi
            else:
                task.csi_old = False