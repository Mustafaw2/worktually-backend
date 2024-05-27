from django.db import models
from .modules.users.models import UserProfile
from .modules.settings.models import Setting
from .modules.organisations.models import  Organization
from .modules.dependents.models import Dependent
from .modules.roles.models import Role
from .modules.permisssions.models import Permission
from .modules.invitations.models import Invitation
from .modules.education_experience.models import Education, Experience
from .modules.skills_languages_portfolio.models import Skill,Portfolio,Language
from.modules.lookups.models import Lookup
# Create your models here.
