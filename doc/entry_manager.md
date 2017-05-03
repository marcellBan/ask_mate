# entry_manager

creates and deletes questions and answers using **data_manager.py**

### add_question()

Renders a question form if method is *GET* or the input was incorrect, otherwise creates a new question dictionary and adds it to **question.csv**.

### add_answer(*q_id*)

Renders an answer form and a question with ID: *q_id* if method is *GET* or the input was incorrect, otherwise creates a new answer dictionary and adds it to **answer.csv**