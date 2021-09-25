from django.core.exceptions import ValidationError 

def validate_score(value):
    if (value > 5) | (value < 1 ):
        msg = "평점은 1 이상 5 이하로 매겨주세요."
        raise ValidationError(msg)