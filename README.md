**To get path of venv when using poetry**

poetry env activate

**To run main file**

poetry run uvicorn app.main:app --reload 

how does threading work with db, if some operation is taking time and db gets locked by 1 thread

try to show migration making password field in db as hash value

to reinstall alembic after doing poetry remove alembic you need to run poetry add alembic and then poetry run **alembic init alembic**

this above line will create alembic folder
 
commands that be used to get info wrt alembic

alembic

alembic list_templates (by defualt running alembic init alembic creates alembic folders in generic template)

alembic init --template generic ./scripts (to create alembic scripts using specific template)
 
to use specific template of alembic: alembic init --template <template_name> alembic

The file generated with the generic configuration template contains all directives for both source code configuration as well as database configuration. When using the pyproject template(recently introduced), the source code configuration elements will instead be in a separate pyproject.toml file

line commented as file_template in .ini file can be uncommented to organise the new migration file created at year/date/file_name

For the SQLAlchemy URL, percent signs are used to escape syntactically- significant characters such as the @ sign as well as the percent sign itself. For a password such as "P@ssw%rd" the @ sign as well as the percent sign when placed into a URL should be escaped with urllib.parse.quote_plus:


Partial revision identifier: If we need to execute a specific verson instead of head (as done by alembic upgrade head), we cna define that version in our cmd as alembic upgrade <initials_of_version_revision> if more than 1 such version initials present alembic will notify via error

To execute versions wrt current head we can use: alembic upgrade +2 (2 versions above current head), alembic upgrade -1 (1 version below current head)

To get current version: alembic current

To get history: alembic history --verbose

To get history within specific range: alembic history --rev-range=-3:current(last 3 transactions till current head)

To move back to the first migration file: alembic downgrade base

To go up till current version: alembic upgrade head (this will run all the migrations from current version in db till migration file we have under /versions/)

alembic upgrade head --sql> running migrations in offline mode ie we just need the sql created by migration instead pf actually running them, this doesnt take into account the db connection it just uses db connection string

alembic upgrade head > this actually creates migration script by making connection with db

In the pffline mode. as we defined head so it will read the code from head pointed file and genereate sql wrt it instead of connectiong with db

The target_metadata collection may also be defined as a sequence if an application has multiple MetaData collections involved:
eg: from myapp.mymodel1 import Model1Base
from myapp.mymodel2 import Model2Base
target_metadata = [Model1Base.metadata, Model2Base.metadata]

auto-generate keeps track of any column added, table created, column updated
but it doesnt keep track of table name change, column name change, anonymously added constraints 

for alembic merge
create 2 revisions and in both point down_revision to the version present in db, so that we will get 2 heads
 
alembic merge -m "merge heads" head1 head2 > this will create a new migration file with codes from both files

To create 2 migrations from same head
alembic revision -m 'migration 1'
check head using alembic head
alembic revision -m 'migration 2' --splice --head <base_head>(that is in db)

alembic current> points to the version present in db

alembic head> points to the recent one present under versions/

alembic merge -m "merge users and posts" <rev_B> <rev_C>

Merge revision doesn’t contain schema changes”

“It only resolves multiple heads by combining revision graph”

“Actual schema changes remain in original migrations”

We can resolve code changes by manually adding them in the merged file

**Steps for demo**

alembic revision -m 'Initial migration'

alembic revision --autogenerate -m 'Initial migration

alembic revision --autogenerate -m 'changes in user table'

alembic current

alembic heads

---- comment useradress table -----

alembic revision --autogenerate -m 'changes in useraddress table'

alembic revision --autogenerate -m 'uncommented changes in useraddress table'

alembic stamp head

alembic revision --autogenerate -m 'uncommented changes in useraddress table'

alembic revision --autogenerate -m 'uncommented changes in useraddress table' --splice --head c28b809534bb

alembic merge -m 'merge heads' <head1> <head2>

update alembic_version set version_num='c28b809534bb'

# While updating alembic/env.py update following things #

from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import asyncio
from app.models import *
from app.db.database import Base
from dotenv import load_dotenv
load_dotenv()
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is not set")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# to show order of migrations run below cmd


target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async def do_migrations():
        async with connectable.connect() as connection:

            await connection.run_sync(
                lambda conn: context.configure(
                    connection=conn,
                    target_metadata=target_metadata,
                    compare_type=True,
                )
            )

            # ✅ correct transaction + correct call
            async with connection.begin():
                await connection.run_sync(
                    lambda conn: context.run_migrations()
                )

    import asyncio
    asyncio.run(do_migrations())


to rollback to any version in db use alembic downgrade <head revision you need to move to>





