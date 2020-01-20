FlaskCarLeasing v0.1b Documentation 

- - - How to start? - - -
1. Activate the virtual enviroment, that's in the appenv folder.
2. pip install all the required modules from requirements.txt .
3. Create a system variable named "MODERATOR_TOKEN" (without quotes).
4. Open python shell and import db from flaskcarleasing.config.
4. Create all tables by using command db.create_all() in previously opened python shell.
5. ???
6. YOU ARE NOW READY TO START. JUST RUN THE "app.py" file in the application folder.


- - - Instructions - - -

As you open the app in your browser at 'localhost:5000' by default, you are on the index page.
There are parts such as concerns, cars and login/register buttons.
By entering the "cars" module you can acces the list of all cars, paginated and sorted from newest to latest.
By entering the "concerns" module you can then click on the concern that you're insterested in and it will show you list of all cars associated with that concern.
Login and register fields are pretty obvious, so you can probably hande it by yourself. 
To lease a car just click on the Lease button and confirm the deal. Later on you can add any payment system to check if the payment was made and validate it or you can just call back the client and send him a courier on the leased car. I don't know, there are lots of options.
To end contracts just go to your profile page and click on the contracts button then choose any of it in the table and click on the button "end contract".
And one more: don't forget to end your contract in time, else you'll be panished with penalty system and got to put extra money of out of time returning of the leased car.


- - - Any validations? - - -

Yes. As I said in the description there is a moderation system. You can simply register an account and then give it the moderator rights.
To do that just login to your account and click on your username at the top. Fill in the MODERATOR_TOKEN variable's value to the right form, then click submit. Congragulations, you now have moderator rights and can create/update/delete objects.



So, that must be it. Just as simple as that, cause it's literally my first project.
Created, designed and developed by GreedWizard : https://github.com/greedWizard .
