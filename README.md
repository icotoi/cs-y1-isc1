GOSSIP and STIGMERGY simple implementation
==========================================

The implementations in this repository are rudimentary and serve as a basis for academic comparison in the context of 
Complex Systems Masters Programme at the Polytechnic University of Bucharest, year 2020.

Folder Structure
----------------

* gossip.py - gossip agent & model implementation
* gossip_viz.py - gossip visualization & web server instance
* stigmergy.py - stigmergy agent & model implementation
* stigmergy_viz.py - stigmergy visualization & web server instance
* requirements.txt - python pip requirements file (containing mesa and other dependencies)


How To Run
----------

1. Clone this repository
2. Go to the cloned repository location
3. Create virtual environment


    python3 -m venv venv 

5. Source the virtual environment

    
    . venv/bin/activate

6. Install dependencies from requirements.txt file

    
    pip install -r requirements.txt
7. Run either gossip_viz.py or stigmergy_viz.py; this will open a web browser pointing to the 
visualization web interface on http://localhost:8521


    ./stigmergy_viz.py 
    .....
    Interface starting at http://127.0.0.1:8521


License
-------

This code is provided under the Apache 2 license
