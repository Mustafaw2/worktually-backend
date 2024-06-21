class GlobalDatabaseRouter:
    """
    A router to control all database operations on models in the
    lookups and job_seekers applications.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read lookups and job_seekers models go to the global db.
        """
        if model._meta.app_label in ['lookups', 'job_seekers']:
            return 'global'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write lookups and job_seekers models go to the global db.
        """
        if model._meta.app_label in ['lookups', 'job_seekers']:
            return 'global'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the lookups or job_seekers app is involved.
        """
        if obj1._meta.app_label in ['lookups', 'job_seekers'] or \
           obj2._meta.app_label in ['lookups', 'job_seekers']:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the lookups and job_seekers apps only appear in the 'global'
        database.
        """
        if app_label in ['lookups', 'job_seekers']:
            return db == 'global'
        return None
