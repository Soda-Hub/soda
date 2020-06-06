from settings import ALLOWED_HOSTS
from marshmallow import Schema, fields


class WebFingerSchema(Schema):
    subject = fields.Method('get_subject')
    links = fields.Method('get_links')

    def get_subject(self, obj):
        return 'acct:' + obj.username + '@' + ALLOWED_HOSTS[0]

    def get_links(self, obj):
        return [
            {'rel': 'self', 'type': 'application/activity+json',
            'href': 'https://' + ALLOWED_HOSTS[0] + '/users/' + obj.username}]

    class Meta:
        fields = ('subject', 'links')
