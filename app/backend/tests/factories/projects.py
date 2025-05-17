from faker import Factory
from factory.django import DjangoModelFactory

from core.apps.projects.models.projects import Project

factory = Factory.create('ru-RU')

factory.add_provider(Project, 'project')


class ProjectModelFactory(DjangoModelFactory):
    class Meta:
        model = Project

    title = factory.Faker('sentence', nb_words=2)
    description = factory.Faker('sentence', nb_words=5)
    slug = factory.Faker('slug')