
DROP TABLE IF EXISTS question;

CREATE TABLE question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text
);


DROP SEQUENCE IF EXISTS question_id_seq;

CREATE SEQUENCE question_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE question_id_seq OWNED BY question.id;

ALTER TABLE ONLY question ALTER COLUMN id SET DEFAULT nextval('question_id_seq'::regclass);


COPY question (id, submission_time, view_number, vote_number, title, message, image) FROM stdin;
10	2017-05-18 19:48:26	2	0	How to query data stored in Hive table using SparkSession of Spark2?	I am trying to query data stored in Hive table from Spark2. Environment: 1.cloudera-quickstart-vm-5.7.0-0-vmware 2. Eclipse with Scala2.11.8 plugin 3. Spark2 and Maven under\r\n\r\nI did not change spark default configuration. Do I need configure anything in Spark or Hive?\r\n\r\nCode\r\n\r\nimport org.apache.spark._\r\nimport org.apache.spark.sql.SparkSession\r\nobject hiveTest {\r\n def main (args: Array[String]){\r\n   val sparkSession = SparkSession.builder.\r\n      master("local")\r\n      .appName("HiveSQL")\r\n      .enableHiveSupport()\r\n      .getOrCreate()\r\n\r\n  val data=  sparkSession2.sql("select * from test.mark")\r\n}\r\n}\r\nGetting error\r\n\r\n16/08/29 00:18:10 INFO SparkSqlParser: Parsing command: select * from test.mark\r\nException in thread "main" java.lang.ExceptionInInitializerError\r\n    at org.apache.spark.sql.hive.HiveSharedState.metadataHive$lzycompute(HiveSharedState.scala:48)\r\n    at org.apache.spark.sql.hive.HiveSharedState.metadataHive(HiveSharedState.scala:47)\r\n    at org.apache.spark.sql.hive.HiveSharedState.externalCatalog$lzycompute(HiveSharedState.scala:54)\r\n    at org.apache.spark.sql.hive.HiveSharedState.externalCatalog(HiveSharedState.scala:54)\r\n    at org.apache.spark.sql.hive.HiveSessionState.catalog$lzycompute(HiveSessionState.scala:50)\r\n    at org.apache.spark.sql.hive.HiveSessionState.catalog(HiveSessionState.scala:48)\r\n    at org.apache.spark.sql.hive.HiveSessionState$$anon$1.<init>(HiveSessionState.scala:63)\r\n    at org.apache.spark.sql.hive.HiveSessionState.analyzer$lzycompute(HiveSessionState.scala:63)\r\n    at org.apache.spark.sql.hive.HiveSessionState.analyzer(HiveSessionState.scala:62)\r\n    at org.apache.spark.sql.execution.QueryExecution.assertAnalyzed(QueryExecution.scala:49)\r\n    at org.apache.spark.sql.Dataset$.ofRows(Dataset.scala:64)\r\n    at org.apache.spark.sql.SparkSession.sql(SparkSession.scala:582)\r\n    at hiveTest$.main(hiveTest.scala:34)\r\n    at hiveTest.main(hiveTest.scala)\r\nCaused by: java.lang.IllegalArgumentException: requirement failed: Duplicate SQLConfigEntry. spark.sql.hive.convertCTAS has been registered\r\n    at scala.Predef$.require(Predef.scala:224)\r\n    at org.apache.spark.sql.internal.SQLConf$.org$apache$spark$sql$internal$SQLConf$$register(SQLConf.scala:44)\r\n    at org.apache.spark.sql.internal.SQLConf$SQLConfigBuilder$$anonfun$apply$1.apply(SQLConf.scala:51)\r\n    at org.apache.spark.sql.internal.SQLConf$SQLConfigBuilder$$anonfun$apply$1.apply(SQLConf.scala:51)\r\n    at org.apache.spark.internal.config.TypedConfigBuilder$$anonfun$createWithDefault$1.apply(ConfigBuilder.scala:122)\r\n    at org.apache.spark.internal.config.TypedConfigBuilder$$anonfun$createWithDefault$1.apply(ConfigBuilder.scala:122)\r\n    at scala.Option.foreach(Option.scala:257)\r\n    at org.apache.spark.internal.config.TypedConfigBuilder.createWithDefault(ConfigBuilder.scala:122)\r\n    at org.apache.spark.sql.hive.HiveUtils$.<init>(HiveUtils.scala:103)\r\n    at org.apache.spark.sql.hive.HiveUtils$.<clinit>(HiveUtils.scala)\r\n    ... 14 more\r\nAny suggestion is appreciated\r\n\r\nThanks\r\nRobin	
9	2017-05-18 19:45:41	9	0	Efficient use of numpy_indexed output	>>> import numpy_indexed as npi\r\n>>> import numpy as np\r\n>>> a = np.array([[0,0,1,1,2,2], [4,4,8,8,10,10]]).T\r\n>>> a\r\narray([[ 0,  4],\r\n       [ 0,  4],\r\n       [ 1,  8],\r\n       [ 1,  8],\r\n       [ 2, 10],\r\n       [ 2, 10]])\r\n>>> npi.group_by(a[:, 0]).sum(a[:,1])\r\n\r\n(array([0, 1, 2]), array([ 8, 16, 20], dtype=int32))\r\nI want to perform calculations on subsets of the second column clustered by the first column on large sets (~1m lines). Is there an efficient (and/or vectorised) way to use the output of group_by by numpy_indexed in order to add a new column with the output of these calculations? In the example of sum as above I would like to produce the output below.\r\n\r\nIf there is an efficient way of doing this without using numpy_indexed in the first place, that would also be very helpful.\r\n\r\narray([[ 0,  4,  8],\r\n       [ 0,  4,  8],\r\n       [ 1,  8, 16],\r\n       [ 1,  8, 16],\r\n       [ 2, 10, 20],\r\n       [ 2, 10, 20]])	
11	2017-05-18 19:50:09	2	0	python memoization and memory leaks	My goal is to memoize the object instantiation such that there is only one object with the same initialization arguments.\r\n\r\nI adapted some code from this post, and the following code works. Basically, memoize is a decorator that caches the initialization arguments. Next time the same initialization arguments are used, the cached object is returned, instead of creating a new one.\r\n\r\nfrom functools import wraps                                                        \r\n\r\ndef memoize(function):                                                             \r\n    memo = {}                                                                      \r\n\r\n    @wraps(function)                                                               \r\n    def wrapper(*args):                                                            \r\n        if args in memo:                                                           \r\n            return memo[args]                                                      \r\n        else:                                                                      \r\n            rv = function(*args)                                                   \r\n            memo[args] = rv                                                        \r\n            return rv                                                              \r\n    return wrapper                                                                 \r\n\r\n\r\n@memoize                                                                           \r\nclass Test(object):                                                                \r\n    def __init__(self, v):                                                         \r\n        self.v = v                                                                 \r\n\r\nclass TT(object):                                                                  \r\n    def __init__(self, v):                                                         \r\n        self.t = Test(v)                                                           \r\n\r\ntests= [Test(1), Test(2), Test(3), Test(2), Test(4)]                               \r\n\r\nfor test in tests:                                                                 \r\n    print test.v, id(test)                                                         \r\n\r\ntt = TT(2)                                                                         \r\nprint id(tt.t) \r\nAnd I got desired results\r\n\r\n1 4355094288\r\n2 4355094416\r\n3 4355094544\r\n2 4355094416\r\n4 4355094672\r\n4355094416\r\nThe question I have is that do I need to manually clear the cache memoize.memo? It seems that it will contain the references and prevent memory to be released. Is there a way to make this resource release more automated?	
5	2017-05-18 15:11:05	9	0	Convert column[Time] to Timestamp mysql	Seeing the question you might find it as duplicate. But I have researched and its not.\r\n\r\nThe problem is I have a column in my table with "TIME" data-type. Now I want to convert the column to "TIMESTAMP".\r\n\r\nI have tried using Modify too. The query\r\n\r\nALTER TABLE `myofficecab`.`temp_table` MODIFY COLUMN `time` TIMESTAMP\r\nBut this doesn't work. The Error I got\r\n\r\nError Code: 1292. Incorrect datetime value: '20:00:00' for column 'time' at row 1\r\nAlter table change column too doesn't work. Is there any way which I can convert the column TIMESTAMP.\r\n\r\nThe last option that I can see is convert the column to VARCHAR then update appending a date and then convert to timestamp.	
12	2017-05-18 19:51:24	11	0	Combining arrays, loops and if statements	I'm trying to understand how to apply arrays, loops and if statements combined. I have created an array of weekdays and I would like to specify that on a particular day that certain exercise should be assigned. I would like to also print out the days and the exercise assigned. As you will see from the code below, using the weekday.push() method assigns swimming or weight training on alternate days, doesn't add yoga at all and creates 14 values. Could you please suggest how to approach this. Thanks!\r\n\r\nvar weekday = ['Sun', 'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat'];\r\nvar workOut = [];\r\n\r\nfunction myExercise() {\r\n  for (var i = 0; i < weekday.length; i++) {\r\n    if (weekday == 'Wed' || 'Mon' || 'Fri') {\r\n      workOut.push('Swimming');\r\n    }\r\n    if (weekday == 'Tue' || 'Thur' || 'Sat') {\r\n      workOut.push('weight training');\r\n    } else {\r\n      workOut.push('Yoga' + 'or' + 'power walking');\r\n    }\r\n  }\r\n}\r\n\r\nmyExercise();\r\nconsole.log(workOut);	
6	2017-05-18 18:48:43	14	0	postgres: upgrade a user to be a superuser?	In postgres, how do I change an existing user to be a superuser? I don't want to delete the existing user, for various reasons.\r\n\r\n# alter user myuser ...?	
8	2017-05-18 19:06:07	25	0	flask - how do you get a query string from flask	Not obvious from the flask documention on how to get the query string. I am new, looked at the docs, could not find!\r\n\r\nSo\r\n\r\n@app.route('/')\r\n@app.route('/data')\r\ndef data():\r\n    query_string=??????\r\n    return render_template("data.html")	
7	2017-05-18 18:58:25	26	0	Flask Optional URL parameters	Is it possible to directly declare a flask url optional parameter, currently I'm proceeding the following way:\r\n\r\n@user.route('/<userId>')\r\n@user.route('/<userId>/<username>')\r\ndef show(userId,username=None):\r\n    .................\r\nis there anything that can allow me to directly say that "username" is optional?	
\.


