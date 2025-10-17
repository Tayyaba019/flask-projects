from flask import request, render_template, flash, redirect, url_for,Response
from datetime import datetime, date
from models import Expense
import csv
import io
from models import User
from flask_login import login_user ,logout_user ,login_required,current_user




# ✅ New imports for Pie Chart
import matplotlib
matplotlib.use('Agg')  # Flask server ke liye non-GUI backend
import matplotlib.pyplot as plt
import io
import base64
from collections import defaultdict


def register_routes(db, app,bcrypt):  

    categories = ['Food', 'Health', 'Transport', 'Rent', 'Utilities']

    # helper function 
    def parse_date_or_none(s: str): 
        if not s:
            return None 
        try: 
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError: 
            return None
        
    @app.route('/')
    def home(): 
        return render_template('home.html')
    
    @app.route('/signup',methods = ['GET','POST'])
    def signup(): 
        if request.method == 'GET': 
            return render_template('signup.html')
        elif request.method == 'POST': 
            username = request.form.get('username')
            password = request.form.get('password')

            hash_password = bcrypt.generate_password_hash(password)
            
            new_user = User(username = username , password = hash_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        
    @app.route('/login',methods = ['GET','POST'])
    def login(): 
        if request.method == 'GET': 
            return render_template('login.html')
        elif request.method == 'POST': 
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter(User.username == username).first()
            if bcrypt.check_password_hash(user.password ,password): 
                login_user(user)
                return redirect(url_for('dashboard'))
            else: 
                flash("Invalid credentials", "error")
        return render_template('login.html')
    
    @app.route('/logout')
    def logout(): 
        logout_user()
        return redirect(url_for('home'))
            

    @app.route('/dashboard')
    @login_required
    def dashboard():
        user_expenses = Expense.query.filter_by(user_id=current_user.id).all()

        total_expenses = sum(e.amount for e in user_expenses)
        total_entries = len(user_expenses)

        # Calculate current month’s total
        from datetime import datetime
        current_month = datetime.now().month
        monthly_expenses = sum(
            e.amount for e in user_expenses if e.date.month == current_month
        )

        return render_template(
            'dashboard.html',
            user=current_user,
            total_expenses=total_expenses,
            monthly_expenses=monthly_expenses,
            total_entries=total_entries
        )





    @app.route('/view')
    def view(): 
        expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()

        total = round(sum(e.amount for e in expenses), 2)

        return render_template(
            'view.html',                    
            expenses=expenses
            

        )

        
   

    @app.route('/index')
    def index(): 
        # 🟩 Reading query string from URL (GET parameters)
        start_str = (request.args.get("start") or " ").strip()
        end_str = (request.args.get("end") or " ").strip()
        selected_category = (request.args.get("category") or "").strip()

        # 🟩 Parse query string into proper date objects
        start_date = parse_date_or_none(start_str)
        end_date = parse_date_or_none(end_str) 

        # 🟥 Validation: End date should not be before start date
        if start_date and end_date and end_date < start_date:
            flash("End date cannot be before start date", "error")
            start_date = end_date = None 
            start_str = end_str = ""

        # 🟩 Build query dynamically based on filters
        q = Expense.query 
        if start_date: 
            q = q.filter(Expense.date >= start_date)
        if end_date: 
            q = q.filter(Expense.date <= end_date)
        if selected_category: 
            q = q.filter(Expense.category == selected_category)

        # 🟩 Fetch filtered results
        expenses = q.order_by(Expense.date.desc(), Expense.id.desc()).all()
        total = round(sum(e.amount for e in expenses), 2)

        # 🟦 Pie chart ke liye category wise total calculate karna
        category_totals = defaultdict(float)
        for e in expenses:
            category_totals[e.category] += e.amount

        # 🟦 Matplotlib pie chart banana
        chart_url = None
        if category_totals:
            fig, ax = plt.subplots()
            ax.pie(
                category_totals.values(), 
                labels=category_totals.keys(), 
                autopct='%1.1f%%', 
                startangle=90
            )
            ax.axis('equal')  # perfect circle shape

            # 🟦 Chart ko memory mein save karna (not file)
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            chart_url = base64.b64encode(img.getvalue()).decode()
            plt.close(fig)

               # 🧠 ====> ADD BELOW CODE to generate daily total chart
        import matplotlib
        matplotlib.use('Agg')  # Use non-GUI backend (important for Flask)
        

                # 🟩 Daily Total Bar Chart
        daily_totals = defaultdict(float)
        for e in expenses:
            daily_totals[e.date] += e.amount

        # Sort by date
        sorted_dates = sorted(daily_totals.keys())
        amounts = [daily_totals[d] for d in sorted_dates]

        # Create bar chart
        plt.figure(figsize=(6,4))
        plt.bar(sorted_dates, amounts)
        plt.title('Daily Expense Totals')
        plt.xlabel('Date')
        plt.ylabel('Total Amount')
        plt.xticks(rotation=45)

        # Save to memory as base64
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        daily_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()

        

        

        # 🟩 Render template with all data
        return render_template(
            'index.html', 
            categories=categories,
            today=date.today().isoformat(),                    
            expenses=expenses, 
            total=total,
            start_str=start_str, 
            end_str=end_str,
            selected_category=selected_category,
            chart_url=chart_url , # 🟦 Sending chart to template
            daily_chart=daily_chart  # 👈 add this line
        )

    @app.route('/add', methods=['GET', 'POST'])
    def add():  
        if request.method == 'GET': 
            return render_template('add.html',categories=categories, today=date.today().isoformat())
        elif request.method == 'POST':
            description = request.form.get('description')
            amount = request.form.get('amount')
            date_val = request.form.get('date')
            category = request.form.get('category')

            print("Form received:", description, amount, category, date_val) 

            if not description or not amount or not category:
                flash("Please fill description, amount or category", 'error') 
                return render_template('add.html')
            try: 
                amount = float(amount)
                if amount <= 0: 
                    raise ValueError
            except ValueError: 
                flash('Amount must be a positive number', 'error')
                return redirect(url_for('index'))
            try: 
                d = datetime.strptime(date_val, "%Y-%m-%d") if date_val else date.today()
            except ValueError: 
                d = date.today()

            e = Expense(description=description, amount=amount, category=category, date=d, user_id=current_user.id)
            db.session.add(e)
            db.session.commit()

            print("Expense saved to DB ✅")

            flash("Expenses added", "success")
            return render_template('add.html')
    
    @app.route('/delete/<id>', methods=['POST'])
    def delete(id): 
        e = Expense.query.get_or_404(id)
        db.session.delete(e)
        db.session.commit()
        flash("Expenses deleted", 'success')
        return render_template('view.html')
    
    @app.route('/edit/<id>',methods =['GET'])
    def edit(id): 
        e= Expense.query.get_or_404(id)

        return render_template('edit.html',expense = e,today= date.today().isoformat(),categories=categories)
    

    @app.route('/edit/<id>' ,methods=['POST'])
    def edit_expense(id): 
        e= Expense.query.get_or_404(id)

        description = request.form.get('description')
        amount = request.form.get('amount')
        category = request.form.get('category')
        date_str = request.form.get('date')

        if not description or not amount or not category:
            flash("Please fill description, amount or category", 'error') 
            return redirect(url_for("edit", id = e.id))
        try: 
            amount = float(amount)
            if amount <= 0: 
                raise ValueError
        except ValueError: 
            flash('Amount must be a positive number', 'error')
            return redirect(url_for("edit", expense_id = e.id))
        
        try: 
            d = datetime.strptime(date_str, "%Y-%m-%d") if date_str else date.today()
        except ValueError: 
            d = date.today()

        e.description = description 
        e.amount = amount 
        e.category = category 
        e.date = d 

        db.session.commit()
        flash("updated Expenese","success")
        return redirect(url_for('index'))


    @app.route('/export.csv')
    def export_csv(): 
        start_str = (request.args.get("start") or " ").strip()
        end_str = (request.args.get("end") or " ").strip()
        selected_category = (request.args.get("category") or "").strip()

        # 🟩 Parse query string into proper date objects
        start_date = parse_date_or_none(start_str)
        end_date = parse_date_or_none(end_str) 

        q = Expense.query 
        if start_date: 
            q = q.filter(Expense.date >= start_date)
        if end_date: 
            q = q.filter(Expense.date <= end_date)
        if selected_category: 
            q = q.filter(Expense.category == selected_category)
        
        expenses = q.order_by(Expense.date,Expense.id).all()
        lines = ["date,description,category,amount"]

        for e in expenses: 
            lines.append(f"{e.date.strftime('%m/%d/%Y')},{e.description},{e.category},{e.amount:.2f}")
        csv_data = '\n'.join(lines)

        filename = "Expenses_Report.csv"

        return Response( 
            csv_data, 
            headers = {
                "Content-Type":"text/csv",
                "Content-Disposition": f"attachment; filename={filename}"


            }
        )




    
        