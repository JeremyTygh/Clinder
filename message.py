import datetime
import flask
from google.cloud import datastore

def clean(s):
    """Return a string w/ angle brackets, endlines, & tab characters removed."""

    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('\n', ' ')
    s = s.replace('\t', ' ')
    s = s.strip()
    if len(s) > 100:
        s = s[:100]

    return s



# def message_to_entity(message):


# def entity_to_message(entity):


class Message():
    """An object representing a single chat message."""

    def __init__(self, user, text, time=None):
        """Initialize a message for named user."""

        self.user = user
        self.text = text

        if time:
            self.time = time
        else:
            self.time = datetime.datetime.now()


    def get_formatted_time(self):
        """Return this messages's time as a 'YYYYMMDD HH:MM:SS' string."""

        return self.time.strftime('%Y%m%d %H:%M:%S')


    def to_html(self):
        """Convert this message to an HTML div."""
        
        outputDiv = '<div class="Message">%s (%s): %s</div>'
        span = '<span class="%s">%s</span>'
        timeSpan = span % ('Time', self.get_formatted_time())
        userSpan = span % ('User', self.user)
        textSpan = span % ('Text', self.text)
        return outputDiv % (timeSpan, userSpan, textSpan)


    def __str__(self):
        """Return a simple formatted string with the message contents."""

        return '%s (%s): %s' % (self.get_formatted_time(), self.user, self.text)
    

    def __lt__(self, other):
        return self.time < other.time


    def __gt__(self, other):
        return self.time > other.time
    

    def __eq__(self, other):
        return self.time == other.time
    

    def __ne__(self, other):
        return self.time != other.time
    

    def __le__(self, other):
        return self.time <= other.time
    

    def __ge__(self, other):
        return self.time >= other.time


class ChatManager():
    """A class for managing chat messages."""

    def get_client(self):
        return datastore.Client()

    def create_a_message(self, msg):
        client = datastore.Client() # self.get_client()
        # with client.transaction():
        key = client.key('message')
        # return datastore.Entity(key)

        message = datastore.Entity(key=key)

        message.update(
            {
                "user": msg.user,
                "text": msg.text,
                "time": msg.time,
            }
        )

        client.put(message)

    # def retrieve_message(self, id):
    #     client = self.get_client()
    #     key = client.key('an_entity_type_name', int(id))
    #     return client.get(key)

    # def update_message(self, message):
    #     client = self.get_client()
    #     client.put(message)

    def delete_message(self):
        client = self.get_client()
        key = client.key('message')
        client.delete(key)

    def get_messages(self):
        result = []
        client = self.get_client()
        query = client.query(kind='message')
        for entity in query.fetch():
            result.append(entity)
        return result


    # def show_messages():
    #     messages_list = get_messages()
    #     return flask.render_template('index.html', messages=messages_list)

    def __init__(self):
        """Initialize the ChatManager with a new list of messages."""
        # client = self.get_client()
        # self.messages = []
        # self.messages = self.get_messages()


    def add_message(self, msg):
        """Add a message to our messages list."""

        self.create_a_message(msg)
        # message = self.create_a_message(msg) #data
        # message['user'] = msg.user
        # message['text'] = msg.text
        # message['time'] = msg.time
        # self.update_message(message) #data

        # self.messages.append(msg)    

        # self.messages.sort()


    def create_message(self, user, text):
        """Create a new message with the current timestamp."""

        self.add_message(Message(clean(user), clean(text)))


    def get_messages_output(self):
        """Return the current message contents as a plain text string."""

        messages = self.get_messages()  
        my_messages = []

        for msg in messages:
            my_msg = Message(msg['user'], msg['text'], msg['time'])
            my_messages.append(my_msg)

        result = ''
        for msg in my_messages:
            result += str(msg)
            result += '\n'
        return result


    def get_messages_html(self):
        """Return the current message contents as HTML."""

        messages = self.get_messages()  
        my_messages = []

        for msg in messages:
            my_msg = Message(msg['user'], msg['text'], msg['time'].replace(tzinfo=None))
            my_messages.append(my_msg)

        result = ''
        for msg in my_messages:
            result += msg.to_html()
            result += '\n'
        return result


    def clear_messages_before(self, time):
        """Remove all messages prior to a given time."""
        messages = self.get_messages()  
        my_messages = []

        for msg in messages:
            my_msg = Message(msg['user'], msg['text'], msg['time'].replace(tzinfo=None))
            my_messages.append(my_msg)

        while len(my_messages) > 0 and my_messages[0].time < time:
            # id = flask.request.values['id']
            self.delete_message()
            # self.messages.pop(0)

