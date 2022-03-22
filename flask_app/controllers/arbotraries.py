from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, arbotrary


@app.route('/view/<int:id>')
def view(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    arbotra = arbotrary.Arbotrary.get_arb_by_id(data)


    dt = {
        'id' : session['user_id']
    }
    logged_in_user = user.User.user_by_id(dt)

    visitors = arbotrary.Arbotrary.these_are_visitors(data)
    planter = user.User.users_tree_by_id(data)
    return render_template('view.html', user = logged_in_user, arbotra = arbotra, visitors = visitors, planter = planter)


@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id' : session['user_id']
    }
    logged_in_user = user.User.user_by_id(data)

    dt = {
        'id': id
    }
    arb = arbotrary.Arbotrary.get_arb_by_id(dt)
    return render_template('update.html', user = logged_in_user, arb = arb)


@app.route('/create')
def create():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id' : session['user_id']
    }
    logged_in_user = user.User.user_by_id(data)

    return render_template('create.html', user = logged_in_user)

@app.route('/plant', methods = ['POST'])
def plant():
    if 'user_id' not in session:
        return redirect('/')
    if not arbotrary.Arbotrary.validate(request.form):
        return redirect('/create')
    data = {
        'species' : request.form['species'],
        'location' : request.form['location'],
        'reason' : request.form['reason'],
        'date' : request.form['date'],
        'planter_id' : session['user_id'],
    }
    arbotrary.Arbotrary.create(data)
    return redirect('/dashboard')

@app.route('/mytrees')
def mytrees():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id' : session['user_id']
    }
    logged_in_user = user.User.user_by_id(data)
    trees = arbotrary.Arbotrary.grab_trees_by_id(data)
    return render_template('mytrees.html', user = logged_in_user, trees = trees)

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    arbotrary.Arbotrary.delete(data)
    return redirect('/mytrees')

@app.route('/yes/<int:id>')
def yes(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id' : session['user_id'],
        'id' : id
    }
    if not id in user.User.im_a_visitor(data):
        arbotrary.Arbotrary.visitors(data)
    return redirect(f'/view/{id}')

@app.route('/no/<int:id>')
def no(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id' : session['user_id'],
        'id' : id
    }
    user.User.delete_from_visits(data)
    return redirect(f'/view/{id}')


@app.route('/update/<int:id>', methods = ['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/')
    if not arbotrary.Arbotrary.validate(request.form):
        return redirect(f'/edit/{id}')

    data = {
        'species' : request.form['species'],
        'location' : request.form['location'],
        'reason' : request.form['reason'],
        'date' : request.form['date'],
    }
    arbotrary.Arbotrary.update(data)
    return redirect('/dashboard')