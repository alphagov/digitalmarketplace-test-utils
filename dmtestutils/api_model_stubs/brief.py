from .base import BaseAPIModelStub


class BriefStub(BaseAPIModelStub):
    resource_name = 'briefs'
    user = {
        "active": True,
        "role": "buyer",
        "emailAddress": "buyer@email.com",
        "id": 123,
        "name": "Buyer User"
    }
    default_data = {
        "id": 1234,
        "title": "I need a thing to do a thing",
        "frameworkSlug": "digital-outcomes-and-specialists",
        "frameworkName": "Digital Outcomes and Specialists",
        "frameworkFramework": "digital-outcomes-and-specialists",
        "frameworkStatus": "live",
        "framework": {
            "family": "digital-outcomes-and-specialists",
            "name": "Digital Outcomes and Specialists",
            "slug": "digital-outcomes-and-specialists",
            "status": "live",
        },
        "lotName": "Digital Specialists",
        "lotSlug": "digital-specialists",
        "isACopy": False,
        "status": "draft",
        "users": [user],
        "createdAt": "2016-03-29T10:11:12.000000Z",
        "updatedAt": "2016-03-29T10:11:13.000000Z",
        "links": {}
    }

    optional_keys = [
        ('lotName', 'lot_name'),
        ('lotSlug', 'lot_slug'),
        ('clarificationQuestions', 'clarification_questions'),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if kwargs.get('user_id'):
            self.user['id'] = kwargs.pop('user_id')
            self.response_data['users'] = [self.user]

        # Allow snake case framework_* kwargs for backwards compatibility
        for nested_framework_key, camelcase_key, snakecase_kwarg in [
            ('family', 'frameworkFramework', 'framework_family'),
            ('name', 'frameworkName', 'framework_name'),
            ('slug', 'frameworkSlug', 'framework_slug'),
            ('status', 'frameworkStatus', 'framework_status'),
        ]:
            if kwargs.get(snakecase_kwarg):
                # Update top level key
                self.response_data[camelcase_key] = kwargs.get(snakecase_kwarg)
                # Update nested key, deleting the snakecase kwarg which will have been updated already in super()
                self.response_data['framework'][nested_framework_key] = kwargs.get(snakecase_kwarg)
                del self.response_data[snakecase_kwarg]

        # Status-dependent values
        if self.response_data['status'] is not "draft":
            self.response_data["publishedAt"] = "2016-03-29T10:11:14.000000Z"
            self.response_data["applicationsClosedAt"] = "2016-04-07T00:00:00.000000Z"
            self.response_data["clarificationQuestionsClosedAt"] = "2016-04-02T00:00:00.000000Z"
            self.response_data["clarificationQuestionsPublishedBy"] = "2016-04-02T00:00:00.000000Z"
            if kwargs.get('clarification_questions_closed') is not None:
                self.response_data["clarificationQuestionsAreClosed"] = kwargs.pop('clarification_questions_closed')
                del self.response_data['clarification_questions_closed']

        if self.response_data['status'] is "withdrawn":
            self.response_data["withdrawnAt"] = "2016-05-07T00:00:00.000000Z"
        elif self.response_data['status'] is "unsuccessful":
            self.response_data["unsuccessfulAt"] = "2016-05-07T00:00:00.000000Z"
        elif self.response_data['status'] is "cancelled":
            self.response_data["cancelledAt"] = "2016-05-07T00:00:00.000000Z"