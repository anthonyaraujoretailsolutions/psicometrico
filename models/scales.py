from odoo import models, fields, api

class ScaleQuestion(models.Model):
    _name="survey.scale"
    name = fields.Char(string='Nombre')
    subscale_id = fields.One2many(comodel_name='survey.subscale', inverse_name='scale_id', string='SubEscala')
    
class subScaleQuestion(models.Model):
    _name="survey.subscale"
    name = fields.Char(string='Nombre')
    scale_id = fields.Many2one(comodel_name='survey.scale', string='Escala')
    score = fields.Integer(string='Puntaje por Escala')

