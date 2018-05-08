query = {
    'select_daily': '''
    select run_time as Statistictime ,
       ifnull((select SUM(account) 
       FROM dailylog a 
       WHERE a.run_time = dailylog.run_time),0) as Totalnumberoftasks,
       ifnull((select SUM(account) 
       FROM dailylog b 
       where status=0 AND b.run_time = dailylog.run_time ),0) as Totalnumberoferrortasks 
    FROM dailylog 
    GROUP BY run_time
    '''
}