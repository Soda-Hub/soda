import sqlalchemy
from .crypto_utils import encrypt_password, generate_keypair
from .meta import metadata, database


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(length=50)),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("pub_key", sqlalchemy.String),
    sqlalchemy.Column("priv_key", sqlalchemy.String),
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


user_manager = UserManager()
