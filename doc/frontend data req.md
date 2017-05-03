#/, /sort
the needed form of data is: list of dictionaries

names and definitions:
question_list: the name of the list which contains dictionaries
    keys:
    question_id: id of the question
    title: title of the question
    message: the question itself
    vote_number: current standing of the vote (number)

#/q/id
list of dictionaries, disctionary keys are: qestion_id, message, vote_number

#/q/id/new-answer
needs the list of dict of questions, to display the correct question above the textbox