from django.db import models

class PublishStateOptions(models.TextChoices): #TextChoices para django 3.0
        # CONSTANT = DB_VALUE, USER_DISPLAY_VA
        PUBLISH = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'
        # UNLISTED = 'UN', 'Unlisted'
        # Private = 'PR', 'Private'