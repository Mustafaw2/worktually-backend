class GlobalDatabaseRouter:
    """
    A router to control all database operations on models in the
    employeee.recruitment and employee apps.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read recruitment models go to global database.
        """
        if model._meta.app_label == 'recruitment':
            return 'global'
        if model._meta.app_label == 'employee':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write recruitment models go to global database.
        """
        if model._meta.app_label == 'recruitment':
            return 'global'
        if model._meta.app_label == 'employee':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in the recruitment or employee apps.
        """
        if obj1._meta.app_label in ['recruitment', 'employee'] and obj2._meta.app_label in ['recruitment', 'employee']:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the recruitment app only appears in the 'global' database
        and the employee app only appears in the 'default' database.
        """
        if app_label == 'recruitment':
            return db == 'global'
        if app_label == 'employee':
            return db == 'default'
        return None
