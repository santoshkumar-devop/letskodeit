command to execute

pip install -r requirements.txt


pytest -> to run all testcases
to run login testcases -> pytest .\tests\home\test_login.py   --html=report.html 
to run register courses testcase -> pytest .\tests\courses\test_register_courses.py   --html=report.html 
to perform parallel execution -> pytest -n 4 --html=report.html
