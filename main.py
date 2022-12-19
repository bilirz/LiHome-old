from flask import Flask, render_template, session
from handler import father, static, index, log, redblack, days, game, energy, user, pk, motto
import config
import logging

app = Flask(__name__)

app.register_blueprint(father.bp)
app.register_blueprint(static.bp)
app.register_blueprint(index.bp)
app.register_blueprint(log.bp)
app.register_blueprint(redblack.bp)
app.register_blueprint(days.bp)
app.register_blueprint(game.bp)
app.register_blueprint(energy.bp)
app.register_blueprint(user.bp)
app.register_blueprint(pk.bp)
app.register_blueprint(motto.bp)

app.config.from_object(config)


# logging.basicConfig(level=logging.DEBUG, filename="./app.log")

@app.errorhandler(404)
def miss(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
