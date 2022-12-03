from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class VideoRatingForm(FlaskForm):

    expression_of_thought = SelectField('Выражение мысли',
                            choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                     (9, '9'), (10, '10')])
    integrity = SelectField('Единство передачи',
                            choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                     (9, '9'), (10, '10')])
    personalized_character = SelectField('Персонифицированный подход',
                            choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                     (9, '9'), (10, '10')])
    artistic_techniques = SelectField('Художественные приемы',
                            choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                     (9, '9'), (10, '10')])
    operators_work = SelectField('Работа оператора',
                            choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                     (9, '9'), (10, '10')])
    promotional_materials = SelectField('Рекламные материалы',
                            choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                     (9, '9'), (10, '10')])
    journalistic_stamps = SelectField('Журналистские штампы',
                            choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                     (9, '9'), (10, '10')])
    сustom_nature = SelectField('Заказной харатер',
                            choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                     (9, '9'), (10, '10')])
    grammatical_errors = SelectField('Грамматические ошибки',
                            choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                     (9, '9'), (10, '10')])
    orthoepic_norms = SelectField('Орфоэпические и лексические нормы',
                            choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                     (9, '9'), (10, '10')])
    @property
    def get_text_rating(self):
        return {
            "relevance": self.relevance.data,
            "integrity": self.integrity.data,
            "validity": self.validity.data,
            "resonance": self.resonance.data,
            "accuracy": self.accuracy.data,
            "ethnicity": self.ethnicity.data,
            "availability": self.availability.data,
            "materials cycle": self.materials_cycle.data
        }
    @property
    def get_video_rating(self):
        return {
            "expression_of_thought": self.expression_of_thought.data,
            "integrity": self.integrity.data,
            "personalized_character": self.personalized_character.data,
            "artistic_techniques": self.artistic_techniques.data,
            "operators_work": self.operators_work.data,
        }
    @property
    def get_lowering_rating(self):
        return {
            "promotional materials": self.promotional_materials.data,
            "journalistic stamps": self.journalistic_stamps.data,
            "сustom_nature": self.сustom_nature.data,
            "grammatical_errors": self.grammatical_errors.data,
            "orthoepic_norms": self.orthoepic_norms.data
        }
    submit = SubmitField('Завершить проверку')