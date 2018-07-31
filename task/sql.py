


query = {
    'add_task': '''
    INSERT INTO task (taskid, category, owner, email,
                      description, tag, enabled, freqency,
                      task_type, threshold, filepath, upload_time,
                      update_time, content, upload_user_id, taskname)
              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''',
    'update_task': '''
    UPDATE task
    SET category=?, owner=?, email=?, description=?, tag=?, freqency=?,
    task_type=?, threshold=?, content=?, update_time=?, upload_user_id=?, taskname=?
    WHERE taskid=?
    ''',
    'remove_task': '''
    UPDATE task
    SET remove=1
    WHERE taskid=?
    '''
}




