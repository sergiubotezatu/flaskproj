from marshmallow import Schema, fields

class PostsJsonSchema(Schema):
    postid = fields.Int(dump_only=True)
    auth = fields.Str(required_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    created = fields.Str(dump_only=True)
    date_modified = fields.Str(dump_only=True)
    img_src = fields.Str(required=True)