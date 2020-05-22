from marshmallow import Schema, fields


USER_CONTEXT = ['https://www.w3.org/ns/activitystreams',
                'https://w3id.org/security/v1']


class MediaSchema(Schema):
    mediaType = fields.Str()
    type = fields.Str()
    url = fields.Str()


class PublicKeySchema(Schema):
    id = fields.Str()
    owner = fields.Str()
    publicKeyPem = fields.Str()


class UserSchema(Schema):
    context = fields.Field(default=USER_CONTEXT, data_key='@context')
    id = fields.Str()
    type = fields.Field(default='Person')
    preferredUsername = fields.Str()
    inbox = fields.Str()
    outbox = fields.Str()
    followers = fields.Str()
    endpoints = fields.Function(lambda obj: {'sharedInbox': obj})
    name = fields.Str()
    icon = fields.Nested(MediaSchema)
    publicKey = fields.Nested(PublicKeySchema)
