from marshmallow import Schema, fields


# {"@context":"https://www.w3.org/ns/activitystreams",
#  "id":"https://mastodon.social/99a04493-0cdd-4912-8831-322f87fc0ec0",
#  "type":"Follow",
#  "actor":"https://mastodon.social/users/victorneo",
#  "object":"https://sodahub.cheshire.io/users/victor6"}


class FollowSchema(Schema):
    id = fields.Str()
    type = fields.Str(data_key='type')
    actor = fields.Str()
    obj = fields.Str(data_key='object')
