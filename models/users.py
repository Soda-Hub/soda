import sqlalchemy
from sqlalchemy.sql import and_
from .crypto_utils import encrypt_password, generate_keypair
from .meta import metadata, database


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("remote", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("pub_key", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("priv_key", sqlalchemy.String, nullable=True),
)


follows = sqlalchemy.Table(
    'follows',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('follower_id', sqlalchemy.Integer),
    sqlalchemy.Column('followed_id', sqlalchemy.Integer)
)


class UserManager(object):
    async def add_user(self, username, password):
        hashed = encrypt_password(password)
        bpriv_key, bpub_key = generate_keypair()

        priv_key = bpriv_key.decode()
        pub_key = bpub_key.decode()

        query = users.insert().values(
            username=username,
            password=hashed,
            pub_key=pub_key,
            priv_key=priv_key,
        )
        await database.execute(query)

    async def get_user(self, username):
        query = users.select().where(users.c.username==username)
        results = await database.fetch_one(query)
        return results

    async def get_or_add_remote_user(self, username):
        query = users.select().where(
                    and_(users.c.username==username, users.c.remote==True))
        results = await database.fetch_one(query)

        if results is None:
            add_user_query = users.insert().values(
                username=username,
                remote=True
            )
            await database.execute(add_user_query)
            results = await database.fetch_one(query)

        return results


class FollowManager(object):
    async def add_following(self, follower_id, followed_id):
        query = follows.insert().values(
            follower_id=follower_id,
            followed_id=followed_id,
        )
        await database.execute(query)

    async def remove_following(self, follower_id, followed_id):
        query = follows.delete().where(
            and_(follower_id==follower_id,
                 followed_id==followed_id),
        )
        await database.execute(query)


user_manager = UserManager()
follow_manager = FollowManager()
