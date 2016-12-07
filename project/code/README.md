# Alternating Offers Protocol (Rubenstein)

[Project Report](http://github.com/wddlz/fss16iad/tree/master/project/code/Report.md)

## Files Description
*Requires* - redis,deap,matplotlib,numpy,Flask.

```nginx.conf``` - Nginx configuration with IPs of the servers running flask application using sockets on wsgi mentioned as ```server 152.46.19.201:5002```.
```app.ini ``` -uwsgi ini file to mention socket address and number of processes for the flask application .
```app.py``` - Flask application to handle ```/prism``` route over HTTP.
```parse.py``` - Run the prism cli and parse the results to get objectives from the decisions. Prism cli location is configured here.
```prism.py``` - To get objectives from the flask application over HTTP.Nginx server IP is configured in this file.
```run.py ``` - All algorithms are written here. Future algos can be written as ```def main_algo(algorithm="AlgorithmName",seed=None,NGEN=100,MU=100)``` and called in ```__main__``` using ```algo = [main_nsga2 , main_spea2 ,main_ga , main_algo]```
```runforever.sh``` - Runs multiple run by calling run.py.
```hit_ratio.txt``` - Saved when ```plotHitRatio()``` is called to calculate hit counters in single thread environment.
```hit_ratio.py``` - Runs on hit_ratio.txt to plot the hit ratio graph.
```negotiation.pm``` - The modified prism file for negotiation which requires 15 decisions to be given in the format ```["B_RP", "S_RP", "B_IP", "S_IP", "Tb", "TbB", "Ts", "TsB", "bCinc", "bBinc", "sCdec", "sBdec", "Kb", "Ks","Offset"]```

```plotGraph.py```  - Plot graphs based on the paretos generated from run.py
```savestat.py``` - Helper class to save stat to files.
```spread_igd.py``` - Professor provided spread and igd calculator.
```hypervolume.py``` - Professor provided hypervolume calculator -modified for our purpose.
```printStat.sh``` -calls stat.py under stats which uses uuid for each run to pretty print stats.
```variance.py``` - Calculate variance for various prism runs
```/sample``` - Contains sample output from prism CLI
```/screenshots``` - Contains screenshots required for the report.
```/stats``` - Contains sample stats of someruns and ```stat.py``` for performance measure.


## Instructions

### On the server running Flask application for prism

1. Make sure prism is installed and configured in prism.py.
2. Run the uwsgi application using ```uwsgi --ini app.ini```

3. Make sure the nginx server with nginx.conf is running with proper sockets conigured in app.ini.

4. Run algorithms by ```python -m scoop -n 50 run.py```



Alternate ways to test :

1. To run Flask app on AWS quickly without nginx or uwsgi install gunicorn and run  - ```gunicorn -w 10 -b 0.0.0.0:5001 app:app```

or only using uwsgi using ```uwsgi -s /tmp/uwsgi.sock -p 100 --http <IP>:5001  --manage-script-name --mount /=app:app```

2. To run using scoop
Add this code to your application -
```
    from scoop import futures
    toolbox.register("map", futures.map)
```

 and run using ``` python -m scoop -n 10 run.py ```

 3. To run using multiprocessing
 Add this code to your application -
 ```
    import multiprocessing

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)
 ```

and run using ```python run.py ```
