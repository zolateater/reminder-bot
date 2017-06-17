from __future__ import with_statement
from alembic import context
from sqlalchemy import pool, create_engine
from logging.config import fileConfig
import sys
from os.path import abspath, dirname


# Path to sources dir
src_dir_path = dirname(dirname((abspath(__file__))))
sys.path.insert(0, src_dir_path)

import app.db

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def engine_from_app_config(configuration, prefix='sqlalchemy.', **kwargs):
    """
    This is custom declaration function for taking url config settings from
    application.
    Contains very same code as engine_from_config except taking url.
    """

    options = dict((key[len(prefix):], configuration[key])
                   for key in configuration
                   if key.startswith(prefix))
    options['_coerce_config'] = True
    options.update(kwargs)
    url = app.db.DBConnection.connection_string_from_config()
    return create_engine(url, **options)

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = app.db.DBConnection.connection_string_from_config()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = engine_from_app_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)


    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
