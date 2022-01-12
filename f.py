
# Import for Migrations
from flask_migrate import Migrate, migrate
 
# Settings for migrations
migrate = Migrate(app, db)