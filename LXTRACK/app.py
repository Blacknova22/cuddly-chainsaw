from flask import Flask, request, render_template, redirect
from datetime import datetime
import os
import requests

app = Flask(__name__)

desktop_path = os.path.expanduser("~/Bureau")
LOG_FILE = os.path.join(desktop_path, "ip_logs.txt")

def get_geo_info(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719")
        return res.json()
    except:
        return {"status": "fail", "query": ip}

# Route d'accueil qui affiche index.html (page avec bouton)
@app.route('/')
def home():
    return render_template('index.html')


# Route pour afficher et traiter le formulaire téléphone
@app.route('/phone', methods=['GET', 'POST'])
def phone_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        adress = request.form.get('adress')
        zip_code = request.form.get('zip_code')
        city = request.form.get('city')
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_line = (
            f"{timestamp} - IP: {ip} - Nom: {name} - Email: {email} - Téléphone: {phone} - Adress: {adress} - Code postal: {zip_code} - Ville: {city}\n"
        )

        with open(LOG_FILE, "a") as file:
            file.write(log_line)

        print(f"[PHONE] {log_line.strip()}")

        return render_template('thank_you.html')

    return render_template('phone_form.html')


if __name__ == '__main__':
      port = int(os.environ.get('PORT', 8080))  # récupère le port de l'env, sinon 5000 par défaut
      app.run(host='0.0.0.0', port=port)
