class GlobalDatabaseRouter:
    """
    A router to control all database operations on models in the
    global application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read global models go to global db.
        """
        if model._meta.app_label == 'global':
            return 'global'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write global models go to global db.
        """
        if model._meta.app_label == 'global':
            return 'global'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the global app is involved.
        """
        if obj1._meta.app_label == 'global' or \
           obj2._meta.app_label == 'global':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the global app only appears in the 'global'
        database.
        """
        if app_label == 'global':
            return db == 'global'
        return None
