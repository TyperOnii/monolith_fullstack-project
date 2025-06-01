INDIVIDUAL_DESCRIPTION = {
    "descr_name_key": "descr_name_value",
    "descr_name_key2": "descr_name_value2",
}

MAPPING_ACTION_TEXT = {
    'create': 'Создание',
    'list': 'Просмотр списка',
    'retrieve': 'Просмотр одного',
    'update': 'Обновление',
    'partial_update': 'Частичное обновление',
    'destroy': 'Удаление',
}

DJANGO_PERMISSIONS_DESCRIPTION = {
    'AllowAny': 'Доступ для всех пользователей',
    'IsAuthenticated': 'Доступ только для зарегистрированных пользователей',
    'IsAdminUser': 'Доступ только для администраторов',
}

def get_description(action, view, descr_key = None, *args, **kwargs) -> str:

    if descr_key:
        return INDIVIDUAL_DESCRIPTION.get(descr_key)
    
    model = view.queryset.model
    permissions = view.permission_classes
    
    def get_permissions_text(permissions):
        permissions_doc = []
        for permission in permissions:
            if permission.__name__ in DJANGO_PERMISSIONS_DESCRIPTION:
                permission_doc = (DJANGO_PERMISSIONS_DESCRIPTION[permission.__name__])
            else: permission_doc = permission.__doc__
            if permission_doc:
                permissions_doc.append(permission_doc)
        text = ", ".join(permissions_doc)
        return text
    
    text = f"""
    Для: {MAPPING_ACTION_TEXT[action]} {model._meta.verbose_name}
    Ограничения: {get_permissions_text(permissions)}
    
    """

    return text

