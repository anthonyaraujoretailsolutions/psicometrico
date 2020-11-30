from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class SurveyUser_inputInherit(models.Model):
    _inherit="survey.user_input"
    score = fields.Integer(string='Puntaje')
    recommendation = fields.Char(string='Recomendación')
    
    def corregir(self):
        #Inicializo Variables
        subescalas = []
        puntajes_parciales = []

        #Hago la correción de las respuestas del postulante
        self.corregirPreguntas()

        #Obtengo las SubEscalas presentes en el examen
        subescalas = self.ObtenerSubEscalas()

        #Obtengo los puntajes por cada Subescala
        puntajes_parciales = self.sumarPuntajesPorSubescala(subescalas)

        #Obtener valor de escala a partir del puntaje
        valores_parciales = self.leerTablas(puntajes_parciales)

        #Obtener la interpretación por los valores
        interpretaciones = self.leerInterpretación(valores_parciales)

        #Obtener Valor por Escala
        valor_escala = self.ObtenerValorxEscala(interpretaciones)

        #Recomendación Final
        recomendacion_final = self.recomendacionFinal(valor_escala)
        self.recommendation = recomendacion_final

    def corregirPreguntas(self):
        for pregunta in self.user_input_line_ids:
            if pregunta.value_suggested.correct_answer:
                pregunta.answer_score = 1
                pregunta.answer_state = 'CORRECTO'
            else:
                pregunta.answer_score = 0
                pregunta.answer_state = 'INCORRECTO'

    def ObtenerSubEscalas(self):
        subescalas = []
        for pregunta in self.user_input_line_ids:
            for subscala in pregunta.question_id.subscale:                
                if not (subscala.name in subescalas):
                    subescalas.append(subscala.name)
        return subescalas

    def sumarPuntajesPorSubescala(self, subescalas):
        puntajes_parciales = []
        for subescala in subescalas:
            obj = {}
            puntaje = 0
            for pregunta in self.user_input_line_ids:
                for subscala in pregunta.question_id.subscale:
                    if subscala.name == subescala:
                        puntaje += pregunta.answer_score
            obj = {
                'subescala': subescala,
                'puntaje': puntaje
            }
            puntajes_parciales.append(obj) 
        return puntajes_parciales

    def leerTablas(self, puntajes_parciales):
        valores_procesados=[]
        obj={}
        for subescala in puntajes_parciales:
            valor = 0
            if subescala['subescala'] == 'Hipocondría':
                valor = self.tablaHipocondria(subescala['puntaje'])
            if subescala['subescala'] == 'Depresión':
                valor = self.tablaDepresion(subescala['puntaje'])
            if subescala['subescala'] == 'Histeria de conversión':
                valor = self.tablaHisteria(subescala['puntaje'])
            if subescala['subescala'] == 'Psicopatía':
                valor = self.tablaPsicopatia(subescala['puntaje'])
            if subescala['subescala'] == 'Masculinidad/Feminidad':
                valor = self.tablaMasculinidadFeminidad(subescala['puntaje'])
            if subescala['subescala'] == 'Paranoia':
                valor = self.tablaParanoia(subescala['puntaje'])
            if subescala['subescala'] == '	Psicastenia':
                valor = self.tablaPsicastenia(subescala['puntaje'])
            if subescala['subescala'] == 'Esquizofrenía':
                valor = self.tablaEsquizofrenia(subescala['puntaje'])
            if subescala['subescala'] == 'Hipomanía':
                valor = self.tablaHipomania(subescala['puntaje'])
            if subescala['subescala'] == 'Introversión social':
                valor = self.tablaIntroversion(subescala['puntaje'])
            if subescala['subescala'] == 'Ansiedad':
                valor = self.tablaAnsiedad(subescala['puntaje'])
            if subescala['subescala'] == 'Miedos':
                valor = self.tablaMiedos(subescala['puntaje'])
            if subescala['subescala'] == 'Obsesividad':
                valor = self.tablaObsesividad(subescala['puntaje'])
            if subescala['subescala'] == 'Depresión':
                valor = self.tablaDepresion(subescala['puntaje'])
            if subescala['subescala'] == 'Preocupaciones por la salud':
                valor = self.tablaPreocupaciones(subescala['puntaje'])   
            if subescala['subescala'] == 'Pensamiento extravagante':
                valor = self.tablaExtravagante(subescala['puntaje']) 
            if subescala['subescala'] == 'Hostilidad':
                valor = self.tablaHostilidad(subescala['puntaje']) 
            if subescala['subescala'] == 'Cinismo':
                valor = self.tablaCinismo(subescala['puntaje']) 
            if subescala['subescala'] == 'Conductas antisociales':
                valor = self.tablaAntisocial(subescala['puntaje']) 
            if subescala['subescala'] == 'Comportamiento Tipo A':
                valor = self.tablaComportamientoA(subescala['puntaje']) 
            if subescala['subescala'] == 'Baja Autoestima':
                valor = self.tablaBajaAutoestima(subescala['puntaje']) 
            if subescala['subescala'] == 'Malestar social':
                valor = self.tablaMalestarSocial(subescala['puntaje']) 
            if subescala['subescala'] == 'Problemas familiares':
                valor = self.tablaProblemasFamiliares(subescala['puntaje']) 
            if subescala['subescala'] == 'Interferencia labora':
                valor = self.tablaInterferencia(subescala['puntaje']) 
            if subescala['subescala'] == 'Indicadores negativos de tratamiento':
                valor = self.tablaIndicadores(subescala['puntaje']) 
            if subescala['subescala'] == 'Mentira':
                valor = self.tablaMentira(subescala['puntaje']) 
            if subescala['subescala'] == 'Incoherencia':
                valor = self.tablaIncoherencia(subescala['puntaje'])      
            if subescala['subescala'] == 'Negación':
                valor = self.tablaNegacion(subescala['puntaje'])   
            obj = {
                'subescala': subescala['subescala'],
                'puntaje': subescala['puntaje'],
                'valor': valor
            }   
            valores_procesados.append(obj) 
        return valores_procesados

    def leerInterpretación(self, valores_parciales):
        valores_procesados=[]
        obj={}
        for valor in valores_parciales:
            recomendacion = ''
            if valor['subescala'] == 'Hipocondría':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Depresión':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Histeria de conversión':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Psicopatía':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 75:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Masculinidad/Feminidad':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 75:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Paranoia':
                if valor['valor'] < 35:
                    recomendacion = 'No Recomendable'
                elif valor['valor'] >= 35 and valor['valor'] < 45:
                    recomendacion = 'Recomendable con observaciones'
                elif valor['valor'] >= 45 and valor['valor'] < 50:
                    recomendacion = 'Recomendable'                    
                elif valor['valor'] >= 50 and valor['valor'] < 60:
                    recomendacion = 'Recomendable con observaciones'         
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'No Recomendable'                             
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Psicastenia':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 75:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Esquizofrenía':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 75:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Hipomanía':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'                    
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Introversión social':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 75:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Ansiedad':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable con observaciones'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                    
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Miedos':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable con  observaciones'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                    
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Obsesividad':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable con observaciones'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                        
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Depresión':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable con observaciones'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                           
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Preocupaciones por la salud':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable con observaciones'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                           
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable' 
            if valor['subescala'] == 'Pensamiento extravagante':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Hostilidad':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable con observaciones'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                           
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Cinismo':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                           
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Conductas antisociales':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                           
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Comportamiento Tipo A':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                           
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Baja Autoestima':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                           
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Malestar social':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Problemas familiares':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                           
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Interferencia labora':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                           
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Indicadores negativos de tratamiento':
                if valor['valor'] < 40:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 40 and valor['valor'] < 60:
                    recomendacion = 'Recomendable'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Recomendable'                           
                elif valor['valor'] >= 70 and valor['valor'] < 80:
                    recomendacion = 'Recomendable con observaciones'
                else:
                    recomendacion = 'No recomendable'
            if valor['subescala'] == 'Mentira':
                if valor['valor'] < 50:
                    recomendacion = 'Probablemente válido'
                elif valor['valor'] >= 50 and valor['valor'] < 59:
                    recomendacion = 'Valido'
                elif valor['valor'] >= 59 and valor['valor'] < 70:
                    recomendacion = 'Probablemente válido'
                elif valor['valor'] >= 59 and valor['valor'] < 70:
                    recomendacion = 'Probablemente válido'                    
                else:
                    recomendacion = 'Probablemente inválido' 
            if valor['subescala'] == 'Incoherencia':
                if valor['valor'] < 50:
                    recomendacion = 'Probablemente válido'
                elif valor['valor'] >= 50 and valor['valor'] < 59:
                    recomendacion = 'Valido'
                elif valor['valor'] >= 59 and valor['valor'] < 64:
                    recomendacion = 'Probablemente válido'
                elif valor['valor'] >= 64 and valor['valor'] < 80:
                    recomendacion = 'Probablemente válido'    
                elif valor['valor'] >= 80 and valor['valor'] < 100:
                    recomendacion = 'Perfil inválido'                                          
                else:
                    recomendacion = 'Perfil inválido'     
            if valor['subescala'] == 'Negación':
                if valor['valor'] < 50:
                    recomendacion = 'Perfil inválido'
                elif valor['valor'] >= 50 and valor['valor'] < 60:
                    recomendacion = 'Válido'
                elif valor['valor'] >= 60 and valor['valor'] < 70:
                    recomendacion = 'Validez cuestionable'
                else:
                    recomendacion = 'Perfil válido'                      
            obj={
                'subescala':valor['subescala'],
                'recomendacion': valor
            }
            valores_procesados.append(obj)
        return valores_procesados

    def ObtenerValorxEscala(self, valores):
        recomendaciones=[]
        obj={}
        sumaPrincipales = 0
        contadorPrincipales = 0
        sumaSecundarias = 0
        contadorSecundarias = 0
        sumaValidacion=0
        contadorValidacion = 0
        cerosPrincipal = 0
        cerosSecundarias = 0
        cerosValidacion = 0
        for valor in valores:
            # Principales    
            if valor['subescala']== 'Hipocondría':
                if valor['recomendacion'] == 'Recomendable':
                    sumaPrincipales +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaPrincipales +=1
                else:
                    sumaPrincipales +=0
                    cerosPrincipal += 1
                contadorPrincipales +=1               
            if valor['subescala']== 'Depresión':
                if valor['recomendacion'] == 'Recomendable':
                    sumaPrincipales +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaPrincipales +=1
                else:
                    sumaPrincipales +=0
                    cerosPrincipal += 1
                contadorPrincipales +=1    
            if valor['subescala']== 'Histeria de conversión':
                if valor['recomendacion'] == 'Recomendable':
                    sumaPrincipales +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaPrincipales +=1
                else:
                    sumaPrincipales +=0
                    cerosPrincipal += 1
                contadorPrincipales +=1    
            if valor['subescala']== 'Psicopatía':
                if valor['recomendacion'] == 'Recomendable':
                    sumaPrincipales +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaPrincipales +=1
                else:
                    sumaPrincipales +=0
                    cerosPrincipal += 1
                contadorPrincipales +=1    
            if valor['subescala']== 'Masculinidad/Feminidad':
                if valor['recomendacion'] == 'Recomendable':
                    sumaPrincipales +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaPrincipales +=1
                else:
                    sumaPrincipales +=0
                    cerosPrincipal += 1
                contadorPrincipales +=1    
            if valor['subescala']== 'Paranoia':
                if valor['recomendacion'] == 'Recomendable':
                    sumaPrincipales +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaPrincipales +=1
                else:
                    sumaPrincipales +=0
                    cerosPrincipal += 1
                contadorPrincipales +=1    
            if valor['subescala']== 'Psicastenia':
                if valor['recomendacion'] == 'Recomendable':
                    sumaPrincipales +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaPrincipales +=1
                else:
                    sumaPrincipales +=0
                    cerosPrincipal += 1
                contadorPrincipales +=1    
            if valor['subescala']== 'Esquizofrenía':
                if valor['recomendacion'] == 'Recomendable':
                    sumaPrincipales +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaPrincipales +=1
                else:
                    sumaPrincipales +=0
                    cerosPrincipal += 1
                contadorPrincipales +=1    
            if valor['subescala']== 'Hipomanía':
                if valor['recomendacion'] == 'Recomendable':
                    sumaPrincipales +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaPrincipales +=1
                else:
                    sumaPrincipales +=0
                    cerosPrincipal += 1
                contadorPrincipales +=1    
            if valor['subescala']== 'Introversión social':
                if valor['recomendacion'] == 'Recomendable':
                    sumaPrincipales +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaPrincipales +=1
                else:
                    sumaPrincipales +=0
                    cerosPrincipal += 1
                contadorPrincipales +=1    
            #Secundarias    
            if valor['subescala']== 'Ansiedad':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1    
            if valor['subescala']== 'Miedos':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1    
            if valor['subescala']== 'Obsesividad':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1    
            if valor['subescala']== 'Depresión':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias += 2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias += 1
                else:
                    sumaSecundarias += 0
                    cerosSecundarias += 1
                contadorSecundarias += 1    
            if valor['subescala']== 'Preocupaciones por la salud':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1    
            if valor['subescala']== 'Pensamiento extravagante':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1                       
            if valor['subescala']== 'Hostilidad':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1
            if valor['subescala']== 'Cinismo':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1      
            if valor['subescala']== 'Conductas antisociales':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1   
            if valor['subescala']== 'Comportamiento Tipo A':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1
            if valor['subescala']== 'Baja Autoestima':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1
            if valor['subescala']== 'Malestar social':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1
            if valor['subescala']== 'Problemas familiares':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1
            if valor['subescala']== 'Interferencia labora':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1
            if valor['subescala']== 'Indicadores negativos de tratamiento':
                if valor['recomendacion'] == 'Recomendable':
                    sumaSecundarias +=2
                elif valor['recomendacion'] == 'Recomendable con observaciones':
                    sumaSecundarias +=1
                else:
                    sumaSecundarias +=0
                    cerosSecundarias += 1
                contadorSecundarias +=1
            #Validacion
            if valor['subescala']== 'Mentira':
                if valor['recomendacion'] == 'Válido':
                    sumaValidacion +=4
                elif valor['recomendacion'] == 'Probablemente válido':
                    sumaValidacion +=3
                elif valor['recomendacion'] == 'Validez cuestionable':
                    sumaValidacion +=2              
                elif valor['recomendacion'] == 'Probablemente inválido':
                    sumaValidacion +=1                                    
                else:
                    sumaValidacion +=0 
                    cerosValidacion += 1
                contadorValidacion +=1
            if valor['subescala']== 'Incoherencia':
                if valor['recomendacion'] == 'Válido':
                    sumaValidacion +=4
                elif valor['recomendacion'] == 'Probablemente válido':
                    sumaValidacion +=3
                elif valor['recomendacion'] == 'Validez cuestionable':
                    sumaValidacion +=2              
                elif valor['recomendacion'] == 'Probablemente inválido':
                    sumaValidacion +=1                                    
                else:
                    sumaValidacion +=0   
                    cerosValidacion += 1
                contadorValidacion +=1
            if valor['subescala']== 'Negación':
                if valor['recomendacion'] == 'Válido':
                    sumaValidacion +=4
                elif valor['recomendacion'] == 'Probablemente válido':
                    sumaValidacion +=3
                elif valor['recomendacion'] == 'Validez cuestionable':
                    sumaValidacion +=2              
                elif valor['recomendacion'] == 'Probablemente inválido':
                    sumaValidacion +=1                                    
                else:
                    sumaValidacion +=0
                    cerosValidacion += 1
                contadorValidacion +=1
        obj={
            'Escala': 'Escala Principal',
            'valor': sumaPrincipales
        }
        recomendaciones= [
            {
            'escala': 'Escala Principal',
            'valor': sumaPrincipales/contadorPrincipales if contadorPrincipales > 0 else 0,
            'ceros': cerosPrincipal
            },
            {
            'escala': 'Escala Secundaria',
            'valor': sumaSecundarias/contadorSecundarias if contadorSecundarias > 0 else 0,
            'ceros': cerosSecundarias
            },
            {
            'escala': 'Escala Validacion',
            'valor': sumaValidacion/contadorValidacion if contadorValidacion > 0 else 0,
            'ceros': cerosValidacion
            }                        
        ]
        return recomendaciones

    def recomendacionFinal(self, valor_escala):
        prom = 0
        validacion=0
        principal = 0
        secundaria = 0
        ceros = 0

        for valor in valor_escala:
            if valor['escala'] == 'Escala Validacion':
                if valor['valor'] == 0:
                    validacion = 0
                elif valor['valor'] == 1:
                    validacion = 0
                elif valor.valor == 2:
                    validacion = 1
                elif valor.valor == 3:
                    validacion = 1
                else:
                    validacion = 2
            if valor['escala'] == 'Escala Principal':
                principal = valor['valor']
            if valor['escala'] == 'Escala Secundaria':
                secundaria = valor['valor']
            ceros += valor['ceros']

        prom = (validacion + principal + secundaria)/3
        if ceros >= 1:
            return 'No recomendable'
        elif prom < 1:
            return 'No recomendable'
        elif prom >= 1 and prom < 1.5:
            return 'Recomendable con observaciones'
        else:
            return 'Recomendable'

