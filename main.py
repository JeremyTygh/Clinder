import flask
from flask import Flask, jsonify, request, render_template
import user
import init
# import jsons
from google.cloud import datastore

app = flask.Flask(__name__)
app.secret_key = 'this is a secret key'

@app.route('/')
@app.route('/homepage.html')
def root():
    # use render_template to convert the template code to HTML.
    # this function will look in the templates/ folder for your file.
    #us = flask.session.get('user', None)
    if 'user' in flask.session:
        # print("logged in as " + flask.session.get('user'))
        #flask.session.get('user') = user.User(flask.session.get('user'))
        return flask.render_template('homepage.html', clothes=init.clothes)
    return flask.render_template('signin.html')

@app.route('/profile_screen.html')
def profile():
    if not 'user' in flask.session:
        return flask.render_template('signin.html')
    return flask.render_template('profile_screen.html', username=flask.session['user'])

#for accessing the like screen, all of the user's likes will be stored in an array called likes
@app.route('/like_screen.html')
def like():
    if not 'user' in flask.session:
        return flask.render_template('signin.html')
    # return flask.render_template('like_screen.html', likes=flask.session['likes'])
    return flask.render_template('like_screen.html', likes=get_liked())

#for sending the sign in screen
@app.route('/signin.html')
def signin():
    if 'user' in flask.session:
        print("logged in as " + flask.session.get('user'))
        return flask.render_template('homepage.html', clothes=init.clothes, index=flask.session['user'].index)
    return flask.render_template('signin.html')

#for sending the sign up screen
@app.route('/signup.html')
def signup():
    print('redirected to signup page')
    if 'user' in flask.session:
        print("logged in as " +flask.session.get('user'))
        return flask.render_template('homepage.html', clothes=init.clothes, index=flask.session['user'].index)
    return flask.render_template('signup.html')

#for handlng login requests - send username and password through json post request
@app.route('/login', methods=['POST','GET'])
def login():
    username = flask.request.form['username']
    password = flask.request.form['password']

    client = datastore.Client()
    print(username + " " + password)

    query = client.query(kind = 'user')
    query.add_filter("username", "=", username)
    pw = 'password'
    index = 0
    for entity in query.fetch(): #fetch the entity that has the user's username
        pw = entity['password']
        index = entity['index']

    if password == pw: #pw on datastore should be hashed, so compare hashes
        flask.session['user'] = username
        # flask.session['likes'] = 
        flask.session['index'] = 0
        return flask.redirect(flask.url_for('root')), 200
    
    return flask.render_template('signin.html', invalid=True) #return an invalid flag when passwords do not match
    
#for handling register requests - send username and password through json post request
@app.route('/register', methods=['POST','GET'])
def register():
    # response = request.get_json()
    # username = response["username"]
    # password = response["password"]
    username = flask.request.form['username']
    password = flask.request.form['password']

    client = datastore.Client()
    query = client.query(kind = 'user')
    query.add_filter("username", "=", username) #query existing users with that username
    print("users with this username: " + str(query.fetch().num_results))
    if query.fetch().num_results > 0: #if there is any result then the username already exists
        return flask.render_template('signup.html', invalid=True) #return an invalid flag when user already exists

    key = client.key('user', username)
    toUpload = datastore.Entity(key)
    toUpload['username'] = username
    toUpload['password'] = password #hash the password
    toUpload['index'] = 0
    client.put(toUpload) #push user data to datastore

    # flask.session['user'] = username #set session username, allowing access to other pages
    print("registered as " + username)
    # flask.session['user'] = jsons.dumps(user.User(username))
    flask.session['user'] = username
    flask.session['likes'] = ["https://cdn.shopify.com/s/files/1/0718/5347/products/IMG_1495_720x720.jpg?v=1624549101"]
    flask.session['index'] = 0
    print(flask.session['user'])
    #resp = flask.make_response()
    #resp.set_cookie('user', user.User(username))
    #resp.headers['location'] = flask.url_for('root') 
    #return resp, 200
    return flask.redirect(flask.url_for('root')), 200
    #return flask.render_template('homepage.html', clothes=init.clothes, index=userList[flask.session['user']].index)

#for handling clicks of the like button
@app.route('/liked', methods=['POST','GET'])
def received_like():
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        response = request.get_json()
        
        # flask.session['likes'].append( init.clothes[int(response["imageAddress"])] )
        add_like(init.clothes[int(response["imageAddress"])] )
        # flask.session.modified = TRUE
        return 'OK', 200

    flask.session['user'].viewed_item()

#for handling clicks of the dislike button
@app.route('/notliked', methods=['POST','GET'])
def received_dislike():
    flask.session['user'].viewed_item()

@app.route('/logout', methods=['POST','GET'])
def logout():
    flask.session['user'] = None
    flask.session.clear()
    return flask.redirect('/')

def add_like(liked):
    """Add the liked clothing item to the list of likes"""
    # likes.append(liked)
    client = datastore.Client()
    key = client.key('like')
    toUpload = datastore.Entity(key)
    toUpload['username'] = flask.session['user']
    toUpload['clothingi'] = liked.image
    toUpload['clothings'] = liked.style
    client.put(toUpload)

def get_liked():
    #get all clothes from datastore where user has liked
    client = datastore.Client()
    result = []
    query = client.query(kind='like')
    query.add_filter("username", "=", flask.session['user'])
    for entity in query.fetch():
        result.append(user.Clothing(entity['clothingi'],entity['clothings']))
    return result

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
