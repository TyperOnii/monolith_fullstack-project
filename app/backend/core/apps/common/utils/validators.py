from django.core.exceptions import ValidationError


def validate_size_image(file_obj):
    """Валидация размера изображения"""
    megabite_limit = 5

    if file_obj.size > megabite_limit * 1024 * 1024:
        raise ValidationError(f'Размер изображения не должен быть больше {megabite_limit} МБ')