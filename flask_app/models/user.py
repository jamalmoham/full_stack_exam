from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'exams'
    def __init__ (self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sighter = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(firstname)s, %(lastname)s, %(email)s, %(password)s);'
        connectToMySQL(User.db).query_db(query, data)

    @classmethod
    def user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(User.db).query_db(query, data)
        if len(result) < 1:
            return None
        return cls(result[0])

    @classmethod
    def user_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL(User.db).query_db(query, data)
        if len(result) < 1:
            return None
        user = cls(result[0])
        return user

    @classmethod
    def user_all_emails(cls):
        query = 'SELECT email FROM users;'
        results = connectToMySQL(User.db).query_db(query)
        print(results)
        all_emails = []
        for email in results:
            all_emails.append(email)
        return all_emails  

    @classmethod
    def all_sightings_by_id(cls):
        query = 'SELECT * FROM users LEFT JOIN sightings ON users.id = sightings.reporter_id;'
        results = connectToMySQL(User.db).query_db(query)
        
        all_sights = []
        for user in results:
            user_instance = cls(user)
            dt ={
                'id' : user['sightings.id'],
                'location' : user['location'],
                'what_happened' : user['what_happened'],
                'date' : user['date'],
                'num_sasquatches' : user['num_sasquatches'],
                'reporter_id' : user['reporter_id'],
                'created_at' : user['sightings.created_at'],
                'updated_at' : user['sightings.updated_at'],
            }
            one_sight = None
            user_instance.sighter = one_sight
            all_sights.append(user_instance)
            print(user_instance)
        return all_sights

    @classmethod
    def im_a_visitor(cls, data):
        query = 'SELECT * FROM visitors WHERE user_id = %(user_id)s and arbotrary_id = %(id)s;'
        results = connectToMySQL(User.db).query_db(query, data)
        visitor = []
        for i in results:
            visitor.append( i['arbotrary_id'])    
        return visitor

    @classmethod
    def delete_from_visits(cls, data):
        query = 'delete from visitors where user_id = %(user_id)s and arbotrary_id = %(id)s;'
        connectToMySQL(User.db).query_db(query, data)

    @classmethod
    def users_tree_by_id(cls, data):
        query = 'SELECT * FROM users JOIN arbotraries ON arbotraries.planter_id = users.id where arbotraries.id = %(id)s;'
        results = connectToMySQL(User.db).query_db(query, data)
        return cls(results[0])

        

    @staticmethod
    def user_validation(form):
        valid = True
        if len(form['firstname']) < 2:
            flash('Please enter a valid First Name', 'register')
            valid = False
        
        if len(form['lastname']) < 2:
            flash('Please enter a valid Last Name', 'register')
            valid = False
        
        if len(form['email']) < 1:
            flash('Email feild cannot be empty', 'register')
            valid = False
        
        if not EMAIL_REGEX.match(form['email']):
            flash('Please enter a valid Email address', 'register')
            valid = False
        
        if len(form['password']) < 8 or len(form['password']) > 20:
            flash('Password must be 8 to 20 characters long', 'register')
            valid = False
        
        emailcheck = User.user_all_emails()
        emailcount = 0        
        for email in emailcheck:
            if form['email'] == email['email']:
                emailcount+=1
        if emailcount > 0:
            flash('Email is associated with an account already', 'register')
            valid = False
        
        if form['confirm-password'] != form['password']:
            flash('Passwords does not match', 'register')
            valid = False
        
        # checks for numbers in password
        numlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        numcount = 0
        for num in form['password']:
            for i in numlist:
                if i == num:
                    numcount+=1
        if numcount < 1:
            flash('Password must contain at least one number', 'register')
            valid = False
        #-----------ends here-----------

        # checks for upper case letters in password
        count = 0
        for i in form['password']:
            if i.isupper():
                count+=1
        if count < 1:
            flash('Password must contain at least one Upper case', 'register')
            valid = False
        return valid