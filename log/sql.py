


query = {
    'select_tasklist': '''
      SELECT * ,
       (select COUNT(taskid)
         from result_tab a
         WHERE a.taskid = t.taskid) as totalrun,
       (select COUNT(taskid)
         from result_tab a
         WHERE a.taskid = t.taskid And a.status = 'Fail') as totalfails,
       (select result FROM result_tab WHERE taskid = t.taskid ORDER BY run_time DESC limit 1) as count
      From task t
      WHERE remove = 0
      ORDER BY last_runtime DESC
    ''',
    'select_task':'''
      select *
      FROM task
      WHERE
      taskid = ?
    ''',
    'selctTaskLogById': '''
      SELECT *
      FROM result_tab
      WHERE
      taskid = ?
      ORDER BY run_time DESC
    ''',
    'updateComment': '''
      UPDATE result_tab
      SET comments = ?
      WHERE
      id = ?
    ''',
    'SelectDailyErrorList':'''
      SELECT a.* 
      FROM
        (SELECT *
            from dailylog
            WHERE result_time = ? AND status = 'Fail') b
        LEFT JOIN task a 
        ON a.taskid = b.taskid
    ''',
    'SelectWeeklyErrorList':'''
      SELECT a.* 
      FROM
        (SELECT *
            from weeklylog
            WHERE result_time = ? AND status = 'Fail') b
        LEFT JOIN task a 
        ON a.taskid = b.taskid
    ''',
    'SelectMonthlyErrorList':'''
      SELECT a.* 
      FROM
        (SELECT *
            from monthlylog
            WHERE result_time = ? AND status = 'Fail' AND user_id = IFNULL(?,user_id)) b
        LEFT JOIN task a 
        ON a.taskid = b.taskid
    ''',
    'SelectSpeDailyErrorList':'''
      SELECT a.* 
      FROM
        (SELECT *
            from dailylog
            WHERE result_time = ? AND status = 'Fail' AND category = ?) b
        LEFT JOIN task a 
        ON a.taskid = b.taskid
    ''',
    'SelectSpeWeeklyErrorList':'''
      SELECT a.* 
      FROM
        (SELECT *
          from weeklylog
          WHERE result_time = ? AND status = 'Fail' AND category = ?) b
      LEFT JOIN task a 
      ON a.taskid = b.taskid
    ''',
    'SelectSpeMonthlyErrorList':'''
      SELECT a.* 
      FROM
        (SELECT *
          from monthlylog
          WHERE result_time = ? AND status = 'Fail' AND category = ?) b
      LEFT JOIN task a 
      ON a.taskid = b.taskid
    ''',
    'filtrateSelect':'''
      SELECT * ,
        (select COUNT(taskid) FROM result_tab a WHERE a.taskid = task.taskid) as totalrun,
        (select COUNT(taskid) FROM result_tab a WHERE a.taskid = task.taskid And a.status = 0) as totalfails,
        (select result FROM result_tab WHERE taskid = task.taskid ORDER BY run_time DESC limit 1) as count
      From task 
      WHERE freqency = IFNULL(?,freqency) AND enabled = IFNULL(?,enabled) AND category = IFNULL(?,category)
    ''',
    'SelectTaskOfMike': '''
      SELECT
      (SELECT a.result FROM result_tab  a WHERE a.taskid = t.taskid  order by a.run_time desc limit 0,0) as last_count, 
      MAX(r.run_time) as last_runtimes,
      (SELECT a.result FROM result_tab  a WHERE a.taskid = t.taskid  order by a.run_time desc limit 0,0) - (SELECT a.result FROM result_tab  a WHERE a.taskid = t.taskid  order by a.run_time desc limit 1,1) as chang,
      t.*
      FROM   (SELECT * FROM result_tab WHERE taskid in (SELECT taskid from task WHERE category = ?)) r
      left join task t ON t.taskid = r.taskid
      group by r.taskid
    ''',
    'selctMikeTaskLogById':'''
      SELECT *
      FROM result_tab
      WHERE
      taskid = ?
      ORDER BY run_time DESC
    ''',
    'getUsernameByUserid':'''
        SELECT name from sys_user_tab WHERE user_id = ?
    ''',
    'getTaskinfoByUsername':'''
        SELECT taskid ,taskname ,description
        FROM task 
        WHERE
        owner = ? AND category = ?
    ''',
    'getTasklogByUsername':'''
        SELECT taskname ,run_time, result
        FROM result_tab
        WHERE
        taskid in (SELECT taskid FROM task WHERE owner = ? AND category = ?) AND ?< run_time AND run_time <?
        ORDER BY run_time DESC
    ''',
    'getCategoryByUsername': '''
        SELECT category
        FROM task
        WHERE owner = ?
        GROUP BY category
    '''
}




