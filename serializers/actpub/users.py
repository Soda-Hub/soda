from marshmallow import Schema, fields
from settings import ALLOWED_HOSTS


USER_CONTEXT = ['https://www.w3.org/ns/activitystreams',
                'https://w3id.org/security/v1']
DOMAIN  = 'https://' + ALLOWED_HOSTS[0]


class MediaSchema(Schema):
    mediaType = fields.Method('get_media_type')
    type = fields.Method('get_type')
    url = fields.Method('get_url')

    def get_media_type(self, obj):
        return 'image/jpg'

    def get_type(self, obj):
        return 'icon'

    def get_url(self, obj):
        return DOMAIN + '/static/images/profile_small.jpg'


class PublicKeySchema(Schema):
    id = fields.Method('get_id')
    owner = fields.Method('get_user_url')
    publicKeyPem = fields.Str(attribute='pub_key')

    def get_user_url(self, obj):
        return DOMAIN + '/users/' + obj.username

    def get_id(self, obj):
        return self.get_user_url(obj) + '#main-key'


class UserSchema(Schema):
    context = fields.Field(default=USER_CONTEXT, data_key='@context')
    id = fields.Method('get_user_url')
    type = fields.Field(default='Person')
    inbox = fields.Method('get_inbox')
    outbox = fields.Method('get_outbox')
    followers = fields.Method('get_followers')
    endpoints = fields.Method('get_endpoints')
    icon = fields.Method('get_icon')
    publicKey = fields.Method('get_public_key')
    preferredUsername = fields.Function(lambda obj: obj.username)
    name = fields.Function(lambda obj: obj.username)

    def get_user_url(self, obj):
        return DOMAIN + '/users/' + obj.username

    def get_inbox(self, obj):
        return self.get_user_url(obj) + '/inbox'

    def get_outbox(self, obj):
        return self.get_user_url(obj) + '/inbox'

    def get_followers(self, obj):
        return self.get_user_url(obj) + '/followers'

    def get_endpoints(self, obj):
        return {'sharedInbox': DOMAIN + '/inbox'}

    def get_icon(self, obj):
        return MediaSchema().dump(obj)

    def get_public_key(self, obj):
        return PublicKeySchema().dump(obj)
