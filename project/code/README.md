# Topic
##Description
## Instructions
1. To run Flask app on AWS - ```gunicorn -w 10 -b 0.0.0.0:5001 app:app```

**Update** : Replaced gunicorn with uwsgi . 
Run uwsgi using ```uwsgi -s /tmp/uwsgi.sock -p 100 --http 152.46.19.201:5001  --manage-script-name --mount /=app:app```

2. To run using scoop 
Add this code to your application - 
```
    from scoop import futures
    toolbox.register("map", futures.map) 
```
 
 and run using ``` python -m scoop -n 10 nsga2.py ```
 
 3. To run using multiprocessing
 Add this code to your application - 
 ``` 
    import multiprocessing

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)
 ```
    
and run using ```python nsga2.py ```


    
