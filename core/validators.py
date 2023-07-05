from jsonschema.exceptions import ValidationError


class AgeValidator:
    def __init__(self, min_reg_age):
        self.today = datetime.date.today()
        self.min_reg_age = min_reg_age
    def __call__(self, value):
        age = (self.today.year - value.year - 1) + ((self.today.month, self.today.day) >= (value.month, value.day))
        if age <= self.min_reg_age:
            raise ValidationError(f'ваш возраст {age} слишком мал для регистрации!')
