from odoo import models, fields, api

class SurveysurveyInherit(models.Model):
    _inherit="survey.question"
    scale = fields.Many2many('survey.scale', string='Escala')
    subscale = fields.Many2many('survey.subscale', string='Sub-Escala') 
    score = fields.Integer(string='Puntaje')

class SurveylabelsInherit(models.Model):
    _inherit="survey.label"
    correct_answer = fields.Boolean(string='Respuesta Correcta')
    
