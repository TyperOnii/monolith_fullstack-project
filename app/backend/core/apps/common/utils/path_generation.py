
def get_path_upload_project_images(instance,file):
    """Формирование пути к файлу для хранения изображений проекта"""
    return f"projects_images/{instance.project.title}/{file}"