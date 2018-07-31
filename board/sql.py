query = {
    'select_daily': '''
       select result_time as Statistictime ,
       ifnull((select COUNT(taskid)
       FROM dailylog a
       WHERE a.result_time = dailylog.result_time),0) as Totalnumberoftasks,
       ifnull((select COUNT(taskid)
       FROM dailylog b
       where status='Fail' AND b.result_time = dailylog.result_time ),0) as Totalnumberoferrortasks
    FROM dailylog
    WHERE user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ''',
    'select_weekly': '''
    select result_time as Statistictime ,
      ifnull((select COUNT(taskid)
      FROM weeklylog a
      WHERE a.result_time = weeklylog.result_time),0) as Totalnumberoftasks,
      ifnull((select COUNT(taskid)
      FROM weeklylog b
      where status='Fail' AND b.result_time = weeklylog.result_time ),0) as Totalnumberoferrortasks
    FROM weeklylog
    WHERE user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ''',
    'monthly_list': '''
    select result_time as Statistictime ,
      ifnull((select COUNT(taskid)
      FROM monthlylog a
      WHERE a.result_time = monthlylog.result_time),0) as Totalnumberoftasks,
      ifnull((select COUNT(taskid)
      FROM monthlylog b
      where status='Fail' AND b.result_time = monthlylog.result_time ),0) as Totalnumberoferrortasks
    FROM monthlylog
    WHERE user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ''',
    'select_daily_desc': '''
    select result_time as Statistictime ,
       ifnull((select COUNT(taskid)
       FROM dailylog a
       WHERE a.result_time = dailylog.result_time),0) as Totalnumberoftasks,
       ifnull((select COUNT(taskid)
       FROM dailylog b
       where status='Fail' AND b.result_time = dailylog.result_time ),0) as Totalnumberoferrortasks
    FROM dailylog
    WHERE user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ORDER BY result_time DESC
    ''',
    'select_weekly_desc': '''
    select result_time as Statistictime ,
      ifnull((select COUNT(taskid)
      FROM weeklylog a
      WHERE a.result_time = weeklylog.result_time),0) as Totalnumberoftasks,
      ifnull((select COUNT(taskid)
      FROM weeklylog b
      where status='Fail' AND b.result_time = weeklylog.result_time ),0) as Totalnumberoferrortasks
    FROM weeklylog
    WHERE user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ORDER BY result_time DESC
    ''',
    'monthly_list_desc': '''
    select result_time as Statistictime ,
      ifnull((select COUNT(taskid)
      FROM monthlylog a
      WHERE a.result_time = monthlylog.result_time),0) as Totalnumberoftasks,
      ifnull((select COUNT(taskid)
      FROM monthlylog b
      where status='Fail' AND b.result_time = monthlylog.result_time ),0) as Totalnumberoferrortasks
    FROM monthlylog
    WHERE user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ORDER BY result_time DESC
    ''',
    'select_fail_daily': '''
    select category as Module, 
    COUNT(id) as totalCount,
    ifnull((select COUNT(id)
      FROM dailylog a
      WHERE a.result_time = ( SELECT MAX(result_time) FROM dailylog) AND a.status = 'Fail' AND a.category = dailylog.category),0) as failCount
    FROM dailylog
    WHERE user_id = IFNULL(?,user_id) AND result_time = (
		SELECT MAX(result_time)
		FROM dailylog
		WHERE user_id = IFNULL(?,user_id)
	)
    Group BY category
    ''',
    'select_fail_weekly': '''
    select category as Module, 
    COUNT(id) as totalCount,
    ifnull((select COUNT(id)
      FROM weeklylog a
      WHERE a.result_time = ( SELECT MAX(result_time) FROM weeklylog)  AND a.status = 'Fail' AND a.category = weeklylog.category),0) as failCount
    FROM weeklylog
    WHERE user_id = IFNULL(?,user_id) AND result_time = (
		SELECT MAX(result_time)
		FROM weeklylog
		WHERE user_id = IFNULL(?,user_id)
	)
    Group BY category
    ''',
    'monthly_fail_list': '''
    select category as Module, 
    COUNT(id) as totalCount,
    ifnull((select COUNT(id)
      FROM monthlylog a
      WHERE a.result_time = ( SELECT MAX(result_time) FROM monthlylog) AND a.status = 'Fail' AND a.category = monthlylog.category),0) as failCount
    FROM monthlylog
    WHERE user_id = IFNULL(?,user_id) AND result_time = (
		SELECT MAX(result_time)
		FROM monthlylog
		WHERE user_id = IFNULL(?,user_id)
	)
    Group BY category
    ''',
    'category_select_daily': '''
    select result_time as Statistictime ,
       ifnull((select COUNT(taskid)
       FROM dailylog a
       WHERE a.result_time = dailylog.result_time AND category = ?),0) as Totalnumberoftasks,
       ifnull((select COUNT(taskid)
       FROM dailylog b
       where status='Fail' AND b.result_time = dailylog.result_time AND category = ?),0) as Totalnumberoferrortasks
    FROM dailylog
    WHERE category = ? AND user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ''',
    'category_select_weekly': '''
    select result_time as Statistictime ,
      ifnull((select COUNT(taskid)
      FROM weeklylog a
      WHERE a.result_time = weeklylog.result_time AND category = ?),0) as Totalnumberoftasks,
      ifnull((select COUNT(taskid)
      FROM weeklylog b
      where status='Fail' AND b.result_time = weeklylog.result_time AND category = ?),0) as Totalnumberoferrortasks
    FROM weeklylog
    WHERE category = ? AND user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ''',
    'category_monthly_list': '''
    select result_time as Statistictime ,
      ifnull((select COUNT(taskid)
      FROM monthlylog a
      WHERE a.result_time = monthlylog.result_time AND category = ?),0) as Totalnumberoftasks,
      ifnull((select COUNT(taskid)
      FROM monthlylog b
      where status='Fail' AND b.result_time = monthlylog.result_time AND category = ?),0) as Totalnumberoferrortasks
    FROM monthlylog
    WHERE category = ? AND user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ''',
    'category_select_daily_desc': '''
    select result_time as Statistictime ,
       ifnull((select COUNT(taskid)
       FROM dailylog a
       WHERE a.result_time = dailylog.result_time AND category = ?),0) as Totalnumberoftasks,
       ifnull((select COUNT(taskid)
       FROM dailylog b
       where status='Fail' AND b.result_time = dailylog.result_time AND category = ?),0) as Totalnumberoferrortasks
    FROM dailylog
    WHERE category = ? AND user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ORDER BY result_time DESC
    ''',
    'category_select_weekly_desc': '''
    select result_time as Statistictime ,
      ifnull((select COUNT(taskid)
      FROM weeklylog a
      WHERE a.result_time = weeklylog.result_time AND category = ?),0) as Totalnumberoftasks,
      ifnull((select COUNT(taskid)
      FROM weeklylog b
      where status='Fail' AND b.result_time = weeklylog.result_time AND category = ?),0) as Totalnumberoferrortasks
    FROM weeklylog
    WHERE category = ? AND user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ORDER BY result_time DESC
    ''',
    'category_monthly_list_desc': '''
    select result_time as Statistictime ,
      ifnull((select COUNT(taskid)
      FROM monthlylog a
      WHERE a.result_time = monthlylog.result_time AND category = ?),0) as Totalnumberoftasks,
      ifnull((select COUNT(taskid)
      FROM monthlylog b
      where status='Fail' AND b.result_time = monthlylog.result_time AND category = ?),0) as Totalnumberoferrortasks
    FROM monthlylog
    WHERE category = ? AND user_id = IFNULL(?,user_id)
    GROUP BY result_time
    ORDER BY result_time DESC
    ''',
    'category_select_fail_daily': '''
    select taskid,result_time,taskname,status,description
    FROM dailylog
    where result_time = (
		SELECT MAX(result_time)
		FROM dailylog
		WHERE user_id = IFNULL(?,user_id)
	) AND category = ? AND user_id = IFNULL(?,user_id)
    ORDER BY result_time DESC 
    ''',
    'category_select_fail_weekly': '''
    select taskid,result_time,taskname,status,description
    FROM weeklylog
    where result_time = (
		SELECT MAX(result_time)
		FROM weeklylog
		WHERE user_id = IFNULL(?,user_id)
	) AND category = ? AND user_id = IFNULL(?,user_id)
    ORDER BY result_time DESC 
    ''',
    'category_monthly_fail_list': '''
    select taskid,result_time,taskname,status,description
    FROM monthlylog
    where result_time = (
		SELECT MAX(result_time)
		FROM monthlylog
		WHERE user_id = IFNULL(?,user_id)
	) AND category = ? AND user_id = IFNULL(?,user_id)
    ORDER BY result_time DESC 
    ''',
    'select_being_performed': '''
    select *
    FROM being_performed
    WHERE status = '1'
    ''',
    'select_error_tasks': '''
    select *
    FROM tasklog
    WHERE status = '1' 
    '''
}