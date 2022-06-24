from odoo import tools, models, fields, api, _
from datetime import datetime

class CrmStageStat(models.Model):
    _name = "crm.stage.stat"
    _description = "crm.stage.stat"

    lead_id = fields.Many2one('crm.lead',string='Lead')
    stage_from_id = fields.Many2one('crm.stage',string='Etapa desde')
    stage_to_id = fields.Many2one('crm.stage',string='Etapa hasta')
    date = fields.Datetime('Fecha')
    diff_days = fields.Integer('Dias')

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def write(self, vals):
        stage_from_id = stage_to_id = None
        if 'stage_id' in vals:
            for rec in self:
                stage_from_id = rec.stage_id.id
                stage_to_id = vals.get('stage_id')
        res = super(CrmLead, self).write(vals)
        if stage_from_id and stage_to_id:
            for rec in self:
                prev_stage = self.env['crm.stage.stat'].search([('lead_id','=',rec.id)],order='id desc',limit=1)
                if prev_stage:
                    diff_days = (datetime.now() - prev_stage.date).days
                else:
                    diff_days = (datetime.now() - rec.create_date).days
                vals = {
                        'lead_id': rec.id,
                        'stage_from_id': stage_from_id,
                        'stage_to_id': stage_to_id,
                        'date': str(datetime.now())[:19],
                        'diff_days': diff_days,
                        }
                stat_id = self.env['crm.stage.stat'].create(vals)
        return res

    stage_stat_ids = fields.One2many(comodel_name='crm.stage.stat',inverse_name='lead_id',string='Stage stats')
