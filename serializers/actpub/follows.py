from marshmallow import Schema, fields
from settings import ALLOWED_HOSTS


AS_CONTEXT = 'https://www.w3.org/ns/activitystreams'
DOMAIN  = 'https://' + ALLOWED_HOSTS[0]


# {"@context":"https://www.w3.org/ns/activitystreams",
#  "id":"https://mastodon.social/<uuid>",
#  "type":"Follow",
#  "actor":"https://mastodon.social/users/victorneo",
#  "object":"https://sodahub.cheshire.io/users/victor6"}
class FollowSchema(Schema):
    id = fields.Str()
    type = fields.Str(data_key='type')
    actor = fields.Str()
    obj = fields.Str(data_key='object')


# {"@context":"https://www.w3.org/ns/activitystreams",
#  "id":"https://mastodon.social/users/victorneo/followers",
#  "type":"OrderedCollection",
#  "totalItems":6,
#  "first":"https://mastodon.social/users/victorneo/followers?page=1"}
class FollowerSummarySchema(Schema):
    context = fields.Str(default=AS_CONTEXT, data_key='@context')
    type = fields.Str(default='OrderedCollection')
    totalItems = fields.Int()
    first = fields.Function(lambda obj: DOMAIN + '/' + obj['first'])


#{"@context":"https://www.w3.org/ns/activitystreams",
# "id":"https://mastodon.social/users/victorneo/followers?page=1",
# "type":"OrderedCollectionPage",
# "totalItems":6,
# "partOf":"https://mastodon.social/users/victorneo/followers",
# "orderedItems":["..."]}
class FollowerSchema(Schema):
    pass
