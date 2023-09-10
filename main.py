import os, config, time, uuid
from flask import Flask, jsonify, Response, request, json, g
from blueprints.activities import activities

def create_app():
    app = Flask(__name__)
    app.register_blueprint(activities, url_prefix='/api/v1/activities')

    @app.before_request
    def before_request():
        execution_id = uuid.uuid4()
        g.execution_id = execution_id
        g.start_time = time.time()

        print(g.execution_id, "ROUTE CALLED ", request.url)


    # error 404 handler
    @app.errorhandler(404)
    def resource_not_found(e):
        return Response(json.dumps({'error': 'Resource not found !'}), status=404, mimetype='application/json')
    
    # error 405 handler
    @app.errorhandler(405)
    def resource_not_found(e):
        return Response(json.dumps({'error': 'Method not allowed !'}), status=405, mimetype='application/json')
    
    # error 401 handler
    @app.errorhandler(401)
    def custom_401(e):
        return Response(json.dumps({'error': 'Unauthorized !'}), status=401, mimetype='application/json')
    
    @app.route('/ping')
    def hello_world():
        return Response(json.dumps({'message': 'pong'}), status=200, mimetype='application/json')
    
    @app.route('/version', methods=['GET'], strict_slashes=False)
    def version():
        return Response(json.dumps({'success': '1.0.0'}), status=200, mimetype='application/json')
    
    @app.after_request
    def after_request(response):
        if response and response.get_json():
            data = response.get_json()

            data["time_request"] = int(time.time())
            data["version"] = config.VERSION

            response.set_data(json.dumps(data))

        return response
    
    return app

app = create_app()

if __name__ == '__main__':
    print('Running app in port 5000')
    app.run(host='0.0.0.0', port=5000)