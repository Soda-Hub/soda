import sqlalchemy
from sqlalchemy.sql import and_, func
from sqlalchemy import select
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
    async def get_follower_count(self, user_id):
        query = select([func.count(follows.c.followed_id==user_id)])
        results = await database.fetch_one(query)
        return results[0]

    async def get_followers(self, user_id, page):
        query = select([users.c.username]).where(
                        and_(follows.c.followed_id==user_id,
                             follows.c.follower_id==users.c.id))
        count = 10
        offset = (page - 1) * count
        query = query.offset(offset).limit(count).order_by(follows.c.id)
        return await database.fetch_all(query)

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
