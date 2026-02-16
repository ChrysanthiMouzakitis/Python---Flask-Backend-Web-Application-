from datetime import date
from functools import wraps

from flask import (Flask, g, redirect, render_template, request, session,
                   url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from database import close_db, get_db
from flask_session import Session
from forms import (AddAdminForm, AdminLoginForm, ConfirmationForm,
                   DeleteAdminForm, FilterForm, LoginForm, PassChange2Form,
                   PassChangeForm, RegisterForm, ReviewFilterForm, ReviewForm,
                   UpdateAdminForm)

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "password"
app.config["SESSION_PERMANENT"] =False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#NOTES***********************************************************************
#admin login is user_id: derek
#               code: webdev23


@app.before_request
def logged_in_user():
    g.user = session.get("user_id", None)



def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None and g.admin is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view


def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for("admin_login", next=request.url))
        return view(**kwargs)
    return wrapped_view

@app.before_request
def logged_in_admin():
    g.admin = session.get("admin_id", None)

@app.route("/")
def index():
    db = get_db()
    user_id=session.get("user_id", " ")

    reviews = db.execute("""SELECT * FROM reviews""").fetchall()
    return render_template("main_page.html", reviews = reviews, user_id=user_id)

@app.route("/add_review", methods=["GET", "POST"])
@login_required
def add_review():
    form = ReviewForm()
    activity_ids =[]
    factcheck=False
    
    if form.validate_on_submit():
        activity_name = form.activity_name.data
        stars=form.stars.data
        review = form.review.data
        db = get_db()
        user_id = session.get("user_id", None)

        if stars=="⋆":
            star_num=1
        elif stars=="⋆⋆":
            star_num=2
        elif stars=="⋆⋆⋆":
            star_num=3
        elif stars=="⋆⋆⋆⋆":
            star_num=4
        elif stars=="⋆⋆⋆⋆⋆":
            star_num=5
    
        db.execute("""INSERT INTO reviews VALUES (?, ?, ?, ?, ?);""", (user_id, activity_name, stars, star_num, review))
        db.commit()
        return redirect(url_for('reviews'))
    
        
    return render_template("add_review.html",  form=form)


@app.route("/reviews", methods=["GET", "POST"])
def reviews():

    form=ReviewFilterForm()
    reviews={}
    ids={}

    if form.validate_on_submit():

        db=get_db()
        filter=form.filter.data

        # for dict in reviews:
        #     id=dict["activity_id"]
        #     name=dict["activity_name"]
        #     ids[name] = id

        if filter == "Rating low to high":
            reviews = db.execute("""SELECT * FROM reviews JOIN activities ON reviews.activity_name = activities.name
                                ORDER BY star_num;""" ).fetchall()

        elif filter == "Rating high to low":
            reviews = db.execute("""SELECT * FROM reviews JOIN activities ON reviews.activity_name = activities.name
                                    ORDER BY star_num DESC;""" ).fetchall()

        elif filter == "Activity A-Z":
            reviews = db.execute("""SELECT * FROM reviews JOIN activities ON reviews.activity_name = activities.name
                                    ORDER BY activities.name;""" ).fetchall()
        


    

    return render_template("reviews.html", reviews=reviews, ids=ids, form=form)
#activit(ies)and booking

@app.route("/activities", methods=["GET", "POST"])
def activities():
    db = get_db()
    form = FilterForm()
    
    activities=[]
    time_filter=""
    note=""
    
    if form.validate_on_submit():
        filter = form.filter.data
        time_filter=form.time_filter.data

        if time_filter < date.today():
            form.time_filter.errors.append("Sorry this date is in the past, please select another date to continue")
        
        else:
        
        
            if filter == "Price low to high":
                activities = db.execute("""SELECT *
                                        FROM activities JOIN dates ON dates.activity_id = activities.activity_id
                                            WHERE dates.date >= ? ORDER BY activities.price;""", (time_filter,)).fetchall()

            elif filter == "Price high to low":
                activities = db.execute("""SELECT * FROM activities JOIN dates ON dates.activity_id = activities.activity_id
                                        WHERE dates.date >= ? ORDER BY price DESC;""", (time_filter,)).fetchall()

            elif filter == "County A-Z":
                activities = db.execute("""SELECT * 
                                        FROM activities JOIN dates ON dates.activity_id = activities.activity_id
                                            WHERE dates.date >= ? ORDER BY county;""", (time_filter,)).fetchall()

            if activities ==[]:
                note="Sorry there are no activities available for this time period, please choose another date"



    
    return render_template("activities.html", activities=activities, form=form, note=note)

