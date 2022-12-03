from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class TextRatingForm(FlaskForm):

    relevance = SelectField('Актуальность',
                            choices= [(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    integrity = SelectField('Цельность',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    validity = SelectField('Аргументированность',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    resonance = SelectField('Резонансность',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    accuracy = SelectField('Точность и доходчивость',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    ethnicity = SelectField('Профессионально-этический подход',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    availability = SelectField('Доступность',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    materials_cycle = SelectField('Цикл материалов',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    promotional_materials = SelectField('Рекламные материалы',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    journalistic_stamps = SelectField('Журналистские штампы',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    сustom_nature = SelectField('Заказной харатер',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    grammatical_errors = SelectField('Грамматические ошибки',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    orthoepic_norms = SelectField('Орфоэпические и лексические нормы',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    @property
    def get_text_rating(self):
        return {
            "relevance": int(self.relevance.data),
            "integrity": int(self.integrity.data),
            "validity": int(self.validity.data),
            "resonance": int(self.resonance.data),
            "accuracy": int(self.accuracy.data),
            "ethnicity": int(self.ethnicity.data),
            "availability": int(self.availability.data),
            "materials cycle": int(self.materials_cycle.data)
        }
    @property
    def get_lowering_rating(self):
        return {
            "promotional materials": int(self.promotional_materials.data),
            "journalistic stamps": int(self.journalistic_stamps.data),
            "сustom_nature": int(self.сustom_nature.data),
            "grammatical_errors": int(self.grammatical_errors.data),
            "orthoepic_norms": int(self.orthoepic_norms.data)
        }
    submit = SubmitField('Завершить проверку')