SELECT pg_catalog.setval('question_id_seq', 12, true);


ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);




DROP TABLE IF EXISTS answer;

CREATE TABLE answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text
);

DROP SEQUENCE IF EXISTS answer_id_seq;

CREATE SEQUENCE answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE answer_id_seq OWNED BY answer.id;


ALTER TABLE ONLY answer ALTER COLUMN id SET DEFAULT nextval('answer_id_seq'::regclass);


COPY answer (id, submission_time, vote_number, question_id, message, image) FROM stdin;
19	2017-05-18 19:09:10	1	8	The full URL is available as request.url, and the query string is available as request.query_string.\r\n\r\nHere's an example:\r\n\r\nfrom flask import request\r\n\r\n@app.route('/adhoc_test/')\r\ndef adhoc_test():\r\n\r\n    return request.query_string\r\nTo access an individual known param passed in the query string, you can use request.args.get('param'). This is the "right" way to do it, as far as I know.\r\n\r\nETA: Before you go further, you should ask yourself why you want the query string. I've never had to pull in the raw string - Flask has mechanisms for accessing it in an abstracted way. You should use those unless you have a compelling reason not to.	
22	2017-05-18 19:46:24	0	9	One approach with np.unique to generate those unique tags and the interval shifting indices and then np.add.reduceat for the intervaled-summing -\r\n\r\n_,idx,tags = np.unique(a[:,0], return_index=1, return_inverse=1)\r\nout = np.c_[a, np.add.reduceat(a[:,1],idx)[tags]]\r\nAnother way that avoids the use of np.unique and might be beneficial on performance would be like so -\r\n\r\nidx = np.r_[0,np.flatnonzero(a[1:,0] > a[:-1,0])+1]\r\ntag_arr = np.zeros(a.shape[0], dtype=int)\r\ntag_arr[idx[1:]] = 1\r\ntags = tag_arr.cumsum()\r\nout = np.c_[a, np.add.reduceat(a[:,1],idx)[tags]]\r\nFor further performance boost, we should use np.bincount. Thus, np.add.reduceat(a[:,1],idx) could be replaced by np.bincount(tags, a[:,1]).\r\n\r\nSample run -\r\n\r\nIn [271]: a    # Using a more generic sample\r\nOut[271]: \r\narray([[11,  4],\r\n       [11,  4],\r\n       [14,  8],\r\n       [14,  8],\r\n       [16, 10],\r\n       [16, 10]])\r\n\r\nIn [272]: _,idx,tags = np.unique(a[:,0], return_index=1, return_inverse=1)\r\n\r\nIn [273]: np.c_[a, np.add.reduceat(a[:,1],idx)[tags]]\r\nOut[273]: \r\narray([[11,  4,  8],\r\n       [11,  4,  8],\r\n       [14,  8, 16],\r\n       [14,  8, 16],\r\n       [16, 10, 20],\r\n       [16, 10, 20]])]\r\nNow, the listed approaches assume that the first column is already sorted. If that's not the case, we need to sort the array by the first column argsort and then use the proposed method. Thus, for the not sorted case, we need the following as pre-processing -\r\n\r\na = a[a[:,0].argsort()]\r\nBattle against np.unique\r\n\r\nLet's time the custom flatnonzero + cumsum based method against the built-in np.unique to create the shifting indices : idx and the uniqueness based IDs/tags : tags. For a case like this one, where we know beforehand that the labels column is already sorted, we are avoiding any sorting, as done with np.unique. This gives us an advantage on performance. So, let's verify it.\r\n\r\nApproaches -\r\n\r\ndef nonzero_cumsum_based(A):\r\n    idx = np.concatenate(( [0] ,np.flatnonzero(A[1:] > A[:-1])+1 ))\r\n    tags = np.zeros(len(A), dtype=int)\r\n    tags[idx[1:]] = 1\r\n    np.cumsum(tags, out = tags)\r\n    return idx, tags\r\n\r\ndef unique_based(A):\r\n    _,idx,tags = np.unique(A, return_index=1, return_inverse=1)\r\n    return idx, tags\r\nSample run with the custom func -\r\n\r\nIn [438]: a\r\nOut[438]: \r\narray([[11,  4],\r\n       [11,  4],\r\n       [14,  8],\r\n       [14,  8],\r\n       [16, 10],\r\n       [16, 10]])\r\n\r\nIn [439]: idx, tags = nonzero_cumsum_based(a[:,0])\r\n\r\nIn [440]: idx\r\nOut[440]: array([0, 2, 4])\r\n\r\nIn [441]: tags\r\nOut[441]: array([0, 0, 1, 1, 2, 2])\r\nTimings -\r\n\r\nIn [444]: a = np.c_[np.sort(randi(10,10000,(100000))), randi(0,10000,(100000))]\r\n\r\nIn [445]: %timeit unique_based(a[:,0])\r\n100 loops, best of 3: 4.3 ms per loop\r\n\r\nIn [446]: %timeit nonzero_cumsum_based(a[:,0])\r\n1000 loops, best of 3: 486 µs per loop\r\n\r\nIn [447]: a = np.c_[np.sort(randi(10,10000,(1000000))), randi(0,10000,(1000000))]\r\n\r\nIn [448]: %timeit unique_based(a[:,0])\r\n10 loops, best of 3: 50.2 ms per loop\r\n\r\nIn [449]: %timeit nonzero_cumsum_based(a[:,0])\r\n100 loops, best of 3: 3.98 ms per loop	
5	2017-05-18 18:52:35	0	6	ALTER USER myuser WITH SUPERUSER;\r\nDocs.	
6	2017-05-18 18:55:54	0	6	To expand on the above and make a quick reference:\r\n\r\nTo make a user a SuperUser: ALTER USER username WITH SUPERUSER;\r\nTo make a user no longer a SuperUser: ALTER USER username WITH NOSUPERUSER;\r\nTo just allow the user to create a database: ALTER USER username CREATEDB;\r\nYou can also use CREATEROLE and CREATEUSER to allow a user privileges without making them a superuser.	
7	2017-05-18 18:56:16	0	6	$ su - postgres\r\n$ psql \r\n$ \\du; for see the user on db \r\nselect the user that do you want be superuser and:\r\n$  ALTER USER user with superuser;	
8	2017-05-18 18:56:53	0	6	Run this Command\r\n\r\nalter user myuser with superuser;\r\nIf you want to see the permission to a user run following command\r\n\r\n\\du	
9	2017-05-18 18:58:44	0	7	Another way is to write\r\n\r\n@user.route('/<user_id>', defaults={'username': None})\r\n@user.route('/<user_id>/<username>')\r\ndef show(user_id, username):\r\n    pass\r\nBut I guess that you want to write a single route and mark username as optional? If that's the case, I don't think it's possible.	
10	2017-05-18 18:59:43	0	7	Almost the same as Audrius cooked up some months ago, but you might find it a bit more readable with the defaults in the function head - the way you are used to with python:\r\n\r\n@app.route('/<user_id>')\r\n@app.route('/<user_id>/<username>')\r\ndef show(user_id, username='Anonymous'):\r\n    return user_id + ':' + username	
11	2017-05-18 19:00:12	0	7	If you are using Flask-Restful like me, it is also possible this way:\r\n\r\napi.add_resource(UserAPI, '/<userId>', '/<userId>/<username>', endpoint = 'user')\r\na then in your Resource class:\r\n\r\nclass UserAPI(Resource):\r\n\r\n  def get(self, userId, username=None):\r\n    pass	
12	2017-05-18 19:00:35	0	7	@user.route('/<userId>/')  # NEED '/' AFTER LINK\r\n@user.route('/<userId>/<username>')\r\ndef show(userId, username=None):\r\n    pass\r\nhttp://flask.pocoo.org/docs/0.10/quickstart/#routing	
13	2017-05-18 19:02:20	0	7	@user.route('/<user_id>', defaults={'username': default_value})\r\n@user.route('/<user_id>/<username>')\r\ndef show(user_id, username):\r\n   #\r\n   pass	
14	2017-05-18 19:02:29	0	7	@app.route('/', defaults={'path': ''})\r\n@app.route('/< path:path >')\r\ndef catch_all(path):\r\n    return 'You want path: %s' % path\r\nhttp://flask.pocoo.org/snippets/57/	
15	2017-05-18 19:03:00	0	7	You can write as you show in example, but than you get build-error.\r\n\r\nFor fix this:\r\n\r\nprint app.url_map () in you root .py\r\nyou see something like:\r\n<Rule '/<userId>/<username>' (HEAD, POST, OPTIONS, GET) -> user.show_0>\r\n\r\nand\r\n\r\n<Rule '/<userId>' (HEAD, POST, OPTIONS, GET) -> .show_1>\r\n\r\nthan in template you can {{ url_for('.show_0', args) }} and {{ url_for('.show_1', args) }}	
18	2017-05-18 19:07:05	3	8	from flask import request\r\n\r\n@app.route('/data')\r\ndef data():\r\n    # here we want to get the value of user (i.e. ?user=some-value)\r\n    user = request.args.get('user')	
20	2017-05-18 19:10:13	0	8	Werkzeug/Flask as already parsed everything for you. No need to do the same work again with urlparse:\r\n\r\nfrom flask import request\r\n\r\n@app.route('/')\r\n@app.route('/data')\r\ndef data():\r\n    query_string = request.query_string  ## There is it\r\n    return render_template("data.html")\r\nThe full documentation for the request and response objects is in Werkzeug: http://werkzeug.pocoo.org/docs/wrappers/	
21	2017-05-18 19:10:25	0	8	We can do this by using request.query_string.\r\n\r\nExample:\r\n\r\nLets consider view.py\r\n\r\nfrom my_script import get_url_params\r\n\r\n@app.route('/web_url/', methods=('get', 'post'))\r\ndef get_url_params_index():\r\n    return Response(get_url_params())\r\nYou also make it more modular by using Flask Blueprints - http://flask.pocoo.org/docs/0.10/blueprints/\r\n\r\nLets consider first name is being passed as a part of query string /web_url/?first_name=john\r\n\r\n## here is my_script.py\r\n\r\n## import required flask packages\r\nfrom flask import request\r\ndef get_url_params():\r\n    ## you might further need to format the URL params through escape.    \r\n    firstName = request.args.get('first_name') \r\n    return firstName\r\nAs you see this is just a small example - you can fetch multiple values + formate those and use it or pass it onto the template file.	
17	2017-05-18 19:04:10	-6	7	Since Flask 0.10 you can`t add multiple routes to one endpoint. But you can add fake endpoint\r\n\r\n@user.route('/<userId>')\r\ndef show(userId):\r\n   return show_with_username(userId)\r\n\r\n@user.route('/<userId>/<username>')\r\ndef show_with_username(userId,username=None):\r\n   pass	
16	2017-05-18 19:03:33	-2	7	I think you can use Blueprint and that's will make ur code look better and neatly.\r\n\r\nexample:\r\n\r\nfrom flask import Blueprint\r\n\r\nbp = Blueprint(__name__, "example")\r\n\r\n@bp.route("/example", methods=["POST"])\r\ndef example(self):\r\n   print("example")	
23	2017-05-18 19:47:18	0	9	Every index object has an inverse property, which maps reduced values back to their original range; for illustration, we could write:\r\n\r\nindex = npi.as_index(keys)\r\nunique_keys = index.unique\r\nunique_keys[index.inverse] == keys  # <- should be all true\r\nAnd this property is exposed on the GroupBy object as well; since indeed mapping grouped values back to their input range is a commonly useful operation:\r\n\r\ngroups = npi.group_by(a[:, 0])\r\nunique, sums = groups.sum(a[:, 1])\r\nnew_column = sums[groups.inverse]\r\nIn general, the source of numpy_indexed can be an inspiration for how to perform such common operations; group_by.var faces the same problem for instance, of broadcasting the means per group back to each element of the group of which it was formed, to compute the errors in each group. But better tutorials certainly wouldn't hurt either.\r\n\r\nCould you give an even higher level description of the problem you are trying to solve? Chances are you can simplify your code even more from a higher level, when you get more comfortable thinking in terms of the design patterns that npi makes convenient.	
24	2017-05-18 19:48:39	0	10	This is what I am using:\r\n\r\nimport org.apache.spark.sql.SparkSession\r\nobject LoadCortexDataLake extends App {\r\n val spark = SparkSession.builder().appName("Cortex-Batch").enableHiveSupport().getOrCreate()\r\nspark.read.parquet(file).createOrReplaceTempView("temp")\r\n       spark.sql(s"insert overwrite table $table_nm partition(year='$yr',month='$mth',day='$dt') select * from temp")\r\nI think you should use 'sparkSession.sql' instead of 'sparkSession2.sql'	
25	2017-05-18 19:50:18	0	11	You can use either a lru/mru dict (https://github.com/amitdev/lru-dict) or use a time limited cache object. There are great examples here https://pythonhosted.org/cachetools/ and here Limiting the size of a python dictionary.	
26	2017-05-18 19:52:33	0	12	Unfortunately you can't use the short cut like you tried in your if clause. Also you forgot the iterator [i]. Besides the normal\r\n\r\nif (weekday[i] == 'Wed' || weekday[i] == 'Mon' ||  weekday[i] == 'Fri')\r\nyou could also use the following form:\r\n\r\nif ( ['Wed','Mon','Fri'].includes(weekday[i]))\r\nIf you want to support IE (no support for includes) you instead could work with indexOf.\r\n\r\nThis is handy whenever you want to check a lot of values. Altogether, you could write it like this:\r\n\r\nNote, I also changed your second if to an else if (which was the reason for the 14 entries) and used the Array.prototype.map function. Also, it is a bad habit to manipulate an object that does not belong to your scope (workout is in the global scope, but gets manipulated by the myExercise function). It is better to return the desired result and then do a simple assignment.\r\n\r\nvar weekday = ['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat'];\r\nvar workOut = [];\r\n\r\nfunction myExercise() {\r\n\r\n  return weekday.map(function(day){\r\n      var workout;\r\n      if (['Mon','Wed','Fri'].includes(day)){\r\n        workout = "Swimming";\r\n      } else if (['Tue','Thur','Sat'].includes(day)){\r\n        workout = "Weight training";\r\n      } else {\r\n        workout = 'Yoga or power walking';\r\n      }\r\n      return workout;\r\n  });\r\n}\r\n\r\nworkOut = myExercise();\r\nconsole.log(workOut);	
27	2017-05-18 19:53:11	0	12	var weekdays = ['Sun', 'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat'];\r\nvar workouts = weekdays.map(day => {\r\n  switch (day) {\r\n    case 'Wed':\r\n    case 'Mon':\r\n    case 'Fri':\r\n      return 'Swimming';\r\n      break;\r\n    case 'Tues':\r\n    case 'Thur':\r\n    case 'Sat':\r\n      return 'weight training';\r\n      break;\r\n    default:\r\n      return 'Yoga or power walking';\r\n      break;\r\n  }\r\n});\r\n\r\nconsole.log(workouts);	
28	2017-05-18 19:53:40	0	12	Modiefied your code, there was spelling mistakes and conditions were overlapped\r\n\r\nvar weekday = ['Sun', 'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat'];\r\nvar workOut = [];\r\n\r\nfunction myExercise() {\r\n  for (var i = 0; i < weekday.length; i++) {\r\n  console.log(weekday[i] )\r\n    if (weekday[i] == 'Wed' || weekday[i] == 'Mon' || weekday[i] == 'Fri') {\r\n      workOut.push('Swimming');\r\n    }\r\n    else{\r\n    if (weekday[i] == 'Tues' || weekday[i] == 'Thur' || weekday[i] == 'Sat') {\r\n      workOut.push('weight training');\r\n    } else {\r\n      workOut.push('Yoga' + 'or' + 'power walking');\r\n    }\r\n    }\r\n  }\r\n}\r\n\r\nmyExercise();\r\nconsole.log(workOut);	
29	2017-05-18 19:53:51	0	12	There is already switch statement in previous answer, but I am including this one as well. It might be not DRY, but for a beginner easier to understand:\r\n\r\nvar weekday = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];\r\nvar workOut = [];\r\n\r\nfunction myExercise() {    \r\n    for (var i = 0; i < weekday.length; i++) {\r\n        switch(weekday[i]) {\r\n            case 'Sun':\r\n                workOut.push('Yoga' + 'or' + 'power walking');\r\n                break;\r\n            case 'Mon':\r\n                workOut.push('Swimming');\r\n                break;\r\n            case 'Tue':\r\n                workOut.push('weight training');\r\n                break;\r\n            case 'Wed':\r\n                workOut.push('Swimming');\r\n                break;\r\n            case 'Thu':\r\n                workOut.push('weight training');\r\n                break;\r\n            case 'Fri':\r\n                workOut.push('Swimming');\r\n                break;\r\n            case 'Sat':\r\n                workOut.push('weight training');\r\n                break;\r\n                default:\r\n                workOut.push('Sleep!!');\r\n        }\r\n    }\r\n}\r\n\r\nmyExercise();\r\nconsole.log(workOut);	
\.


SELECT pg_catalog.setval('answer_id_seq', 29, true);


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);





DROP TABLE IF EXISTS comment;

CREATE TABLE comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edit_count integer
);

DROP SEQUENCE IF EXISTS comment_id_seq;

CREATE SEQUENCE comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE comment_id_seq OWNED BY comment.id;

ALTER TABLE ONLY comment ALTER COLUMN id SET DEFAULT nextval('comment_id_seq'::regclass);


COPY comment (id, question_id, answer_id, message, submission_time, edit_count) FROM stdin;
3	6	\N	I had RTFM, but the manual only describes the command and its options. Newbies then struggle to understand how to put the command together. Most good manuals give you example commands as well. That, however, would be far too helpful for postgres.	2017-05-18 18:50:28	0
4	6	\N	This is what always drives me mad about SO! How is this possibly off topic! It's a great question that solved my issue - as a programmer; while programming.	2017-05-18 18:51:40	0
5	6	\N	This is a very helpful question as a programmer. I'm writing a database adapter and this is definitely not an "off topic" question. 165 people are "in the community" and found this helpful	2017-05-18 18:52:14	0
6	\N	5	Thanks! Now people googling this question will find this answer, and StackOverflow will work as it's intended to.	2017-05-18 18:52:53	0
7	\N	5	the opposite operation is ALTER USER myuser WITH NOSUPERUSER	2017-05-18 18:53:09	0
8	\N	5	and how can i detect if myuser is currently superuser?	2017-05-18 18:53:26	0
9	\N	5	SELECT rolname, rolsuper FROM pg_roles;	2017-05-18 18:53:41	0
10	\N	5	You can do \\du to list all users/roles.	2017-05-18 18:53:56	0
11	\N	7	in this specific case, you have to put the username inside comas, example ALTER USER "user" WITH SUPERUSER;	2017-05-18 18:56:31	0
12	\N	9	Any problems using this method when referencing endpoints and url_for ?	2017-05-18 18:58:59	0
13	\N	9	Not that I know of. Even Flask docs contain similar example (you need to scroll down a bit to see it).	2017-05-18 18:59:21	0
14	\N	10	Also, the this works if username is not constant. defaults= freezes the default value in a dictionary.	2017-05-18 18:59:55	0
15	\N	12	Please, add some explanation to your code.	2017-05-18 19:00:59	0
16	\N	12	flask.pocoo.org/docs/0.10/quickstart/#routing	2017-05-18 19:01:16	0
17	\N	14	You should add here the info from the external link because if that link will no longer be valid, your answer will be damaged.	2017-05-18 19:02:44	0
18	\N	16	This does not answer the question.	2017-05-18 19:03:55	0
19	\N	17	What? Using flask 0.10.1 here and I can add multiple routes to one endpoint just fine.	2017-05-18 19:04:29	0
20	8	\N	It's in the documentation under quickstart: flask.pocoo.org/docs/quickstart/#the-request-object	2017-05-18 19:06:18	0
21	\N	18	This example returns that value of the "user" parameter passed in the query string, not the query string itself. "Query string" means everything after the question mark and before the pound sign, if one is present.	2017-05-18 19:07:32	0
22	\N	18	still is a useful answer consider that it is related to the question. So valid and +1	2017-05-18 19:07:45	0
23	\N	18	Will this raise an exception if user is not present? (I guess not if args is just a dict.)	2017-05-18 19:07:58	0
24	\N	18	No - as with a dict and .get, you'd just get None.	2017-05-18 19:08:13	0
25	\N	18	Well spotted. But since this answer correctly answers the question my Google search terms alluded to ('flask get request parameter') I'm up-voting it anyhow. I'm a pedant too, but I'm chalking this up to web mysticism. 😉	2017-05-18 19:08:31	0
26	\N	19	+1 for the actual right answer. OAuth flows such as Dropbox will regularly ask for redirection URLs to pass tokens to. It makes perfect sense that you'd want to parse the query string yourself.	2017-05-18 19:09:28	0
27	9	\N	Would the first col be already sorted? Also, would it always start with 0 and have only sequential numbers?	2017-05-18 19:45:58	0
28	9	\N	The column with the categories is always sorted but the group numbers don't necessarily start from 0 but are incrementally numbers. Thank you	2017-05-18 19:46:08	0
29	\N	22	Thank you, may I ask how the first value that is unpacked, _, is used?	2017-05-18 19:46:47	0
30	\N	22	We have three outputs from that step. With that _, we are just not storing it, i.e. we don't need that first output.	2017-05-18 19:47:01	0
31	\N	23	Thank you for your answer. If I define a as in my initial post and then run the two lines you are presenting above, the first one returns an npi object, but the second returns TypeError: only integer scalar arrays can be converted to a scalar index. I'm sure the answer is obvious to you but not to me so any help please? Cheers	2017-05-18 19:47:32	0
32	\N	23	sorry, small mistake on my part indeed; still havn't actually ran my code but I am fairly sure it should be correct now!	2017-05-18 19:47:45	0
33	12	\N	Not answering your question but fyi instead of an if you could use a switch	2017-05-18 19:51:37	0
34	12	\N	definitely use a switch here	2017-05-18 19:51:46	0
35	12	\N	not sure a switch would help in this case. You'd either need to hard code the workOut.push() for each day or order the cases weirdly (Mon,Wed,Fri,Tue,Thur,Sat) to overlap the cases.	2017-05-18 19:52:01	0
36	\N	26	what's the point in using the extra function? Why not do workout = weekday.map(fn)	2017-05-18 19:52:47	0
37	\N	26	This is just resembling the code of the OP. It might come in handy later, if you want to reuse the functionality.	2017-05-18 19:52:56	0
38	\N	27	Thanks! One question, what is the purpose of "(day)" here?	2017-05-18 19:53:25	0
\.



SELECT pg_catalog.setval('comment_id_seq', 38, true);


ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);


ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

