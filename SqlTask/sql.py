





query = {
    'add_dailylog': '''
    INSERT INTO dailylog (taskid, result_count, result_time, status, user_id, insert_time, taskname, category, description)
    VALUES (?,?,?,?,?,?,?,?,?)
    ''',
    'add_weeklylog': '''
    INSERT INTO weeklylog (taskid, result_count, result_time, status, user_id, insert_time, taskname, category, description)
    VALUES (?,?,?,?,?,?,?,?,?)
    ''',
    'add_monthlylog': '''
    INSERT INTO monthlylog (taskid, result_count, result_time, status, user_id, insert_time, taskname, category, description)
    VALUES (?,?,?,?,?,?,?,?,?)
    ''',
    'add_resulttab': '''
    INSERT INTO result_tab (taskname, taskid, result, status, run_time, duration)
    VALUES (?,?,?,?,?,?)
    ''',
    'tasklog':'''
    INSERT INTO tasklog (taskname, taskid, status, description, insert_time)
    VALUES (?,?,?,?,?)
    '''
}
