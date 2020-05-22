from marshmallow import Schema, fields



class WebFingerSchema(Schema):
    subject = fields.Str()
    links = fields.Function(lambda obj: 
        [{'rel': 'self', 'type': 'application/activity+json',
        'href': obj}])

    class Meta:
        fields = ('subject', 'links')
