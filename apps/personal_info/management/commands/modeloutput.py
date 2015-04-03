"""
This module contains management commands for the
personal_info application
"""
from django.core.management.base import BaseCommand
from django.db import models
from django.db import utils


class Command(BaseCommand):
    """
    The command is represented via class named Command
    So it's the 'instance' of our command
    """
    help = 'Outputs the information about all project \
            models and the count of objects in each model.'

    def handle(self, *args, **options):
        """
        The method that actually handles the command
        :param args: command arguments
        :param options: command options
        :return: None
        """
        try:
            model_list = models.get_models()
            for model in model_list:
                self.stdout.write(
                    '%s - %s' % (
                        model.__name__,
                        model.objects.count()
                    )
                )
                self.stderr.write(
                    'error: %s - %s' % (
                        model.__name__,
                        model.objects.count()
                    )
                )
        except utils.OperationalError:
            pass
