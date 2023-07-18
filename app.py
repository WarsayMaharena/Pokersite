from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, emit, SocketIO
import random
from string import ascii_uppercase
from create_database import User
user=User()
app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app)

@app.route("/", methods=["POST", "GET"])
def home():

    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        betting = request.form.get("betting")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name, betting=betting)
        
        if not betting:
            return render_template("home.html", error="Please enter a betting amount.", code=code, name=name)
        
        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name, betting=betting)
        
        room = code
        if create != False:
            room = user.generate_unique_code()
            print(room, "room numbe is here")

        elif user.room_exists(code)==False:
            return render_template("home.html", error="Room does not exist.", code=code, name=name, betting=betting)
        
        session["room"] = room
        session["name"] = name
        session["betting"] = betting
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room", methods=['POST', 'GET'])
def room():
    print("------------ENTERED A ROOM")
    room=session.get("room")
    name=session.get("name")
    NonExistent=user.room_exists(room)
    print("room:", room, "name", name, "noneexistant:", NonExistent)
    if room is None or name is None or NonExistent==False:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        bet = request.form.get('bet')
        check = request.form.get('check', False)
        fold = request.form.get('fold', False)
        print("-------------entered POST")
        if check == False:
            print("-------------PRESSED CHECK")   
    return render_template("room.html",code=room,name=name) #also add in messages.


@socketio.on("message")
def message(data):
    room=session.get("room")
    name=session.get("name")
    message=name+": "+data["data"]
    print("HELLLLLLLOOOOOOOOO")
    print(message)
    if user.room_exists(room) ==False:
        return
    
    content = {
        "name":session.get("name"), 
        "message": data["data"]
    }

    send(content, to=room)
    user.insert_comment(name,room,message)
    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room=session.get("room")
    name=session.get("name")
    if not room or not name:
        return
    if user.room_exists==False:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message":"has joined the room"}, to=room)
    session["playerpos"] = user.add_member(room)
    session["currPlayer"] = 1
    session["roundBet"] = 0
    print("playerpos", session["playerpos"], "current players turn=", session["currPlayer"])
    print(f"{name} has joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room=session.get("room")
    name=session.get("name")
    leave_room(room)

    if user.room_exists(room)==True:
        user.sub_member(room)
        if user.member_exists(room)==False:
            user.del_room(room)

    send({"name": name, "message":"has left the room"}, to=room)
    print(f"{name} has left the room {room}")


@socketio.on("updateCurrPlayer")
def updateCurrPlayer(currPlayer, betAmount=0):
    session["currPlayer"] = currPlayer
    print("Updatecurrplayer", session.get("currPlayer"))
    session["roundBet"] = session.get("roundBet") + betAmount
    print("Betamont: ", session.get("roundBet"))
    
    

#Currplayer is none for some reason need fix
@socketio.on("check")
def check():
    print("-------Entered check, playerpos: ", session.get("playerpos"), "currplayer: ", session.get("currPlayer"))
    room = session.get("room")
    if int(session.get("playerpos")) == int(session.get("currPlayer")):
        #Check if someone has raised before them: if raisedAmount > 0: betted - raisedAmount
        print("----Check IF STATEMENT")
        if session["currPlayer"] >= user.return_members(room):
            session["currPlayer"] = 1
        else:
            session["currPlayer"] = int(session.get("currPlayer")) + 1


        #Send currplayer to the rest of the players
        #This emit statement calls the socketio.on(updateCurrPlayer) function in the javascript code
        emit("updateCurrPlayer", {'data': session.get("currPlayer")}, to=room)


@socketio.on("fold")
def fold():
    room = session.get("room")
    if session.get("playerpos") == session.get("currPlayer"):
        pass


@socketio.on("bet")
def bet(betAmount):
    room = session.get("room")
    playerpos = session.get("playerpos")
    print(betAmount)
    amount = betAmount
    print("amount", amount)
    if session.get("playerpos") == session.get("currPlayer"):
        print(betAmount, playerpos, "PLAYERPOIS BETAMOUNT")
        emit("updateBet", {'data': betAmount, 'pos': playerpos}, to=room)


        
if __name__ == "__main__":
    socketio.run(app, debug=True)