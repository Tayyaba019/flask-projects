
from flask import render_template,request,redirect,url_for
from model import User ,MyTask
from flask_login import login_user,logout_user,current_user,login_required

def app_routes(app,db,bcrypt): 
    @app.route('/home',methods=['GET','POST'])
    @login_required
    def home():
        if request.method == 'POST': 
            current_task = request.form.get('content')
            new_task = MyTask(content = current_task ,
                              user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            return redirect('/home')
        else: 
            tasks = MyTask.query.filter_by(user_id=current_user.id).order_by(MyTask.created).all()

            return render_template('home.html',tasks = tasks)
        
    # delete the task 
    @app.route('/delete/<int:id>')
    def delete(id:int): 
        delete_task = MyTask.query.get_or_404(id)
        try: 
            db.session.delete(delete_task)
            db.session.commit()
            return redirect(url_for("home")) 
        except Exception as e: 
            return f"ERROR:{e}"
        
    # edit the task 
    @app.route('/edit/<int:id>' , methods = ['GET','POST'])
    def edit(id:int): 
        task_edit = MyTask.query.get_or_404(id)
        if request.method == 'POST': 
            task_edit.content = request.form['content']
            try: 
                db.session.commit()
                return redirect(url_for('home'))
            except Exception as e: 
                return f"ERROR as {e}"
        else: 
            return render_template('edit.html' ,task_edit = task_edit)
        
    @app.route('/complete/<int:id>')
    def complete(id:int): 
        complete_task = MyTask.query.get_or_404(id)
        if complete_task.user_id == current_user.id: 
            complete_task.complete = 1 
            db.session.commit()
        return redirect(url_for('home'))

    @app.route('/undo/<int:id>')
    def undo(id:int): 
        undo_task = MyTask.query.get_or_404(id)
        if undo_task.user_id == current_user.id: 
            undo_task.complete = 0 
            db.session.commit()
        return redirect(url_for('home'))
     
    @app.route('/',methods = ['GET','POST'])
    def index(): 
        return render_template('index.html')
    
    @app.route('/signup',methods = ['GET','POST'])
    def signup():
        if request.method == 'GET': 
            return render_template('signup.html')
        elif request.method == 'POST': 
            username = request.form.get('username')
            password = request.form.get('password')

            hash_password = bcrypt.generate_password_hash(password)

            user = User(username = username,password = hash_password)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

    @app.route('/login',methods=['GET','POST'])
    def login(): 
        if request.method == 'GET': 
            return render_template('login.html')
        elif request.method == 'POST': 
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter(User.username == username).first()
            if bcrypt.check_password_hash(user.password ,password): 
                login_user(user)
                return redirect(url_for('home'))
            else: 
                return "failed"
            
    @app.route('/logout')
    def logout(): 
        logout_user()
        return redirect(url_for('index'))

    