@app.route("/register", methods=["GET", "POST"])
def register():
    formR = RegisterForm()
    if formR.validate_on_submit():
        user_idR = formR.user_id.data
        passwordR = formR.password.data
        passwordR2 = formR.password2.data
        db= get_db()

        possible_clash = db.execute("""SELECT * FROM users
                                    WHERE user_id = ?;""", (user_idR, )).fetchone()

        if possible_clash is not None:
            formR.user_id.errors.append("Sorry this user id is already taken")
        else:
            db.execute("""INSERT INTO users (user_id, password)
                    VALUES(?,?);""", (user_idR, generate_password_hash(passwordR)))
            db.commit()
            return redirect(url_for("login"))
        
        
    return render_template("register.html", formR = formR)

@app.route("/login", methods=["GET", "POST"])
def login():

    formL = LoginForm()
    if formL.validate_on_submit():
        user_idL = formL.user_id.data
        passwordL = formL.password.data
        db= get_db()

        possible_clash = db.execute("""SELECT * FROM users
                                    WHERE user_id = ?;""", (user_idL, )).fetchone()

        if possible_clash is None:
            formL.user_id.errors.append("Sorry this user does not exist")

        elif not check_password_hash(possible_clash["password"], passwordL):
            formL.password.errors.append("Sorry, it looks like this password is incorrect")

        else:
            session.clear()
            session ["user_id"] = user_idL
            next_page = request.args.get("next")
            print(next_page)
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
        
    return render_template("login.html", formL = formL)

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    form = AdminLoginForm()
    if form.validate_on_submit():
        admin_id = form.admin_id.data
        
        code = form.code.data
        db= get_db()

        possible_clash = db.execute("""SELECT * FROM admins
                                    WHERE admin_id = ?;""", (admin_id, )).fetchone()

        if possible_clash is None:
            form.admin_id.errors.append("Sorry this user does not exist")

        # elif not check_password_hash(possible_clash["password"], password):
        #     form.password.errors.append("Sorry, it looks like this password is incorrect")

        elif code!= "webdev23":
            form.code.errors.append("Sorry this code is incorrect")

        else:
            session.clear()
            session ["admin_id"] = admin_id

            return redirect('admin_acts')
        
    return render_template("admin_login.html", form = form)

@app.route("/admin_acts")
@admin_required
def admin_acts():

    admin_id = session.get("admin_id", None)

    return render_template("admin_acts.html", admin_id=admin_id, note=" ")

@app.route("/delete_admin", methods=["GET","POST"])
def delete_admin():

    form=DeleteAdminForm()

    if form.validate_on_submit():
        factcheck=False
        activity_id= form.activity_id.data
        db=get_db()
        activity_ids = db.execute("""SELECT activity_id FROM activities;""").fetchall()

        for x in activity_ids:
            if activity_id==x[0]:
                factcheck=True
                break
            else:
                factcheck=False

        if not factcheck:
            form.activity_id.errors.append("Sorry this id does not match an existing activity")

        else:
            db.execute("""DELETE FROM activities WHERE activity_id=?;""", (activity_id,))
            db.commit()
            db.execute("""DELETE FROM dates WHERE activity_id=?;""", (activity_id,))
            db.commit()
            return render_template("admin_acts.html", note="Successful deletion!")
                
    return render_template("delete_admin.html", form=form)

@app.route("/add_admin", methods=["GET", "POST"])
def add_admin():

    form=AddAdminForm()

    if form.validate_on_submit():
        county=form.county.data
        category=form.category.data
        name=form.name.data
        date=form.date.data
        price=form.price.data
        pricenote= form.pricenote.data
        description = form.description.data
        image=form.image.data

        if date < date.today():
            form.date.errors.append("Sorry this date is in the past, please enter another one to continue")
        
        else:

            db=get_db()
            db.execute("""INSERT INTO activities (county, category, name, price, pricenote, description, image) VALUES (?,?,?,?,?,?,?);""",
                        (county, category, name, price, pricenote, description, image))
            db.commit()

            id=db.execute("""SELECT activity_id FROM activities WHERE name=?;""", (name,)).fetchone()
            print(id)
            id=id[0]
            print(id)

            db.execute("""INSERT INTO dates VALUES(?,?);""", (id, date))
            db.commit()

            return(render_template("admin_acts.html", note="Successful Addition"))
    
    return render_template("add_admin.html", form=form)

