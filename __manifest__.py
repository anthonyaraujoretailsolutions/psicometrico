{ 'name': "psicometric_test",

    'summary': """Test Psicométricos""",

    'description': """
        Módulo para realizar el test Psicométrico
    """,

    'author': "Luis Enrique Alva Villena",
    'website': "https://digilab.pe",
    'qweb': [],

    'category': 'Uncategorized',
    'version': '0.1.0.4',
    'depends': ['survey'],
    # always loaded
    'data': [
        'data/scales.xml',
        'data/questions.xml',
        'data/answers.xml',        
        'security/ir.model.access.csv',
        'views/menu_items.xml',
        'views/survey_views.xml',
        'reports/report.xml',
        'reports/report_test.xml',
        ]
}
