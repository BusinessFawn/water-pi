echo "installing requirements"
pip3 install -r requirements.txt
echo "finished installing, starting server"
cd source
export FLASK_APP=led_pi_api.py
sudo -E flask run --host=0.0.0.0 --port=80
