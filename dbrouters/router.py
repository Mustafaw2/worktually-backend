class GlobalDatabaseRouter:
    """
    A router to control all database operations on models in the
    lookups application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read lookups models go to the lookups db.
        """
        if model._meta.app_label == 'lookups':
            return 'global'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write lookups models go to the lookups db.
        """
        if model._meta.app_label == 'lookups':
            return 'global'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the lookups app is involved.
        """
        if obj1._meta.app_label == 'lookups' or \
           obj2._meta.app_label == 'lookups':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the lookups app only appears in the 'global'
        database.
        """
        if app_label == 'lookups':
            return db == 'global'
        return None