@app.route("/update_admin", methods=["GET", "POST"])
def update_admin():

    form=UpdateAdminForm()

    if form.validate_on_submit():

        activity_id=form.activity_id.data
        attribute=form.attribute.data
        print("HERE!!", attribute)
        new_value = form.new_value.data

        factcheck=False
        db=get_db()
        activity_ids = db.execute("""SELECT activity_id FROM activities;""").fetchall()

        for x in activity_ids:
            if activity_id==x[0]:
                factcheck=True
                break
            else:
                factcheck=False
        

        if not factcheck:
            form.activity_id.errors.append("Sorry this id does not match an existing activity")

        else:
            if attribute=="Date":
                db.execute("""UPDATE dates SET date=? WHERE activity_id=?;""", (new_value, activity_id))
                db.commit()

            elif attribute=="Name":
                db.execute("""UPDATE activities SET name=? WHERE activity_id=?;""",( new_value,activity_id))
                db.commit()

            elif attribute=="County":
                db.execute("""UPDATE activities SET county=? WHERE activity_id=?;""",( new_value,activity_id))
                db.commit()

            elif attribute=="Price":
                db.execute("""UPDATE activities SET price=? WHERE activity_id=?;""",( new_value,activity_id))
                db.commit()

            elif attribute=="Category":
                db.execute("""UPDATE activities SET category=? WHERE activity_id=?;""",( new_value,activity_id))
                db.commit()

            elif attribute=="Pricenote":
                db.execute("""UPDATE activities SET pricenote=? WHERE activity_id=?;""",( new_value,activity_id))
                db.commit()

            elif attribute=="Description":
                db.execute("""UPDATE activities SET description=? WHERE activity_id=?;""",( new_value,activity_id))
                db.commit()

            elif attribute=="Image":
                db.execute("""UPDATE activities SET image=? WHERE activity_id=?;""",( new_value,activity_id))
                db.commit()

            


            return render_template("admin_acts.html", note="Successful Activity Update")


    return render_template("update_admin.html", form=form)

@app.route("/logout")
@login_required
def logout():

    session.clear()
    return redirect(url_for("index"))

@app.route("/activity/<int:activity_id>")
def activity(activity_id):
    db = get_db()
    activities = db.execute("""SELECT * FROM activities WHERE activity_id =?;""", (activity_id,)).fetchone()
    category = activities["category"]
    print(category)

    other_activities=db.execute("""SELECT * FROM activities WHERE category = ? AND activity_id <> ?;""", (category, activity_id)).fetchall()
    return render_template("activity.html", activity=activities, other_activities=other_activities)

# #cart and save for later and add to cart

@app.route("/booked_activities")
@login_required
def booked_activities():
    if "cart" not in session:
        session["cart"]={}

    costs={}
    names ={}
    dates={}
    date_clash={}
    alert=""
    total=0
    db = get_db()

    for activity_id in session["cart"]:
        activity = db.execute("""SELECT * FROM activities WHERE activity_id =?;""", (activity_id,)).fetchone()
        name = activity["name"]
        names[activity_id] = name

        #cost=activity["pricenote"]
        

        cost_adult=activity["price"]
        cost_child = cost_adult/2
        
        num_adults=session["cart"][activity_id][0]
        #num_adults=int(num_adults)
        

        num_child=session["cart"][activity_id][1]
        #num_child=int(num_child)
        print(num_adults, num_child)

        total_activity=(cost_adult*num_adults)+(cost_child*num_child)

        total_activity=round(total_activity,2)

        costs[activity_id]=total_activity

        total+=float(total_activity)

        print(num_child, num_adults, total_activity, cost_adult, cost_child)

        

        join = db.execute("""SELECT * FROM activities JOIN dates 
                            ON activities.activity_id=dates.activity_id
                            WHERE activities.activity_id=?;""", (activity_id,)).fetchone()
        date = join["date"]
        dates[activity_id]=date

    total=round(total,2)
    for value in dates.values():
        if value in date_clash:
            date_clash[value]+=1
            alert="Be Careful, looks like some of these dates clash!"

        else:
            date_clash[value]=1
     
    
    return render_template("booked_activities.html", cart=session["cart"], names=names, dates=dates, costs=costs,total=total,alert=alert )


