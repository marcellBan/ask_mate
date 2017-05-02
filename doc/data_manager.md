# data_manager

loads and saves data to csv files

### load_data(*answers*=False)

If provided with *answers*=True parameter it will load the answers from the **answer.csv** otherwise it loads the questions form **question.csv** it returns a dictionary of dictionaries where the outer keys are the ids and the inner keys are the field names. All numeric values (including ids) are in numeric form.

### save_data(*data*, *answers*=False)
Same as with **load_data** it will save to **answer.csv** if provided with *answers*=True
and to **question.csv** otherwise.
The *data* parameter should be a dictionary of dictionaries like the one the **load_data** function returns.
