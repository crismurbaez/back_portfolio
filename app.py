# -*- coding: utf-8 -*-
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import json
from flask import Flask, request, jsonify, Response
from flask_cors import CORS


load_dotenv()
app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    return "send_email with POST"


@app.route("/sendemail", methods=["POST"])
def send_email():
    # envío de emails
    (
        name,
        email,
        asunto,
        mensaje,
    ) = request.json.values()

    remitente = os.getenv("USER")
    destinatario = os.getenv("DEST")

    password = os.getenv("PASS")

    msg = MIMEMultipart()

    msg["Subject"] = asunto
    # me envío el email a mí misma
    msg["From"] = remitente
    msg["To"] = destinatario

    body = (
        "Recibiste un mensaje desde el portfolio de "
        + name
        + " y su email es: "
        + email
        + ". Su mensaje es : "
        + mensaje
    )

    msg.attach(MIMEText(body, "plain", "utf-8"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(remitente, password)

    server.sendmail(remitente, destinatario, msg.as_string())

    server.quit()
    return "El email fue enviado con éxito"


if __name__ == "__main__":
    app.run()