@app.route("/book_activity/<int:activity_id>", methods=["GET", "POST"])
@login_required
def book_activity(activity_id):

    form=ConfirmationForm()

    if "cart" not in session:
            session["cart"] = {}

    if activity_id in session["cart"]:
        return render_template("oops.html")

    if form.validate_on_submit():

        num_people1=form.num_people1.data
        num_people2=form.num_people2.data

        if "cart" not in session:
            session["cart"] = {}

        if activity_id not in session["cart"]:
            session["cart"][activity_id] = [num_people1, num_people2]
            

    
        #say its already booked
    
        return redirect(url_for("booked_activities"))

    return render_template("confirmation.html", form=form)

@app.route("/edit_people/<int:activity_id>", methods=["GET", "POST"])
def edit_people(activity_id):

    session["cart"].pop(activity_id)

    return redirect(url_for('book_activity', activity_id=activity_id))
     

@app.route("/faved_activities")
def faved_activities():
    if "favs" not in session:
        session["favs"]={}

    names ={}
    ids={}
    db = get_db()

    for activity_id in session["favs"]:
        activity = db.execute("""SELECT * FROM activities WHERE activity_id =?;""", (activity_id,)).fetchone()

        name = activity["name"]
        names[activity_id] = name
        
        id = activity["activity_id"]
        ids[activity_id] = id
    
    return render_template("favourites.html", favs=session["favs"], names=names, ids=ids)

@app.route("/fav_activity/<int:activity_id>")
def fav_activity(activity_id):

    if "favs" not in session:
        session["favs"] = {}

    if activity_id not in session["favs"]:
        session["favs"][activity_id] = "Saved"

    
        #say its already booked
    
    return redirect(url_for("faved_activities"))

@app.route("/move_to_cart/<int:activity_id>")
@login_required
def move_to_cart(activity_id):

    # if "cart" not in session:
    #     session["cart"] ={}

    # if activity_id not in session["cart"]:
    #     session["cart"][activity_id] = "BOOKED"
    
    

    del session["favs"][activity_id]

    return redirect(url_for("book_activity", activity_id = activity_id))

@app.route("/move_to_favs/<int:activity_id>")
def move_to_favs(activity_id):

    if "favs" not in session:
        session["favs"] ={}

    if activity_id not in session["favs"]:
        session["favs"][activity_id] = "SAVED"
    

    session["cart"].pop(activity_id)

    return redirect(url_for("booked_activities"))

@app.route("/remove_cart/<int:activity_id>")
def remove_cart(activity_id):

    session["cart"].pop(activity_id)

    return redirect(url_for("booked_activities"))

@app.route("/remove_fav/<int:activity_id>")
def remove_fav(activity_id):

    session["favs"].pop(activity_id)

    return redirect(url_for("faved_activities"))

@app.route("/account")
@login_required
def account():
    user_id = session.get("user_id"," ")

    
    
    return render_template("account.html", user_id=user_id)

@app.route("/change_password", methods=["GET", "POST"])
def change_password():

    form=PassChangeForm()

    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db= get_db()

        possible_clash = db.execute("""SELECT * FROM users
                                    WHERE user_id = ?;""", (user_id, )).fetchone()

        if possible_clash is None:
            form.user_id.errors.append("Sorry this user does not exist")

        elif not check_password_hash(possible_clash["password"], password):
            form.password.errors.append("INCORRECT PASSWORD")

        else:
            return redirect('change_form')

    return render_template("change_pass.html", form=form)



@app.route("/change_form", methods=["GET", "POST"])
def change_form():

    form=PassChange2Form()

    if form.validate_on_submit():
        user_id=session.get("user_id", None)

        password=form.password.data

        db=get_db()
        db.execute("""UPDATE users SET password=? WHERE user_id=?;""", (generate_password_hash(password), user_id))
        db.commit()
        
        return redirect(url_for("account"))
    
    return render_template("change_pass2.html", form=form)

@app.route("/delete1")
@login_required
def delete1():

    return render_template("delete1.html")

@app.route("/delete2")
@login_required
def delete2():
    
    user_id=session.get('user_id', None)
    db=get_db()
    db.execute("""DELETE  FROM users WHERE user_id=?;""", (user_id,))
    db.commit()
    session.clear()
    return redirect(url_for('index'))