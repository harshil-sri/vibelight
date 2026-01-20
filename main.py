import requests
import sys
from PIL import Image
from io import BytesIO
import numpy as np
from sklearn.cluster import KMeans
import colorsys
import tinytuya
import time
import webcolors
import atexit

def cleanup_lights():
    print("\n🧹 Cleaning up: Resetting bulb to White...")
    try:
        bulb.set_mode('white')
        bulb.set_white(1000, 1000)
    except:
        print("Could not reset bulb.")
atexit.register(cleanup_lights)

def get_color_name(rgb_triplet):
    min_colours = {}
    for name in webcolors.names("css3"):
        r_c, g_c, b_c = webcolors.name_to_rgb(name)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

device_id , local_key, ip_address = "ENTER_DEVICE_ID_HERE", "ENTER_LOCAL_API_HERE", "ENTER_IP_ADDRESS_HERE"
bulb = tinytuya.BulbDevice(device_id,None, local_key)
bulb.set_version(3.3)
bulb.set_socketPersistent(True)
last_song = None
def last_fm():
    response = requests.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=hrxlukaki&api_key=ENTER_API_KEY_HERE")
    api_data = response.json()
    track_list = api_data['recenttracks']['track']
    #print(track_list)
    current_song = track_list[0]
    #print(current_song)

    #print(current_song['@attr'])
    if '@attr' in current_song and current_song['@attr']['nowplaying'] == 'true':
        print("Currently Playing: ", current_song['name'], "🎶🎶")
        print("-" * 30)
        image_url = current_song['image'][3]['#text']
        return current_song['name'], image_url
    else:
        print("No song playing currently! ☹️")
        return None, None

def download_image(url):
    temp = requests.get(url, stream = True)
    large_img = Image.open(BytesIO(temp.content)).convert('RGB')
    final_img = large_img.resize((50,50))
    #print(final_img.size)
    img_array = np.array(final_img)
    #print(img_array.shape)
    final_array = img_array.reshape(-1,3)
    #print(final_array.shape)
    model = KMeans(n_clusters = 6, random_state = 0)
    model.fit(final_array)
    centers = model.cluster_centers_.astype(int)
    #print(centers)

    best_color = centers[0]
    max_score = -1
    
    for rgb in centers:
        norm = rgb / 255.0
        h, s, v = colorsys.rgb_to_hsv(norm[0], norm[1], norm[2])
        score = s
        # --- THE BIAS ---
        if h < 0.1 or h > 0.9:
            score *= 1.3
        if score > max_score and v > 0.05:
            max_score = score
            best_color = rgb

    final_color = best_color / 255
    r,g,b = final_color
    h,s,v = colorsys.rgb_to_hsv(r, g, b)
    s = s * 1.5
    if s > 1.0:
        s = 1.0
    r_float, g_float, b_float = colorsys.hsv_to_rgb(h, s, 1.0)
    final_color = [int(r_float * 255), int(g_float * 255), int(b_float * 255)]
    #print (final_color)
    return final_color


def set_bulb(r,g,b):
    bulb.status()
    max_val = max(r, g, b)
    
    if max_val > 0:
        scale = 255.0 / max_val
        r = int(r * scale)
        g = int(g * scale)
        b = int(b * scale)
    try:
        bulb.set_mode('colour')
        bulb.set_colour(r, g, b)
    except:
        print("Bulb glitch (ignoring)")
no_song_count = 0

while True:
    name, url = last_fm()
    if name:
        no_song_count = 0
        if name != None and name != last_song:
            print("‼️  New Song Detected ‼️")
            best_color = download_image(url)
            color_name = get_color_name(best_color)
            print(f"🎨  Detected Color: {color_name}")
            print(f"💡  Setting bulb color to {color_name}")
            set_bulb(*best_color)
            print(f"✅  Color changed to {color_name}")
            print("-" * 30)
            last_song = name
    else:
        no_song_count += 1
        print(f"[{no_song_count}/6]")
        print("-" * 30)
        
        if no_song_count >= 6:
            print("\n🛑 Timeout reached. Exiting.")
            sys.exit()
    time.sleep(5)