# Tablas de valores

    def tablaHipocondria(self, puntaje):
        if puntaje == 0:
            return 17
        if puntaje == 1:
            return 20
        if puntaje == 2:
            return 22
        if puntaje == 3:
            return 24
        if puntaje == 4:
            return 26
        if puntaje == 5:
            return 28
        if puntaje == 6:
            return 31
        if puntaje == 7:
            return 33
        if puntaje == 8:
            return 35
        if puntaje == 9:
            return 37
        if puntaje == 10:
            return 40
        if puntaje == 11:
            return 42
        if puntaje == 12:
            return 44
        if puntaje == 13:
            return 46
        if puntaje == 14:
            return 48
        if puntaje == 15:
            return 51
        if puntaje == 16:
            return 53
        if puntaje == 17:
            return 55
        if puntaje == 18:
            return 57
        if puntaje == 19:
            return 60
        if puntaje == 20:
            return 62
        if puntaje == 21:
            return 64
        if puntaje == 22:
            return 66
        if puntaje == 23:
            return 68
        if puntaje == 24:
            return 71
        if puntaje == 25:
            return 73
        if puntaje == 26:
            return 75
        if puntaje == 27:
            return 77
        if puntaje == 28:
            return 80
        if puntaje == 29:
            return 82                                                                                                                                                                                                                                                                                                                                                
        if puntaje == 30:
            return 84
        if puntaje == 31:
            return 86
        if puntaje == 32:
            return 88
        if puntaje == 33:
            return 91
        if puntaje == 34:
            return 93
        if puntaje == 35:
            return 95
        if puntaje == 36:
            return 97
        if puntaje == 37:
            return 99
        if puntaje == 38:
            return 102
        if puntaje == 39:
            return 104
        if puntaje == 40:
            return 106
        if puntaje == 41:
            return 108
        if puntaje == 42:
            return 110
        if puntaje == 43:
            return 113
        if puntaje == 44:
            return 115
        if puntaje == 45:
            return 117
        if puntaje == 46:
            return 119

    def tablaDepresion(self, puntaje):
        if puntaje == 1:
            return 8
        if puntaje == 2:
            return 10
        if puntaje == 3:
            return 12
        if puntaje == 4:
            return 14
        if puntaje == 5:
            return 16
        if puntaje == 6:
            return 18
        if puntaje == 7:
            return 20
        if puntaje == 8:
            return 22
        if puntaje == 9:
            return 24
        if puntaje == 10:
            return 26
        if puntaje == 11:
            return 28
        if puntaje == 12:
            return 30
        if puntaje == 13:
            return 32
        if puntaje == 14:
            return 34
        if puntaje == 15:
            return 36
        if puntaje == 16:
            return 38
        if puntaje == 17:
            return 40
        if puntaje == 18:
            return 42
        if puntaje == 19:
            return 44
        if puntaje == 20:
            return 46
        if puntaje == 21:
            return 48
        if puntaje == 22:
            return 50
        if puntaje == 23:
            return 52
        if puntaje == 24:
            return 54
        if puntaje == 25:
            return 56
        if puntaje == 26:
            return 58
        if puntaje == 27:
            return 60
        if puntaje == 28:
            return 62
        if puntaje == 29:
            return 64                                                                                                                                                                                                                                                                                                                                               
        if puntaje == 30:
            return 66
        if puntaje == 31:
            return 68
        if puntaje == 32:
            return 70
        if puntaje == 33:
            return 72
        if puntaje == 34:
            return 74
        if puntaje == 35:
            return 76
        if puntaje == 36:
            return 78
        if puntaje == 37:
            return 80
        if puntaje == 38:
            return 82
        if puntaje == 39:
            return 84
        if puntaje == 40:
            return 86
        if puntaje == 41:
            return 89
        if puntaje == 42:
            return 91
        if puntaje == 43:
            return 93
        if puntaje == 44:
            return 95
        if puntaje == 45:
            return 97
        if puntaje == 46:
            return 99
        if puntaje == 47:
            return 101
        if puntaje == 48:
            return 103
        if puntaje == 49:
            return 105
        if puntaje == 50:
            return 107
        if puntaje == 51:
            return 109
        if puntaje == 52:
            return 111
        if puntaje == 53:
            return 113
        if puntaje == 54:
            return 115                                                                                    
        if puntaje == 55:
            return 117               
        if puntaje == 56:
            return 119

    def tablaHisteria(self, puntaje):
        if puntaje == 1:
            return 9
        if puntaje == 2:
            return 11
        if puntaje == 3:
            return 13
        if puntaje == 4:
            return 15
        if puntaje == 5:
            return 17
        if puntaje == 6:
            return 19
        if puntaje == 7:
            return 21
        if puntaje == 8:
            return 23
        if puntaje == 9:
            return 25
        if puntaje == 10:
            return 27
        if puntaje == 12:
            return 29
        if puntaje == 13:
            return 31
        if puntaje == 14:
            return 33
        if puntaje == 15:
            return 35
        if puntaje == 16:
            return 37
        if puntaje == 17:
            return 39
        if puntaje == 18:
            return 41
        if puntaje == 19:
            return 43
        if puntaje == 20:
            return 45
        if puntaje == 21:
            return 48
        if puntaje == 22:
            return 50
        if puntaje == 23:
            return 52
        if puntaje == 24:
            return 54
        if puntaje == 25:
            return 56
        if puntaje == 26:
            return 58             
        if puntaje == 27:
            return 60
        if puntaje == 28:
            return 62
        if puntaje == 29:
            return 64
        if puntaje == 30:
            return 66
        if puntaje == 31:
            return 68
        if puntaje == 32:
            return 70
        if puntaje == 33:
            return 72
        if puntaje == 34:
            return 74
        if puntaje == 35:
            return 76
        if puntaje == 36:
            return 78
        if puntaje == 37:
            return 80
        if puntaje == 38:
            return 82
        if puntaje == 39:
            return 84
        if puntaje == 40:
            return 86
        if puntaje == 41:
            return 89
        if puntaje == 42:
            return 91
        if puntaje == 43:
            return 93
        if puntaje == 44:
            return 95
        if puntaje == 45:
            return 97
        if puntaje == 46:
            return 99
        if puntaje == 47:
            return 101
        if puntaje == 48:
            return 103
        if puntaje == 49:
            return 105
        if puntaje == 50:
            return 107
        if puntaje == 51:
            return 109
        if puntaje == 52:
            return 111
        if puntaje == 53:
            return 113
        if puntaje == 54:
            return 115
        if puntaje == 55:
            return 115
        if puntaje == 56:
            return 119

    def tablaPsicopatia(self, puntaje):
        if puntaje == 4:
            return 8
        if puntaje == 5:
            return 10
        if puntaje == 6:
            return 12
        if puntaje == 7:
            return 14
        if puntaje == 8:
            return 16
        if puntaje == 9:
            return 19
        if puntaje == 10:
            return 20
        if puntaje == 12:
            return 22           
        if puntaje == 12:
            return 24
        if puntaje == 13:
            return 27
        if puntaje == 14:
            return 29
        if puntaje == 15:
            return 31
        if puntaje == 16:
            return 33
        if puntaje == 17:
            return 35
        if puntaje == 18:
            return 37
        if puntaje == 19:
            return 39
        if puntaje == 20:
            return 41
        if puntaje == 21:
            return 44
        if puntaje == 22:
            return 46
        if puntaje == 23:
            return 48
        if puntaje == 24:
            return 50
        if puntaje == 25:
            return 52
        if puntaje == 26:
            return 54             
        if puntaje == 27:
            return 56
        if puntaje == 28:
            return 58
        if puntaje == 29:
            return 61
        if puntaje == 30:
            return 63
        if puntaje == 31:
            return 65
        if puntaje == 32:
            return 67
        if puntaje == 33:
            return 69
        if puntaje == 34:
            return 71
        if puntaje == 35:
            return 73
        if puntaje == 36:
            return 76
        if puntaje == 37:
            return 78
        if puntaje == 38:
            return 80
        if puntaje == 39:
            return 82
        if puntaje == 40:
            return 84
        if puntaje == 41:
            return 86
        if puntaje == 42:
            return 88
        if puntaje == 43:
            return 91
        if puntaje == 44:
            return 93
        if puntaje == 45:
            return 95
        if puntaje == 46:
            return 97
        if puntaje == 47:
            return 99
        if puntaje == 48:
            return 101
        if puntaje == 49:
            return 103
        if puntaje == 50:
            return 106
        if puntaje == 51:
            return 108
        if puntaje == 52:
            return 110
        if puntaje == 53:
            return 112
        if puntaje == 54:
            return 114
        if puntaje == 55:
            return 116
        if puntaje == 56:
            return 118
        if puntaje == 57:
            return 120

    def tablaMasculinidadFeminidad(self, puntaje):
        if puntaje == 7:
            return 7
        if puntaje == 8:
            return 9
        if puntaje == 9:
            return 11
        if puntaje == 10:
            return 14
        if puntaje == 12:
            return 18           
        if puntaje == 13:
            return 21
        if puntaje == 14:
            return 23
        if puntaje == 15:
            return 25
        if puntaje == 16:
            return 18
        if puntaje == 17:
            return 30
        if puntaje == 18:
            return 32
        if puntaje == 19:
            return 35
        if puntaje == 20:
            return 37
        if puntaje == 21:
            return 40
        if puntaje == 22:
            return 42
        if puntaje == 23:
            return 44
        if puntaje == 24:
            return 47
        if puntaje == 25:
            return 49
        if puntaje == 26:
            return 51             
        if puntaje == 27:
            return 54
        if puntaje == 28:
            return 56
        if puntaje == 29:
            return 59
        if puntaje == 30:
            return 61
        if puntaje == 31:
            return 63
        if puntaje == 32:
            return 66
        if puntaje == 33:
            return 68
        if puntaje == 34:
            return 70
        if puntaje == 35:
            return 71
        if puntaje == 36:
            return 73
        if puntaje == 38:
            return 75
        if puntaje == 39:
            return 77
        if puntaje == 40:
            return 78
        if puntaje == 41:
            return 80
        if puntaje == 42:
            return 82
        if puntaje == 43:
            return 85
        if puntaje == 44:
            return 87
        if puntaje == 45:
            return 90
        if puntaje == 46:
            return 92
        if puntaje == 47:
            return 94
        if puntaje == 48:
            return 97
        if puntaje == 49:
            return 99
        if puntaje == 50:
            return 101
        if puntaje == 51:
            return 104
        if puntaje == 52:
            return 106
        if puntaje == 53:
            return 109
        if puntaje == 54:
            return 111
        if puntaje == 55:
            return 113
        if puntaje == 56:
            return 116
        if puntaje == 57:
            return 118
 
    def tablaParanoia(self, puntaje):
        if puntaje == 1:
            return 21
        if puntaje == 2:
            return 24
        if puntaje == 3:
            return 27
        if puntaje == 4:
            return 30
        if puntaje == 5:
            return 33
        if puntaje == 6:
            return 36
        if puntaje == 7:
            return 38
        if puntaje == 8:
            return 41
        if puntaje == 9:
            return 44
        if puntaje == 10:
            return 47
        if puntaje == 11:
            return 50
        if puntaje == 12:
            return 53
        if puntaje == 13:
            return 55
        if puntaje == 14:
            return 58
        if puntaje == 15:
            return 61
        if puntaje == 16:
            return 64
        if puntaje == 17:
            return 67
        if puntaje == 18:
            return 70
        if puntaje == 19:
            return 73
        if puntaje == 20:
            return 75
        if puntaje == 21:
            return 78
        if puntaje == 22:
            return 81
        if puntaje == 23:
            return 84
        if puntaje == 24:
            return 87
        if puntaje == 25:
            return 90
        if puntaje == 26:
            return 92
        if puntaje == 27:
            return 95
        if puntaje == 28:
            return 98
        if puntaje == 29:
            return 101                                                                                                                                                                                                                                                                                                                                               
        if puntaje == 30:
            return 104
        if puntaje == 31:
            return 107
        if puntaje == 32:
            return 109
        if puntaje == 33:
            return 112
        if puntaje == 34:
            return 115
        if puntaje == 35:
            return 118

    def tablaPsicastenia(self, puntaje):
        if puntaje == 4:
            return 8
        if puntaje == 5:
            return 9
        if puntaje == 6:
            return 11
        if puntaje == 7:
            return 12
        if puntaje == 8:
            return 14
        if puntaje == 9:
            return 15
        if puntaje == 10:
            return 17
        if puntaje == 11:
            return 19            
        if puntaje == 12:
            return 20   
        if puntaje == 13:
            return 22
        if puntaje == 14:
            return 24
        if puntaje == 15:
            return 25
        if puntaje == 16:
            return 27
        if puntaje == 17:
            return 29
        if puntaje == 18:
            return 30
        if puntaje == 19:
            return 32
        if puntaje == 20:
            return 33
        if puntaje == 21:
            return 35
        if puntaje == 22:
            return 37
        if puntaje == 23:
            return 38
        if puntaje == 24:
            return 40
        if puntaje == 25:
            return 42
        if puntaje == 26:
            return 44             
        if puntaje == 27:
            return 45
        if puntaje == 28:
            return 47
        if puntaje == 29:
            return 49
        if puntaje == 30:
            return 50
        if puntaje == 31:
            return 52
        if puntaje == 32:
            return 53
        if puntaje == 33:
            return 55
        if puntaje == 34:
            return 57
        if puntaje == 35:
            return 59
        if puntaje == 36:
            return 60
        if puntaje == 37:
            return 62
        if puntaje == 38:
            return 64
        if puntaje == 39:
            return 66
        if puntaje == 40:
            return 67
        if puntaje == 41:
            return 69
        if puntaje == 42:
            return 71
        if puntaje == 43:
            return 72
        if puntaje == 44:
            return 74
        if puntaje == 45:
            return 76
        if puntaje == 46:
            return 77
        if puntaje == 47:
            return 79
        if puntaje == 48:
            return 81
        if puntaje == 49:
            return 83
        if puntaje == 50:
            return 84
        if puntaje == 51:
            return 86
        if puntaje == 52:
            return 88
        if puntaje == 53:
            return 89
        if puntaje == 54:
            return 91
        if puntaje == 55:
            return 93
        if puntaje == 56:
            return 94
        if puntaje == 57:
            return 96
        if puntaje == 58:
            return 98
        if puntaje == 59:
            return 99
        if puntaje == 60:
            return 101
        if puntaje == 61:
            return 103
        if puntaje == 62:
            return 105                                                         
        if puntaje == 63:
            return 106
        if puntaje == 64:
            return 108
        if puntaje == 65:
            return 110
        if puntaje == 66:
            return 111
        if puntaje == 67:
            return 113
        if puntaje == 68:
            return 115
        if puntaje == 69:
            return 116
        if puntaje == 70:
            return 118
        if puntaje == 71:
            return 120                                                                                                    

    def tablaEsquizofrenia(self, puntaje):
        if puntaje == 1:
            return 10
        if puntaje == 2:
            return 11
        if puntaje == 3:
            return 13
        if puntaje == 4:
            return 14
        if puntaje == 5:
            return 15
        if puntaje == 6:
            return 17
        if puntaje == 7:
            return 18
        if puntaje == 8:
            return 19
        if puntaje == 9:
            return 21
        if puntaje == 10:
            return 22
        if puntaje == 11:
            return 23
        if puntaje == 12:
            return 25
        if puntaje == 13:
            return 26
        if puntaje == 14:
            return 27
        if puntaje == 15:
            return 29
        if puntaje == 16:
            return 30
        if puntaje == 17:
            return 31
        if puntaje == 18:
            return 33
        if puntaje == 19:
            return 34
        if puntaje == 20:
            return 35
        if puntaje == 21:
            return 36
        if puntaje == 22:
            return 38
        if puntaje == 23:
            return 39
        if puntaje == 24:
            return 40
        if puntaje == 25:
            return 42
        if puntaje == 26:
            return 43
        if puntaje == 27:
            return 44
        if puntaje == 28:
            return 46
        if puntaje == 29:
            return 47                                                                                                                                                                                                                                                                                                                                               
        if puntaje == 30:
            return 48
        if puntaje == 31:
            return 50
        if puntaje == 32:
            return 51
        if puntaje == 33:
            return 52
        if puntaje == 34:
            return 54
        if puntaje == 35:
            return 55       
        if puntaje == 36:
            return 56 
        if puntaje == 37:
            return 57 
        if puntaje == 38:
            return 59 
        if puntaje == 39:
            return 60 
        if puntaje == 40:
            return 61 
        if puntaje == 41:
            return 63 
        if puntaje == 42:
            return 64 
        if puntaje == 43:
            return 65 
        if puntaje == 44:
            return 67 
        if puntaje == 45:
            return 68 
        if puntaje == 46:
            return 69
        if puntaje == 47:
            return 71
        if puntaje == 48:
            return 72
        if puntaje == 49:
            return 73
        if puntaje == 50:
            return 75
        if puntaje == 51:
            return 76
        if puntaje == 52:
            return 77
        if puntaje == 53:
            return 79
        if puntaje == 54:
            return 80
        if puntaje == 55:
            return 81
        if puntaje == 56:
            return 82
        if puntaje == 57:
            return 84
        if puntaje == 58:
            return 85
        if puntaje == 59:
            return 86
        if puntaje == 60:
            return 88
        if puntaje == 61:
            return 89
        if puntaje == 62:
            return 90
        if puntaje == 63:
            return 92
        if puntaje == 64:
            return 93
        if puntaje == 65:
            return 94
        if puntaje == 66:
            return 96
        if puntaje == 67:
            return 97
        if puntaje == 68:
            return 98
        if puntaje == 69:
            return 100
        if puntaje == 70:
            return 101
        if puntaje == 71:
            return 102
        if puntaje == 72:
            return 103
        if puntaje == 73:
            return 105
        if puntaje == 74:
            return 106
        if puntaje == 75:
            return 107
        if puntaje == 76:
            return 109
        if puntaje == 77:
            return 110
        if puntaje == 78:
            return 111
        if puntaje == 79:
            return 113
        if puntaje == 80:
            return 114
        if puntaje == 81:
            return 115
        if puntaje == 82:
            return 117
        if puntaje == 83:
            return 118
        if puntaje == 84:
            return 119

    def tablaHipomania(self, puntaje):
        if puntaje == 2:
            return 8
        if puntaje == 3:
            return 10
        if puntaje == 4:
            return 12
        if puntaje == 5:
            return 15
        if puntaje == 6:
            return 17
        if puntaje == 7:
            return 19
        if puntaje == 8:
            return 22
        if puntaje == 9:
            return 24
        if puntaje == 10:
            return 26
        if puntaje == 11:
            return 29
        if puntaje == 12:
            return 31
        if puntaje == 13:
            return 33
        if puntaje == 14:
            return 36
        if puntaje == 15:
            return 38
        if puntaje == 16:
            return 40
        if puntaje == 17:
            return 43
        if puntaje == 18:
            return 45
        if puntaje == 19:
            return 47
        if puntaje == 20:
            return 50
        if puntaje == 21:
            return 52
        if puntaje == 22:
            return 55
        if puntaje == 23:
            return 57
        if puntaje == 24:
            return 59
        if puntaje == 25:
            return 62
        if puntaje == 26:
            return 64
        if puntaje == 27:
            return 66
        if puntaje == 28:
            return 69
        if puntaje == 29:
            return 71                                                                                                                                                                                                                                                                                                                                               
        if puntaje == 30:
            return 73
        if puntaje == 31:
            return 76
        if puntaje == 32:
            return 78
        if puntaje == 33:
            return 81
        if puntaje == 34:
            return 83
        if puntaje == 35:
            return 85       
        if puntaje == 36:
            return 88 
        if puntaje == 37:
            return 90 
        if puntaje == 38:
            return 92 
        if puntaje == 39:
            return 95 
        if puntaje == 40:
            return 97 
        if puntaje == 41:
            return 99 
        if puntaje == 42:
            return 102 
        if puntaje == 43:
            return 104 
        if puntaje == 44:
            return 105
        if puntaje == 45:
            return 107
        if puntaje == 46:
            return 109
        if puntaje == 47:
            return 112
        if puntaje == 48:
            return 114
    
    def tablaIntroversion(self, puntaje):
        if puntaje == 1:
            return 19
        if puntaje == 2:
            return 20
        if puntaje == 3:
            return 22
        if puntaje == 4:
            return 23
        if puntaje == 5:
            return 24
        if puntaje == 6:
            return 25
        if puntaje == 7:
            return 26
        if puntaje == 8:
            return 27
        if puntaje == 9:
            return 29
        if puntaje == 10:
            return 30
        if puntaje == 11:
            return 31
        if puntaje == 12:
            return 32
        if puntaje == 13:
            return 33
        if puntaje == 14:
            return 34
        if puntaje == 15:
            return 35
        if puntaje == 16:
            return 37
        if puntaje == 17:
            return 38
        if puntaje == 18:
            return 39
        if puntaje == 19:
            return 40
        if puntaje == 20:
            return 41
        if puntaje == 21:
            return 42
        if puntaje == 22:
            return 43
        if puntaje == 23:
            return 45
        if puntaje == 24:
            return 46
        if puntaje == 25:
            return 47
        if puntaje == 26:
            return 48
        if puntaje == 27:
            return 49
        if puntaje == 28:
            return 50
        if puntaje == 29:
            return 52                                                                                                                                                                                                                                                                                                                                               
        if puntaje == 30:
            return 53
        if puntaje == 31:
            return 54
        if puntaje == 32:
            return 55
        if puntaje == 33:
            return 56
        if puntaje == 34:
            return 57
        if puntaje == 35:
            return 58       
        if puntaje == 36:
            return 60 
        if puntaje == 37:
            return 61 
        if puntaje == 38:
            return 62 
        if puntaje == 39:
            return 63 
        if puntaje == 40:
            return 64 
        if puntaje == 41:
            return 65 
        if puntaje == 42:
            return 67 
        if puntaje == 43:
            return 68
        if puntaje == 44:
            return 69
        if puntaje == 45:
            return 70
        if puntaje == 46:
            return 71
        if puntaje == 47:
            return 72
        if puntaje == 48:
            return 73
        if puntaje == 49:
            return 75
        if puntaje == 50:
            return 76
        if puntaje == 51:
            return 77
        if puntaje == 52:
            return 78
        if puntaje == 53:
            return 79
        if puntaje == 54:
            return 80
        if puntaje == 55:
            return 82
        if puntaje == 56:
            return 83
        if puntaje == 57:
            return 84
        if puntaje == 58:
            return 85
        if puntaje == 59:
            return 86
        if puntaje == 60:
            return 87
        if puntaje == 61:
            return 88
        if puntaje == 62:
            return 90
        if puntaje == 63:
            return 91
        if puntaje == 64:
            return 92
        if puntaje == 65:
            return 93
        if puntaje == 66:
            return 94
        if puntaje == 67:
            return 95
        if puntaje == 68:
            return 97
        if puntaje == 69:
            return 98                                                                                                                                                                                                  
        if puntaje == 0:
            return 17
        if puntaje == 1:
            return 20
        if puntaje == 2:
            return 22
        if puntaje == 3:
            return 24
        if puntaje == 4:
            return 26
        if puntaje == 5:
            return 28
        if puntaje == 6:
            return 31
        if puntaje == 7:
            return 33
        if puntaje == 8:
            return 35
        if puntaje == 9:
            return 37
        if puntaje == 10:
            return 40
        if puntaje == 11:
            return 42
        if puntaje == 12:
            return 44
        if puntaje == 13:
            return 46
        if puntaje == 14:
            return 48
        if puntaje == 15:
            return 51
        if puntaje == 16:
            return 53
        if puntaje == 17:
            return 55
        if puntaje == 18:
            return 57
        if puntaje == 19:
            return 60
        if puntaje == 20:
            return 62
        if puntaje == 21:
            return 64
        if puntaje == 22:
            return 66
        if puntaje == 23:
            return 68
        if puntaje == 24:
            return 71
        if puntaje == 25:
            return 73
        if puntaje == 26:
            return 75
        if puntaje == 27:
            return 77
        if puntaje == 28:
            return 80
        if puntaje == 29:
            return 82                                                                                                                                                                                                                                                                                                                                                
        if puntaje == 30:
            return 84
        if puntaje == 31:
            return 86
        if puntaje == 32:
            return 88
        if puntaje == 33:
            return 91
        if puntaje == 34:
            return 93
        if puntaje == 35:
            return 95
        if puntaje == 36:
            return 97
        if puntaje == 37:
            return 99
        if puntaje == 38:
            return 102
        if puntaje == 39:
            return 104
        if puntaje == 40:
            return 106
        if puntaje == 41:
            return 108
        if puntaje == 42:
            return 110
        if puntaje == 43:
            return 113
        if puntaje == 44:
            return 115
        if puntaje == 45:
            return 117
        if puntaje == 46:
            return 119

    def tablaAnsiedad(self, puntaje):
        if puntaje == 0:
            return 32
        if puntaje == 1:
            return 35
        if puntaje == 2:
            return 37
        if puntaje == 3:
            return 39
        if puntaje == 4:
            return 41
        if puntaje == 5:
            return 43
        if puntaje == 6:
            return 45
        if puntaje == 7:
            return 47
        if puntaje == 8:
            return 50
        if puntaje == 9:
            return 52
        if puntaje == 10:
            return 54
        if puntaje == 11:
            return 56
        if puntaje == 12:
            return 58
        if puntaje == 13:
            return 60
        if puntaje == 14:
            return 62
        if puntaje == 15:
            return 65
        if puntaje == 16:
            return 67
        if puntaje == 17:
            return 69
        if puntaje == 18:
            return 71
        if puntaje == 19:
            return 73
        if puntaje == 20:
            return 75
        if puntaje == 21:
            return 77
        if puntaje == 22:
            return 80
        if puntaje == 23:
            return 82
        if puntaje == 24:
            return 84
        if puntaje == 25:
            return 86
        if puntaje == 26:
            return 88

    def tablaMiedos(self, puntaje):
        if puntaje == 0:
            return 32
        if puntaje == 1:
            return 35
        if puntaje == 2:
            return 37
        if puntaje == 3:
            return 39
        if puntaje == 4:
            return 41
        if puntaje == 5:
            return 43
        if puntaje == 6:
            return 45
        if puntaje == 7:
            return 47
        if puntaje == 8:
            return 50
        if puntaje == 9:
            return 52
        if puntaje == 10:
            return 54
        if puntaje == 11:
            return 56
        if puntaje == 12:
            return 58
        if puntaje == 13:
            return 60
        if puntaje == 14:
            return 62
        if puntaje == 15:
            return 65
        if puntaje == 16:
            return 67
        if puntaje == 17:
            return 69
        if puntaje == 18:
            return 71
        if puntaje == 19:
            return 73
        if puntaje == 20:
            return 75
        if puntaje == 21:
            return 77
        if puntaje == 22:
            return 80
        if puntaje == 23:
            return 82

    def tablaObsesividad(self, puntaje):
        if puntaje == 0:
            return 33
        if puntaje == 1:
            return 36
        if puntaje == 2:
            return 39
        if puntaje == 3:
            return 42
        if puntaje == 4:
            return 44
        if puntaje == 5:
            return 47
        if puntaje == 6:
            return 50
        if puntaje == 7:
            return 53
        if puntaje == 8:
            return 56
        if puntaje == 9:
            return 58
        if puntaje == 10:
            return 61
        if puntaje == 11:
            return 64
        if puntaje == 12:
            return 67
        if puntaje == 13:
            return 69
        if puntaje == 14:
            return 72
        if puntaje == 15:
            return 75
        if puntaje == 16:
            return 78
        if puntaje == 17:
            return 81
        if puntaje == 18:
            return 84
        if puntaje == 19:
            return 87
        if puntaje == 20:
            return 90
        if puntaje == 21:
            return 93
        if puntaje == 22:
            return 96
    
    def tablaDepresion(self, puntaje):
        if puntaje == 0:
            return 35
        if puntaje == 1:
            return 36
        if puntaje == 2:
            return 38
        if puntaje == 3:
            return 40
        if puntaje == 4:
            return 42
        if puntaje == 5:
            return 44
        if puntaje == 6:
            return 46
        if puntaje == 7:
            return 48
        if puntaje == 8:
            return 50
        if puntaje == 9:
            return 52
        if puntaje == 10:
            return 53
        if puntaje == 11:
            return 55
        if puntaje == 12:
            return 57
        if puntaje == 13:
            return 59
        if puntaje == 14:
            return 61
        if puntaje == 15:
            return 63
        if puntaje == 16:
            return 65
        if puntaje == 17:
            return 67
        if puntaje == 18:
            return 68
        if puntaje == 19:
            return 70
        if puntaje == 20:
            return 72
        if puntaje == 21:
            return 74
        if puntaje == 22:
            return 76
        if puntaje == 23:
            return 78
        if puntaje == 24:
            return 80
        if puntaje == 25:
            return 82
        if puntaje == 26:
            return 83
        if puntaje == 27:
            return 85
        if puntaje == 28:
            return 87
        if puntaje == 29:
            return 89
        if puntaje == 30:
            return 91
        if puntaje == 31:
            return 93
        if puntaje == 32:
            return 95
        if puntaje == 33:
            return 97                                                                                                            
 
    def tablaPreocupaciones(self, puntaje):
        if puntaje == 0:
            return 35
        if puntaje == 1:
            return 37
        if puntaje == 2:
            return 39
        if puntaje == 3:
            return 41
        if puntaje == 4:
            return 42
        if puntaje == 5:
            return 44
        if puntaje == 6:
            return 46
        if puntaje == 7:
            return 48
        if puntaje == 8:
            return 50
        if puntaje == 9:
            return 52
        if puntaje == 10:
            return 54
        if puntaje == 11:
            return 56
        if puntaje == 12:
            return 58
        if puntaje == 13:
            return 60
        if puntaje == 14:
            return 62
        if puntaje == 15:
            return 64
        if puntaje == 16:
            return 66
        if puntaje == 17:
            return 68
        if puntaje == 18:
            return 70
        if puntaje == 19:
            return 72
        if puntaje == 20:
            return 74
        if puntaje == 21:
            return 76
        if puntaje == 22:
            return 78
        if puntaje == 23:
            return 80
        if puntaje == 24:
            return 82
        if puntaje == 25:
            return 84
        if puntaje == 26:
            return 86
        if puntaje == 27:
            return 88
        if puntaje == 28:
            return 90
        if puntaje == 29:
            return 92
        if puntaje == 30:
            return 94
        if puntaje == 31:
            return 96
        if puntaje == 32:
            return 98
        if puntaje == 33:
            return 100   
        if puntaje == 34:
            return 102
        if puntaje == 35:
            return 104
        if puntaje == 36:
            return 106

    def tablaExtravagante(self, puntaje):
        if puntaje == 0:
            return 39
        if puntaje == 1:
            return 42
        if puntaje == 2:
            return 45
        if puntaje == 3:
            return 48
        if puntaje == 4:
            return 51
        if puntaje == 5:
            return 54
        if puntaje == 6:
            return 57
        if puntaje == 7:
            return 60
        if puntaje == 8:
            return 63
        if puntaje == 9:
            return 66
        if puntaje == 10:
            return 69
        if puntaje == 11:
            return 72
        if puntaje == 12:
            return 75
        if puntaje == 13:
            return 78
        if puntaje == 14:
            return 81
        if puntaje == 15:
            return 84
        if puntaje == 16:
            return 87
        if puntaje == 17:
            return 90
        if puntaje == 18:
            return 92
        if puntaje == 19:
            return 95
        if puntaje == 20:
            return 98
        if puntaje == 21:
            return 102
        if puntaje == 22:
            return 104
        if puntaje == 23:
            return 107

    def tablaHostilidad(self, puntaje):
        if puntaje == 0:
            return 39
        if puntaje == 1:
            return 42
        if puntaje == 2:
            return 45
        if puntaje == 3:
            return 48
        if puntaje == 4:
            return 51
        if puntaje == 5:
            return 54
        if puntaje == 6:
            return 57
        if puntaje == 7:
            return 60
        if puntaje == 8:
            return 63
        if puntaje == 9:
            return 66
        if puntaje == 10:
            return 69
        if puntaje == 11:
            return 72
        if puntaje == 12:
            return 75
        if puntaje == 13:
            return 78
        if puntaje == 14:
            return 81
        if puntaje == 15:
            return 84
        if puntaje == 16:
            return 87
        if puntaje == 17:
            return 90
        if puntaje == 18:
            return 92
        if puntaje == 19:
            return 95
        if puntaje == 20:
            return 98
        if puntaje == 21:
            return 102
        if puntaje == 22:
            return 104
        if puntaje == 23:
            return 107

    def tablaCinismo(self, puntaje):
        if puntaje == 0:
            return 29
        if puntaje == 1:
            return 31
        if puntaje == 2:
            return 33
        if puntaje == 3:
            return 35
        if puntaje == 4:
            return 37
        if puntaje == 5:
            return 39
        if puntaje == 6:
            return 41
        if puntaje == 7:
            return 43
        if puntaje == 8:
            return 45
        if puntaje == 9:
            return 47
        if puntaje == 10:
            return 48
        if puntaje == 11:
            return 50
        if puntaje == 12:
            return 52
        if puntaje == 13:
            return 54
        if puntaje == 14:
            return 56
        if puntaje == 15:
            return 58
        if puntaje == 16:
            return 60
        if puntaje == 17:
            return 62
        if puntaje == 18:
            return 64
        if puntaje == 19:
            return 66
        if puntaje == 20:
            return 67
        if puntaje == 21:
            return 69
        if puntaje == 22:
            return 71
        if puntaje == 23:
            return 73
        if puntaje == 24:
            return 75
        if puntaje == 25:
            return 77
        if puntaje == 26:
            return 79
        if puntaje == 27:
            return 81
        if puntaje == 28:
            return 83
        if puntaje == 29:
            return 85
        if puntaje == 30:
            return 86

    def tablaAntisocial(self, puntaje):
        if puntaje == 0:
            return 26
        if puntaje == 1:
            return 29
        if puntaje == 2:
            return 31
        if puntaje == 3:
            return 33
        if puntaje == 4:
            return 36
        if puntaje == 5:
            return 38
        if puntaje == 6:
            return 41
        if puntaje == 7:
            return 43
        if puntaje == 8:
            return 46
        if puntaje == 9:
            return 48
        if puntaje == 10:
            return 50
        if puntaje == 11:
            return 53
        if puntaje == 12:
            return 55
        if puntaje == 13:
            return 58
        if puntaje == 14:
            return 60
        if puntaje == 15:
            return 63
        if puntaje == 16:
            return 65
        if puntaje == 17:
            return 68
        if puntaje == 18:
            return 70
        if puntaje == 19:
            return 72
        if puntaje == 20:
            return 75
        if puntaje == 21:
            return 77
        if puntaje == 22:
            return 80
        if puntaje == 23:
            return 82
        if puntaje == 24:
            return 84
        if puntaje == 25:
            return 87
        if puntaje == 26:
            return 89

    def tablaComportamientoA(self, puntaje):
        if puntaje == 0:
            return 26
        if puntaje == 1:
            return 29
        if puntaje == 2:
            return 32
        if puntaje == 3:
            return 35
        if puntaje == 4:
            return 35
        if puntaje == 5:
            return 38
        if puntaje == 6:
            return 41
        if puntaje == 7:
            return 44
        if puntaje == 8:
            return 47
        if puntaje == 9:
            return 49
        if puntaje == 10:
            return 52
        if puntaje == 11:
            return 55
        if puntaje == 12:
            return 58
        if puntaje == 13:
            return 61
        if puntaje == 14:
            return 64
        if puntaje == 15:
            return 67
        if puntaje == 16:
            return 70
        if puntaje == 17:
            return 73
        if puntaje == 18:
            return 76
        if puntaje == 19:
            return 79
        if puntaje == 20:
            return 82
        if puntaje == 21:
            return 85
        if puntaje == 22:
            return 88

    def tablaBajaAutoestima(self, puntaje):
        if puntaje == 0:
            return 33
        if puntaje == 1:
            return 35
        if puntaje == 2:
            return 38
        if puntaje == 3:
            return 40
        if puntaje == 4:
            return 43
        if puntaje == 5:
            return 45
        if puntaje == 6:
            return 48
        if puntaje == 7:
            return 50
        if puntaje == 8:
            return 53
        if puntaje == 9:
            return 55
        if puntaje == 10:
            return 58
        if puntaje == 11:
            return 60
        if puntaje == 12:
            return 63
        if puntaje == 13:
            return 65
        if puntaje == 14:
            return 68
        if puntaje == 15:
            return 70
        if puntaje == 16:
            return 72
        if puntaje == 17:
            return 75
        if puntaje == 18:
            return 77
        if puntaje == 19:
            return 80
        if puntaje == 20:
            return 82
        if puntaje == 21:
            return 85
        if puntaje == 22:
            return 87
        if puntaje == 23:
            return 90
        if puntaje == 24:
            return 92

    def tablaMalestarSocial(self,puntaje):
        if puntaje == 0:
            return 33
        if puntaje == 1:
            return 35
        if puntaje == 2:
            return 38
        if puntaje == 3:
            return 40
        if puntaje == 4:
            return 43
        if puntaje == 5:
            return 45
        if puntaje == 6:
            return 48
        if puntaje == 7:
            return 50
        if puntaje == 8:
            return 53
        if puntaje == 9:
            return 55
        if puntaje == 10:
            return 58
        if puntaje == 11:
            return 60
        if puntaje == 12:
            return 63
        if puntaje == 13:
            return 65
        if puntaje == 14:
            return 68
        if puntaje == 15:
            return 70
        if puntaje == 16:
            return 72
        if puntaje == 17:
            return 75
        if puntaje == 18:
            return 77
        if puntaje == 19:
            return 80
        if puntaje == 20:
            return 82
        if puntaje == 21:
            return 85
        if puntaje == 22:
            return 87
        if puntaje == 23:
            return 90
        if puntaje == 24:
            return 92

    def tablaProblemasFamiliares(self, puntaje):
        if puntaje == 0:
            return 35
        if puntaje == 1:
            return 38
        if puntaje == 2:
            return 40
        if puntaje == 3:
            return 43
        if puntaje == 4:
            return 45
        if puntaje == 5:
            return 47
        if puntaje == 6:
            return 50
        if puntaje == 7:
            return 52
        if puntaje == 8:
            return 55
        if puntaje == 9:
            return 57
        if puntaje == 10:
            return 59
        if puntaje == 11:
            return 62
        if puntaje == 12:
            return 64
        if puntaje == 13:
            return 67
        if puntaje == 14:
            return 69
        if puntaje == 15:
            return 71
        if puntaje == 16:
            return 74
        if puntaje == 17:
            return 76
        if puntaje == 18:
            return 79
        if puntaje == 19:
            return 81
        if puntaje == 20:
            return 83
        if puntaje == 21:
            return 86
        if puntaje == 22:
            return 88
        if puntaje == 23:
            return 90
        if puntaje == 24:
            return 93
        if puntaje == 25:
            return 95
        if puntaje == 26:
            return 98
        if puntaje == 28:
            return 100
        if puntaje == 29:
            return 103
        if puntaje == 30:
            return 105
        if puntaje == 31:
            return 107
        if puntaje == 32:
            return 110
        if puntaje == 33:
            return 112
        if puntaje == 34:
            return 115
        if puntaje == 35:
            return 117
        if puntaje == 36:
            return 119
                                                                                                       
    def tablaInterferencia(self, puntaje):
        if puntaje == 0:
            return 34
        if puntaje == 1:
            return 36
        if puntaje == 2:
            return 37
        if puntaje == 3:
            return 39
        if puntaje == 4:
            return 41
        if puntaje == 5:
            return 42
        if puntaje == 6:
            return 44
        if puntaje == 7:
            return 46
        if puntaje == 8:
            return 47
        if puntaje == 9:
            return 49
        if puntaje == 10:
            return 51
        if puntaje == 11:
            return 52
        if puntaje == 12:
            return 54
        if puntaje == 13:
            return 56
        if puntaje == 14:
            return 57
        if puntaje == 15:
            return 59
        if puntaje == 16:
            return 61
        if puntaje == 17:
            return 62
        if puntaje == 18:
            return 64
        if puntaje == 19:
            return 66
        if puntaje == 20:
            return 67
        if puntaje == 21:
            return 69
        if puntaje == 22:
            return 71
        if puntaje == 23:
            return 72
        if puntaje == 24:
            return 74
        if puntaje == 25:
            return 76
        if puntaje == 26:
            return 77
        if puntaje == 28:
            return 81
        if puntaje == 29:
            return 82
        if puntaje == 30:
            return 84
        if puntaje == 31:
            return 86
        if puntaje == 32:
            return 87
        if puntaje == 33:
            return 89

    def tablaIndicadores(self, puntaje):
        if puntaje == 0:
            return 34
        if puntaje == 1:
            return 36
        if puntaje == 2:
            return 39
        if puntaje == 3:
            return 41
        if puntaje == 4:
            return 43
        if puntaje == 5:
            return 45
        if puntaje == 6:
            return 47
        if puntaje == 7:
            return 49
        if puntaje == 8:
            return 51
        if puntaje == 9:
            return 53
        if puntaje == 10:
            return 55
        if puntaje == 11:
            return 57
        if puntaje == 12:
            return 59
        if puntaje == 13:
            return 61
        if puntaje == 14:
            return 63
        if puntaje == 15:
            return 66
        if puntaje == 16:
            return 68
        if puntaje == 17:
            return 70
        if puntaje == 18:
            return 72
        if puntaje == 19:
            return 74
        if puntaje == 20:
            return 76
        if puntaje == 21:
            return 78
        if puntaje == 22:
            return 80
        if puntaje == 23:
            return 82
        if puntaje == 24:
            return 84
        if puntaje == 25:
            return 86
        if puntaje == 26:
            return 88
        if puntaje == 27:
            return 90
        if puntaje == 28:
            return 93            
        if puntaje == 29:
            return 95
        if puntaje == 30:
            return 97
        if puntaje == 31:
            return 99
        if puntaje == 32:
            return 101
        if puntaje == 33:
            return 103
        if puntaje == 34:
            return 105
        if puntaje == 35:
            return 107
        if puntaje == 36:
            return 109
        if puntaje == 37:
            return 111
        if puntaje == 38:
            return 113
        if puntaje == 39:
            return 115
        if puntaje == 40:
            return 118
        if puntaje == 41:
            return 120                                                                       

    def tablaMentira(self, puntaje):
        if puntaje == 0:
            return 30
        if puntaje == 1:
            return 35
        if puntaje == 2:
            return 39
        if puntaje == 3:
            return 43
        if puntaje == 4:
            return 47
        if puntaje == 5:
            return 52
        if puntaje == 6:
            return 55
        if puntaje == 7:
            return 59
        if puntaje == 8:
            return 63
        if puntaje == 9:
            return 67
        if puntaje == 10:
            return 71
        if puntaje == 11:
            return 75
        if puntaje == 12:
            return 79
        if puntaje == 13:
            return 83
        if puntaje == 14:
            return 88
        if puntaje == 15:
            return 92
        if puntaje == 16:
            return 96
        if puntaje == 17:
            return 100
        if puntaje == 18:
            return 104
        if puntaje == 19:
            return 108
        if puntaje == 20:
            return 112

    def tablaIncoherencia(self, puntaje):
        if puntaje == 0:
            return 36
        if puntaje == 1:
            return 38
        if puntaje == 2:
            return 40
        if puntaje == 3:
            return 42
        if puntaje == 4:
            return 43
        if puntaje == 5:
            return 45
        if puntaje == 6:
            return 47
        if puntaje == 7:
            return 49
        if puntaje == 8:
            return 51
        if puntaje == 9:
            return 52
        if puntaje == 10:
            return 54
        if puntaje == 11:
            return 56
        if puntaje == 12:
            return 58
        if puntaje == 13:
            return 59
        if puntaje == 14:
            return 61
        if puntaje == 15:
            return 63
        if puntaje == 16:
            return 65
        if puntaje == 17:
            return 67
        if puntaje == 18:
            return 68
        if puntaje == 19:
            return 70
        if puntaje == 20:
            return 72
        if puntaje == 21:
            return 74
        if puntaje == 22:
            return 76
        if puntaje == 23:
            return 77
        if puntaje == 24:
            return 79
        if puntaje == 25:
            return 81
        if puntaje == 26:
            return 83
        if puntaje == 27:
            return 85
        if puntaje == 28:
            return 86         
        if puntaje == 29:
            return 88
        if puntaje == 30:
            return 90
        if puntaje == 31:
            return 92
        if puntaje == 32:
            return 93
        if puntaje == 33:
            return 95
        if puntaje == 34:
            return 97
        if puntaje == 35:
            return 99
        if puntaje == 36:
            return 101
        if puntaje == 37:
            return 102
        if puntaje == 38:
            return 104
        if puntaje == 39:
            return 106
        if puntaje == 40:
            return 108
        if puntaje == 41:
            return 110
        if puntaje == 42:
            return 111  
        if puntaje == 43:
            return 113
        if puntaje == 44:
            return 115
        if puntaje == 45:
            return 117
        if puntaje == 46:
            return 119
        if puntaje == 47:
            return 120   

    def tablaNegacion(self, puntaje):
        if puntaje == 0:
            return 18
        if puntaje == 1:
            return 21
        if puntaje == 2:
            return 23
        if puntaje == 3:
            return 25
        if puntaje == 4:
            return 27
        if puntaje == 5:
            return 29
        if puntaje == 6:
            return 31
        if puntaje == 7:
            return 33
        if puntaje == 8:
            return 36
        if puntaje == 9:
            return 38
        if puntaje == 10:
            return 40
        if puntaje == 11:
            return 42
        if puntaje == 12:
            return 46
        if puntaje == 13:
            return 46
        if puntaje == 14:
            return 48
        if puntaje == 15:
            return 51
        if puntaje == 16:
            return 53
        if puntaje == 17:
            return 55
        if puntaje == 18:
            return 57
        if puntaje == 19:
            return 59
        if puntaje == 20:
            return 61
        if puntaje == 21:
            return 63
        if puntaje == 22:
            return 66
        if puntaje == 23:
            return 68
        if puntaje == 24:
            return 70
        if puntaje == 25:
            return 72
        if puntaje == 26:
            return 74
        if puntaje == 27:
            return 76
        if puntaje == 28:
            return 78         
        if puntaje == 29:
            return 81
        if puntaje == 30:
            return 83
        if puntaje == 31:
            return 85
        if puntaje == 32:
            return 87
        if puntaje == 33:
            return 89
        if puntaje == 34:
            return 91
        if puntaje == 35:
            return 93
        if puntaje == 36:
            return 95
        if puntaje == 37:
            return 98
        if puntaje == 38:
            return 100
        if puntaje == 39:
            return 102
        if puntaje == 40:
            return 104
        if puntaje == 41:
            return 106
        if puntaje == 42:
            return 108  
        if puntaje == 43:
            return 110
        if puntaje == 44:
            return 113
        if puntaje == 45:
            return 115
        if puntaje == 46:
            return 117
        if puntaje == 47:
            return 119   

    
class SurveyUser_inputLineInherit(models.Model):
    _inherit="survey.user_input_line"
    answer_state = fields.Char(string='Estado')
    