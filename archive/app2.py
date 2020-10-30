from flask import Flask, render_template, jsonify, request, redirect, url_for, jsonify

host = 'localhost'
port = 5000

app = Flask(__name__)



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aurora.db'




@app.route('/')
def index():
    return redirect(url_for('aurora'))

@app.route('/aurora', methods=['GET', 'POST'])
def aurora():
    if request.method == 'POST':
        data = request.form # get the data from the request form
        name = data['name']
        email = data['email']

        new_data = User(name, email)
        db.session.add(new_data)
        db.session.commit()

    user_data = User.query.all()
    
    return render_template('index.html', user_data=user_data)
    



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    #server = Server((host, port), app)
    #print(f'Running Aurora on http://{host}:{port} (Press CTRL+C to shut down)')
    #try:
    #    server.start()
    #except KeyboardInterrupt:
    #    print(f'\n\nShutting down Aurora')
    #    server.stop()