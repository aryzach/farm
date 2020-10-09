from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_redis import FlaskRedis
import sys
from svgpathtools import svg2paths, paths2svg
import re
import pickle
import json
import datetime

sys.path.append('../vehicle')

from master_process import Robot, RobotCommand


app = Flask(__name__, template_folder="templates")
app.config['REDIS_URL'] = "redis://:@localhost:6379/0"
redis_client = FlaskRedis(app)


volatile_path = [] # When the robot is streaming a path, save it in RAM here.
active_site = ""

def get_svg_path(filename):
    p = re.compile('\s+[d][=]["]([M][^"]+)["]')
    with open(filename) as f:
        for line in f:
            matches = p.match(line)
            if matches:
                return matches.group(1).replace(' ', ', ')

robot_icon_path = get_svg_path("robot.svg")
arrow_icon_path = get_svg_path("arrow.svg")


@app.route('/')
def map_canvas_flask():
    return render_template(
        'acorn_map.html'
    )


date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, (datetime.datetime, datetime.date))
    else None
)

@app.route('/api/get_herd_data')
def send_herd_data():
    keys = get_robot_keys()
    robots = robots_to_json(keys)
    return jsonify(robots)

def get_robot_keys():
    robot_keys = []
    for key in redis_client.scan_iter():
        if ':robot:' in str(key):
            if ':command:' not in str(key):
                robot_keys.append(key)
    return robot_keys

def robots_to_json(keys):
    robots_list = []
    for key in keys:
        robot = pickle.loads(redis_client.get(key))
        time_stamp = json.dumps(robot.time_stamp, default=date_handler)
        live_path_data = robot.live_path_data
        gps_path_data = robot.gps_path_data
        debug_points = robot.debug_points
        #print(debug_points)
        robot_entry = { 'name': robot.name, 'lat': robot.location.lat, 'lon':
        robot.location.lon, 'heading': robot.location.azimuth_degrees,
        'speed': robot.speed, 'turn_intent_degrees': robot.turn_intent_degrees,
        'voltage': robot.voltage, 'control_state': robot.control_state,
        'motor_state': robot.motor_state, 'time_stamp': time_stamp,
        'loaded_path_name': "" if not robot.loaded_path_name else robot.loaded_path_name.split('gpspath:')[1].split(':key')[0],
        'live_path_data' : live_path_data,
        'gps_path_data' : gps_path_data,
        'debug_points' : debug_points
        # 'front_lat': debug_points[0].lat,
        # 'front_lon': debug_points[0].lat,
        # 'rear_lat': debug_points[1].lat,
        # 'rear_lon': debug_points[1].lat,
        # 'front_close_lat': debug_points[2].lat,
        # 'front_close_lon': debug_points[2].lat,
        # 'rear_close_lat': debug_points[3].lat,
        # 'rear_close_lon': debug_points[3].lat,
        }
        robots_list.append(robot_entry)
    return robots_list

@app.route('/api/save_path', methods = ['POST'])
@app.route('/api/save_path/<pathname>', methods = ['POST'])
def save_current_path(pathname=None):
    if request.method == 'POST':
        pathdata = request.json
        print(pathdata)
    if not pathdata:
        return "Missing something. No path saved."
    if not pathname:
        volatile_path = pathdata
        return "Updated volatile_path"
    key = get_path_key(pathname)
    redis_client.set(key, pickle.dumps(pathdata))
    return "Saved Path {}".format(key)

@app.route('/api/delete_path/<pathname>')
def delete_path(pathname=None):
    if not pathname:
        return "Missing something. No path deleted."
    redis_client.delete(get_path_key(pathname))
    return "Deleted path {}".format(pathname)

@app.route('/api/set_vehicle_path/<pathname>/<vehicle_name>')
def set_vehicle_path(pathname=None, vehicle_name=None):
    if not vehicle_name or not pathname:
        return "Missing something. No vehicle path set."
    vehicle_command_key = "{}:robot:{}:command:key".format(active_site, vehicle_name)
    if redis_client.exists(vehicle_command_key):
        robot_command = pickle.loads(redis_client.get(vehicle_command_key))
    else:
        robot_command = RobotCommand()
    robot_command.load_path = get_path_key(pathname)
    print(vehicle_command_key)
    redis_client.set(vehicle_command_key, pickle.dumps(robot_command))
    return "Set vehicle {} path to {}".format(vehicle_command_key, robot_command.load_path)

@app.route('/api/set_gps_recording/<vehicle_name>/<record_gps_path>')
def set_gps_recording(vehicle_name=None, record_gps_path=None):
    if not vehicle_name or not record_gps_path:
        return "Missing something. No gps command set."
    if len(active_site) == 0:
        return "Active site not set. Please load a path."
    vehicle_command_key = "{}:robot:{}:command:key".format(active_site, vehicle_name)
    if redis_client.exists(vehicle_command_key):
        robot_command = pickle.loads(redis_client.get(vehicle_command_key))
    else:
        robot_command = RobotCommand()
    robot_command.record_gps_path = record_gps_path
    print(robot_command.record_gps_path)
    redis_client.set(vehicle_command_key, pickle.dumps(robot_command))
    return "Set vehicle {} record gps command to {}".format(vehicle_command_key, record_gps_path)

@app.route('/api/set_vehicle_autonomy/<vehicle_name>/<speed>/<enable>')
def set_vehicle_autonomy(vehicle_name=None, speed=None, enable=None):
    if not all((vehicle_name, speed, enable)):
        return "Missing something. No vehicle autonomy set."
    if len(active_site) == 0:
        return "Active site not set. Please load a path."
    vehicle_command_key = "{}:robot:{}:command:key".format(active_site, vehicle_name)
    if redis_client.exists(vehicle_command_key):
        robot_command = pickle.loads(redis_client.get(vehicle_command_key))
    else:
        robot_command = RobotCommand()
    robot_command.activate_autonomy = enable=="true"
    robot_command.autonomy_velocity = float(speed)
    redis_client.set(vehicle_command_key, pickle.dumps(robot_command))
    return "Set vehicle {} autonomy to {}".format(vehicle_command_key, (speed, enable))

def get_path_key(pathname):
    print(active_site)
    return "{}:gpspath:{}:key".format(active_site, pathname)

@app.route('/api/get_path/')
@app.route('/api/get_path/<pathname>')
def show_path(pathname=None):
    if not pathname:
        return jsonify(volatile_path)
    else:
        print(get_path_key(pathname))
        path = pickle.loads(redis_client.get(get_path_key(pathname)))
        return jsonify(path)

@app.route('/api/get_path_names')
def send_path_names():
    names = []
    for key in redis_client.scan_iter():
        if ':gpspath:' in str(key):
            pathname = str(key).split(":")[2]
            names.append(pathname)
            global active_site
            active_site = str(str(key).split(":")[0]).replace('b\'','')
            print(active_site)
    return jsonify(names)

@app.route('/api/getRobotIcon')
def send_robot_paths():
    return jsonify(robot_icon_path)

@app.route('/api/getArrowIcon')
def send_arrow_paths():
    return jsonify(arrow_icon_path)

@app.route('/api/robot.svg')
def send_robot_icon():
    return send_from_directory('../', "robot.svg")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")

