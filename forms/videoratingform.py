from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class VideoRatingForm(FlaskForm):

    expression_of_thought = SelectField('Выражение мысли',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    integrity = SelectField('Единство передачи',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    personalized_character = SelectField('Персонифицированный подход',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    artistic_techniques = SelectField('Художественные приемы',
                            choices=[(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                      (9, 9), (10, 10)])
    operators_work = SelectField('Работа оператора',
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
    def get_video_rating(self):
        return {
            "expression_of_thought": int(self.expression_of_thought.data),
            "integrity": int(self.integrity.data),
            "personalized_character": int(self.personalized_character.data),
            "artistic_techniques": int(self.artistic_techniques.data),
            "operators_work": int(self.operators_work.data)
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