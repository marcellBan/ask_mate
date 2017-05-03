# vote

Handle downvoting and upvoting of questions and answers.

### downvote_question(*q_id*)

Decreases *vote_number* of the given question by one. **Redirect should depend on where we voted from**

### upvote_question(*q_id*)

Increases *vote_number* of the given question by one. **Redirect should depend on where we voted from**

### downvote_answer(*a_id*)

Decreases *vote_number* of the given answer by one. Redirect to the answers question page.

### upvote_answer(*a_id*)

Increases *vote_number* of the given answer by one. Redirect to the answers question page.