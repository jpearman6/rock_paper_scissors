#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# **Initialization**
# Initialize the game score
score = {
    "user": 0,
    "api": 0,
    "draws": 0
}

# **Helper Functions**

# Determine the winner based on user and API choices
def determine_winner(user_choice, api_choice):
    global score
    if user_choice == api_choice:
        score["draws"] += 1
        return "Draw!"
    if user_choice == "rock":
        if api_choice == "scissors":
            score["user"] += 1
            return "You win!"
        else:
            score["api"] += 1
            return "You lose!"
    if user_choice == "paper":
        if api_choice == "rock":
            score["user"] += 1
            return "You win!"
        else:
            score["api"] += 1
            return "You lose!"
    if user_choice == "scissors":
        if api_choice == "paper":
            score["user"] += 1
            return "You win!"
        else:
            score["api"] += 1
            return "You lose!"

# **API Endpoints**

# Play the game
@app.route('/play', methods=['POST'])
def play():
    data = request.get_json()
    user_choice = data.get('choice')
    if user_choice not in ['rock', 'paper', 'scissors']:
        return jsonify(error="Invalid choice"), 400

    choices = ['rock', 'paper', 'scissors']
    api_choice = random.choice(choices)

    result = determine_winner(user_choice, api_choice)

    return jsonify(user_choice=user_choice, api_choice=api_choice, result=result)

# Get the current score
@app.route('/score', methods=['GET'])
def get_score():
    return jsonify(score)

# Restart the game by resetting the score
@app.route('/restart', methods=['PUT'])
def restart_game():
    global score
    score = {
        "user": 0,
        "api": 0,
        "draws": 0
    }
    return jsonify(message="Game score has been reset.", score=score)

# **Main Execution**
if __name__ == '__main__':
    app.run(debug=False)

