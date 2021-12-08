import flask
from flask import Flask, jsonify, request, render_template
import user
import init
from google.cloud import datastore

app = flask.Flask(__name__)
app.secret_key = b'oaijrwoizsdfmdfgdfyrehfghf34foinmzsdv98j234ijefjieojEFIuhEhefiueuieuheuiheu8'
userList = {} #a list of all users in the system. added to upon receiving a valid connection. never shrinks, resets on startup.

#uncomment these lines to verify that things get added to datastore!
#us.add_like(init.clothes[0])
#us.viewed_item()
#us.viewed_item()
#us.viewed_item()
#for l in us.get_liked():
#    print(l)

@app.route('/')
def root():
    # use render_template to convert the template code to HTML.
    # this function will look in the templates/ folder for your file.
    # return flask.render_template('homepage.html', page_title='Main Page')
    # if flask.session.get('user') is None:
    #     return flask.render_template('signin.html')
    # return flask.render_template('homepage.html', clothes=init.clothes, index=userList[flask.session['user']].index)

    user = flask.session.get('user', None)
    # if flask.session.get('user') is None:
    if user:
        return flask.render_template('homepage.html', clothes=init.clothes, index=userList[flask.session['user']].index)
        # return flask.render_template('signin.html')
    return flask.render_template('signin.html')
    # return flask.render_template('homepage.html', clothes=init.clothes, index=userList[flask.session['user']].index)
    # return flask.redirect("homepage.html", clothes=init.clothes, index=us.index)


@app.route('/profile_screen.html')
def profile():
    if flask.session.get('user') is None:
        return flask.render_template('signin.html')
    return flask.render_template('profile_screen.html', username=flask.session['user'])

#for accessing the like screen, all of the user's likes will be stored in an array called likes
@app.route('/like_screen.html')
def like():
    if flask.session.get('user') is None:
        return flask.render_template('signin.html')
    return flask.render_template('like_screen.html', likes=userList[flask.session['user']].get_liked())

#for accessing the homepage, the list of all clothes is in variable clothes and the index is where in the list the page should start showing new clothes
@app.route('/homepage.html')
def home():
    user = flask.session.get('user', None)
    # if flask.session.get('user') is None:
    if user:
        return flask.render_template('homepage.html', clothes=init.clothes, index=userList[flask.session['user']].index)
        # return flask.render_template('signin.html')
    return flask.render_template('signin.html')
    # return flask.render_template('homepage.html', clothes=init.clothes, index=userList[flask.session['user']].index)
    # return flask.redirect("homepage.html", clothes=init.clothes, index=us.index)

#for sending the sign in screen
@app.route('/signin.html')
def signin():
    return flask.render_template('signin.html')

#for sending the sign up screen
@app.route('/signup.html')
def signup():
    return flask.render_template('signup.html')

#for handlng login requests - send username and password through json post request
@app.route('/login', methods=['POST'])
def login():
    response = request.get_json()
    username = response["username"]
    password = response["password"]
    client = datastore.Client()
    print(username + " " + password)

    query = client.query(kind = 'user')
    query.add_filter("username", "=", username)
    pw = 'password'
    index = 0
    for entity in query.fetch(): #fetch the entity that has the user's username
        pw = entity['password']
        index = entity['index']

    if hash(password) == pw: #pw on datastore should be hashed, so compare hashes
        flask.session['user'] = username #set session username, allowing access to other pages
        userList[username] = user.User(username, index) #add user to the userlist
        return flask.redirect('/')
    
    return flask.render_template('signin.html', invalid=True) #return an invalid flag when passwords do not match
    
#for handling register requests - send username and password through json post request
@app.route('/register', methods=['POST'])
def register():
    response = request.get_json()
    username = response["username"]
    password = response["password"]

    client = datastore.Client()
    query = client.query(kind = 'user')
    query.add_filter("username", "=", username) #query existing users with that username
    if query.fetch().num_results > 0: #if there is any result then the username already exists
        return flask.render_template('signup.html', invalid=True) #return an invalid flag when user already exists

    key = client.key('user', username)
    toUpload = datastore.Entity(key)
    toUpload['username'] = username
    toUpload['password'] = hash(password) #hash the password
    toUpload['index'] = 0
    client.put(toUpload) #push user data to datastore

    flask.session['user'] = username #set session username, allowing access to other pages
    userList[username] = user.User(username) #add user to the userlist
    return flask.redirect('/')

#for handling clicks of the like button
@app.route('/liked', methods=['POST','GET'])
def received_like():
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        response = request.get_json()
        userList[flask.session['user']].add_like( init.clothes[int(response["imageAddress"])] )
        return 'OK', 200

    userList[flask.session['user']].viewed_item()

#for handling clicks of the dislike button
@app.route('/notliked', methods=['POST','GET'])
def received_dislike():
    userList[flask.session['user']].viewed_item()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
