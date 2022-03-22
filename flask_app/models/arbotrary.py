from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Arbotrary:
    db = 'exams'
    def __init__(self, data):
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.date = data['date']
        self.planter_id = data['planter_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.visitor = None

    @classmethod
    def create(cls, data):
        query = 'INSERT INTO arbotraries (species, location, reason, date, planter_id) VALUES (%(species)s, %(location)s, %(reason)s, %(date)s, %(planter_id)s);'
        connectToMySQL(Arbotrary.db).query_db(query, data)

    @classmethod
    def arbotrary_and_planter(cls):
        query = 'select * , count(arbotrary_id) as num  from arbotraries left  join  visitors on arbotraries.id = visitors.arbotrary_id join users on users.id = arbotraries.planter_id group by arbotraries.id;'
        results = connectToMySQL(Arbotrary.db).query_db(query)
        
        all_arbotraries = []
        for arbotra in results:
            arbotrary_instance = cls(arbotra)
            dt ={
                'id' : arbotra['users.id'],
                'first_name' : arbotra['first_name'],
                'last_name' : arbotra['last_name'],
                'email' : arbotra['email'],
                'password' : arbotra['password'],
                'created_at' : arbotra['users.created_at'],
                'updated_at' : arbotra['users.updated_at'],
            }
            arbotrary_instance.visitor = arbotra['num']
            one_user = user.User(dt)
            arbotrary_instance.user = one_user
            all_arbotraries.append(arbotrary_instance)
        return all_arbotraries

    @classmethod
    def get_arb_by_id(cls, data):
        query = 'SELECT * FROM arbotraries WHERE id = %(id)s;'
        result = connectToMySQL(Arbotrary.db).query_db(query,data)
        if len(result) == 0:
            return None
        else:
            return cls(result[0])

    @classmethod
    def grab_trees_by_id(cls, data):
        query = 'SELECT * FROM arbotraries WHERE planter_id = %(id)s;'
        result = connectToMySQL(Arbotrary.db).query_db(query,data)
        trees = []       
        for tree in result:
            trees.append(cls(tree))
        return trees
        
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM arbotraries WHERE id = %(id)s"
        connectToMySQL(Arbotrary.db).query_db(query, data)


    @classmethod
    def these_are_visitors(cls, data):
        query = 'SELECT * from arbotraries LEFT JOIN visitors ON arbotraries.id = visitors.arbotrary_id LEFT JOIN users ON users.id = visitors.user_id WHERE arbotraries.id = %(id)s;'
        results = connectToMySQL(Arbotrary.db).query_db(query, data)
        all_visitors = []
        for visitor in results:
            arbotrary_instance = cls(visitor)
            dt ={
                'id' : visitor['users.id'],
                'first_name' : visitor['first_name'],
                'last_name' : visitor['last_name'],
                'email' : visitor['email'],
                'password' : visitor['password'],
                'created_at' : visitor['users.created_at'],
                'updated_at' : visitor['users.updated_at'],
            }
            one_user = user.User(dt)
            arbotrary_instance.user = one_user
            all_visitors.append(arbotrary_instance)
        return all_visitors

    @classmethod
    def visitors(cls, data):
        query = 'INSERT INTO visitors (user_id, arbotrary_id) VALUES (%(user_id)s, %(id)s);'
        result = connectToMySQL(Arbotrary.db).query_db(query, data)
        return result

    @classmethod
    def update(cls, data):
        query = 'UPDATE arbotraries set species = %(species)s, location = %(location)s, reason = %(reason)s, date = %(date)s WHERE arbotraries.id = %(id)s;'
        connectToMySQL(Arbotrary.db).query_db(query, data)




    @staticmethod
    def validate(form):
        valid = True
        if len(form['species']) < 5:
            flash('species must contain at least 5 characters')
            valid = False
        if len(form['location']) < 2:
            flash('please enter a valid location')
            valid = False
        if len(form['reason']) < 5 or len(form['reason']) > 50:
            flash('reason must be 5 to 50 characters long')
            valid = False
        if len(form['date']) < 1:
            flash('please input date')
            valid = False
        return valid