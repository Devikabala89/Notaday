Project Name: Notaday
Project Overview:
	We use multiple applications in our day to day life be it for taking Notes or creating docket or for Calorie tracking. This project aims in integrating those different apps in single web application along with e-commerce platform which allows users to use the features and buy stuffs they need as well.
Problem Statement:
	To maintain single application where we can store all data like docket list, agenda, notes, tracking of food intake.
	This helps the users to organize the tasks and notes and be mindful of their health.
Key Features and Functionalities:
	Used Django built-in modules for user registration, authentication and session management.
	Docket feature:
		Allows users to add task with date and priority.
		Date and priority are displayed and highlighted for better view.
		Users can mark the task as “completed” once done
		Users can delete the task if they feel it’s not needed.
		The UI part includes three tabs namely All tasks, Active and completed for   segregation of list based on completion status.
	Calorie Tracker Feature:
		Allows users to input the meals they had based on category along with date.
		User can input the calorie GOAL.
		This app calculates the total calories intake based on user inputs and compares with goal.
		UI part includes a progress bar to display the total calories intake.
		Upon selecting a date, user can able to see the data they registered.
	Notes Feature:
		Allows users to add a new note.
		They can select a note to be displayed and edit it.
		Notes can be deleted if it’s no more needed.
	Merchandise Feature:
		Lists the products that are being selling.
		UI has filter options integrated with add to cart facility.
		Payment app used – RazorPay.
		Gmail integrated.
Technology stack:
	This project is developed including below technologies,
		Frontend – Bootstrap
		Backend – Django
		Database – MySQL
