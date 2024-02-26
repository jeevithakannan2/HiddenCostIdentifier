import os
import pystray
import asyncio
import threading
from PIL import Image
from Ajio import Ajio
from Amazon import Amazon
from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart import Quart, jsonify, request

app = Quart(__name__)

global ajio_instance


@app.route('/ajio_run', methods=['POST'])
async def ajio_run():
    request_data = await request.get_json()
    requester_ip = request.remote_addr
    print(f"Route: /ajio_run")
    print(f"Requester IP Address: {requester_ip}")
    print(f"Requester data: {request_data}")

    try:
        if 'url' in request_data:
            url = request_data['url']
            if '/p/' in url:

                global ajio_instance
                ajio_instance = Ajio()

                result = await ajio_instance.main(url)
                return jsonify(result), 200
            else:
                return jsonify({'error': "Enter full product url. Short url not accepted"}), 400
    except:
        return jsonify({'error': "Enter valid url"}), 400


@app.route('/ajio_login', methods=['POST'])
async def ajio_login():
    request_data = await request.get_json()
    requester_ip = request.remote_addr
    print(f"Route: /ajio_login")
    print(f"Requester IP Address: {requester_ip}")
    print(f"Requester data: {request_data}")

    if 'mobileNumber' in request_data:
        mobile_number = request_data['mobileNumber']

        global ajio_instance
        ajio_instance = Ajio()

        result = await ajio_instance.login(mobile_number)
        return jsonify(result), 200

    return jsonify({"Error": "Enter mobile number"})


@app.route('/ajio_otp', methods=['POST'])
async def ajio_OTP():
    request_data = await request.get_json()
    requester_ip = request.remote_addr
    print(f"Route: /ajio_login")
    print(f"Requester IP Address: {requester_ip}")
    print(f"Requester data: {request_data}")

    if 'OTP' in request_data:
        OTP = request_data['OTP']

        global ajio_instance

        result = await ajio_instance.OTP(OTP)
        return jsonify(result), 200

    return jsonify({"Error": "Enter OTP"})


@app.route("/amazon_run", methods=['POST'])
async def amazon_run():
    request_data = await request.get_json()
    requester_ip = request.remote_addr
    print(f"Requester IP Address: {requester_ip}")
    print(f"Requester data: {request_data}")
    try:
        if 'url' in request_data:
            url = request_data['url']
            if '/dp/' or '/gp/' in url:

                amazon_instance = Amazon()

                result = await amazon_instance.main(url)
                return jsonify(result), 200

            else:
                return jsonify({'error': "Enter full product url. Short url not accepted"}), 400
        else:
            return jsonify({'error': "Enter valid url"}), 400
    except TypeError:
        return jsonify({'error': "Enter url"}), 400


def background_task():
    icon = Image.open('icon.ico')
    menu = pystray.Menu(pystray.MenuItem('Exit', lambda: os._exit(0)))
    tray = pystray.Icon("name", icon, "Title", menu)
    tray.run()


async def run_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    config = Config()
    config.bind = "127.0.0.1:5123",
    config.workers = 1
    await serve(app, config)


if __name__ == "__main__":
    background_thread = threading.Thread(target=background_task)
    background_thread.daemon = True
    background_thread.start()

    asyncio.run(run_server())


