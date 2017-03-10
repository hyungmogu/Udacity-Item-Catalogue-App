from item_catalogue import app
from item_catalogue.handlers.login.routes import mod
from item_catalogue.handlers.logout.routes import mod
from item_catalogue.handlers.post.routes import mod
from item_catalogue.handlers.api.routes import mod
from item_catalogue.handlers.home.routes import mod
from item_catalogue.handlers.category.routes import mod
from item_catalogue.handlers.welcome.routes import mod
from item_catalogue.handlers.error.routes import mod

app.register_blueprint(login.routes.mod)
app.register_blueprint(logout.routes.mod)
app.register_blueprint(post.routes.mod)
app.register_blueprint(api.routes.mod)
app.register_blueprint(home.routes.mod)
app.register_blueprint(category.routes.mod)
app.register_blueprint(welcome.routes.mod)
app.register_blueprint(error.routes.mod)

