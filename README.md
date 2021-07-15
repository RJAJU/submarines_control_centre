# submarines_control_centre
Submarines Control Centre

Steps to setup:
1. Create one virtual environment
   virtualenv -p python3.7 venv

2. Install Pubnub
   pip install 'pubnub>=4.6.0'

3. Install Flask
   pip install flask

4. Go to your project directory
   cd Desktop

5. Clone Submarines Control Repository
   git clone https://github.com/RJAJU/submarines_control_centre.git

6. Move inside the project directory
   cd submarines_control_centre

7. Checkout to master branch
   git checkout master

8. Activate the virtual environment here
   source venv/bin/activate

9. Start submarines control centre service
   A. export FLASK_APP=jack_sparrow
   B. flask run --port=5000

10. Open another terminal and activate virtual environment here as well
    source venv/bin/activate

11. Start submarines service here
    export FLASK_APP=submarine
    flask run --port=5001
