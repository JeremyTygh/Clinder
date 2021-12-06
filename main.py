import flask
from flask import Flask, jsonify, request, render_template
import user
import init

app = flask.Flask(__name__)
us = user.User()

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
    return flask.render_template('homepage.html', clothes=init.clothes, index=us.index)


@app.route('/profile_screen.html')
def profile():
    return flask.render_template('profile_screen.html')

#for accessing the like screen, all of the user's likes will be stored in an array called likes
@app.route('/like_screen.html')
def like():
    return flask.render_template('like_screen.html', likes=us.get_liked())

#for accessing the homepage, the list of all clothes is in variable clothes and the index is where in the list the page should start showing new clothes
@app.route('/homepage.html')
def home():
    return flask.render_template('homepage.html', clothes=init.clothes, index=us.index)
    # return flask.redirect("homepage.html", clothes=init.clothes, index=us.index)

#point javascript requests to these two listeners!
@app.route('/liked', methods=['POST','GET'])
def received_like():
    # clothingIndex = flask.request.form['clothingIndex']
    # us.add_like(init.clothes[clothingIndex])
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        response = request.get_json()
        us.add_like( init.clothes[int(response["imageAddress"])] )
        return 'OK', 200    
    #choose one - either send the index of the clothes or the clothing object itself
    #clothing = flask.request.form['clothing']
    #us.add_like(init.clothes[clothing])
    us.viewed_item()

@app.route('/notliked', methods=['POST','GET'])
def received_dislike():
    us.viewed_item()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)