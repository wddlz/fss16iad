# Topic
##Description
## Instructions
1. To run Flask app on AWS - ```gunicorn -w 10 -b 0.0.0.0:5001 app:app```

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
    
