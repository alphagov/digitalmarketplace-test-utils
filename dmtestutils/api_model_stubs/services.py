
from .base import BaseAPIModelStub


class DraftServiceStub(BaseAPIModelStub):
    resource_name = "services"
    links = {
        "self": "http://127.0.0.1:5000/draft-services/{id}",
        "publish": "http://127.0.0.1:5000/draft-services/{id}/publish",
        "complete": "http://127.0.0.1:5000/draft-services/{id}/complete",
        "copy": "http://127.0.0.1:5000/draft-services/{id}/copy",
    }
    default_data = {
        "id": 1234,
        "copiedToFollowingFramework": False,
        "frameworkSlug": "g-cloud-10",
        "frameworkFramework": "g-cloud",
        "frameworkFamily": "g-cloud",
        "frameworkName": "G-Cloud 10",
        "frameworkStatus": "open",
        "lot": "cloud-software",
        "lotSlug": "cloud-software",
        "lotName": "Cloud software",
        "serviceName": "I run a service that does a thing",
        "status": "not-submitted",
        "supplierId": 8866655,
        "supplierName": "Kev's Pies",
        "createdAt": "2017-04-07T12:34:00.000000Z",
        "updatedAt": "2017-04-07T12:34:00.000000Z",
    }
    optional_keys = (
        ("frameworkFamily", "framework_family"),
        ("frameworkFramework", "framework_framework"),
        ("frameworkName", "framework_name"),
        ("frameworkSlug", "framework_slug"),
        ("lotSlug", "lot_slug"),
        ("lotName", "lot_name"),
        ("serviceName", "service_name"),
        ("supplierId", "supplier_id"),
        ("supplierName", "supplier_name"),
        ("createdAt", "created_at"),
        ("updatedAt", "updated_at"),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.response_data["links"] = self._format_values(self.links)

        if (
            ("framework_slug" in kwargs or "frameworkSlug" in kwargs)
            and ("framework_name" not in kwargs and "frameworkName" not in kwargs)
            and ("framework_family" not in kwargs and "frameworkFamily" not in kwargs)
        ):
            self.response_data.update(self._format_framework(self.response_data["frameworkSlug"], oldstyle=True))

        if self.response_data["status"] != "not-submitted":
            self.response_data["updatedAt"] = "2017-05-08T13:24:00.000000Z"
