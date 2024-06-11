class GlobalDatabaseRouter:
    """
    A router to control all database operations on models in the
    'employee' application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read 'employee' models go to 'global'.
        """
        if model._meta.app_label == 'employee':
            return 'global'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write 'employee' models go to 'global'.
        """
        if model._meta.app_label == 'employee':
            return 'global'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the 'employee' app is involved.
        """
        if obj1._meta.app_label == 'employee' or obj2._meta.app_label == 'employee':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the 'employee' app only appears in the 'global'
        database.
        """
        if app_label == 'employee':
            return db == 'global'
        return None