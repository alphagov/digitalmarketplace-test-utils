from .base import BaseAPIModelStub
from .audit_event import AuditEventStub
from .brief import BriefStub
from .framework import FrameworkStub
from .framework_agreement import FrameworkAgreementStub
from .lot import LotStub
from .supplier import SupplierStub
from .supplier_framework import SupplierFrameworkStub


# TODO: Flesh out the stubs below and move to their own modules


class BriefResponseStub(BaseAPIModelStub):
    resource_name = 'briefResponses'
    default_data = {

    }


class DirectAwardProjectStub(BaseAPIModelStub):
    resource_name = 'project'
    default_data = {

    }


class DirectAwardSearchStub(BaseAPIModelStub):
    resource_name = 'search'
    default_data = {

    }


class DraftServiceStub(BaseAPIModelStub):
    resource_name = 'services'
    default_data = {

    }


class OutcomeStub(BaseAPIModelStub):
    resource_name = 'outcome'
    default_data = {

    }


class ServiceStub(BaseAPIModelStub):
    resource_name = 'services'
    default_data = {

    }


class UserStub(BaseAPIModelStub):
    resource_name = 'users'
    default_data = {

    }
