from django.apps import AppConfig


class SkillucketappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "skillucketApp"

    def ready(self):
        """call signals file every time the app is run"""
        import skillucketApp.signals
