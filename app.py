from flask import Flask, render_template
# from sqlalchemy import true
from flask import Flask
from components import app

if __name__=='__main__':
    app.run(debug=True)