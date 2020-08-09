# MyLMS
MyLMS is a Learning Management System (LMS) - a simple online platform for learning and education. It aims to condense and smoothen the workflow between teachers and students, providing a shared digital medium as a learning space.
## Overview

The project consists of three unique users (**teacher, student, admin**). It contains 9 base pages - **Login**, **Register**, **Updates**, **Lessons**, **Resources**, **Assignments**, **Submissions**, **Forum**, **Notifications**. These will be explained in further detail below.

## Features
### Students:

 - **Updates page**
	 - Students who are logged in should be able to see all the latest updates from all teachers
	 - An update should show the:
		 - Teacher name
		 - Timestamp of update
		 - Content of update

 - **Resources page**
	 - Students who are logged in should have access to a resources page, where they can see the latest files uploaded by their teachers
	 - Resources should only be shown to students who are registered with that subject.
		 - Every file should show the:
			 - Filename
			 - Timestamp of upload
			 - User that uploaded it

 - **Assignments page:**
	  - Students who are logged in should be able to view all their assignments, in backwards chronological order.
	  - Assignments should only be shown if the student is taking that subject.
	  - Each assignment should show the status (open/closed), and the deadline.
	  - Clicking on an assignment should take them to that 		assignment&#39;s page.
	  - The assignment page should show the:
		  - Deadline
		  - Teacher that created the assignment
		  - Title
		  - Further instructions
	  - The student should be allowed to submit their homework if the deadline has not yet passed.
	  - Once submitted, the submission should be recorded as submitted.
	  - If the deadline has passed, students will not be allowed to submit their homework anymore.
	  - If the deadline has passed and student has not submitted, the submission should be marked as unsubmitted.
	  
 - **Forum page:**
	  - The forum should allow both students and teachers to post questions or any subject-related matters.
	  - Original poster should be allowed to edit his/her posts **asynchronously**.
	  - The main forum page lists the subjects, and when clicked, are taken to the respective subject forums.
	  - Each subject forum should show a list of all forum posts.
	  - Both students and teachers are able to reply to forum posts.
	  - The forum page should only show the subjects pertaining to each student/teacher.
	  - Users should be allowed to search for a forum post based on the title with the search bar.
	  
- **Video Lessons page:**
  - Students are able to view the YouTube video lessons from the subjects they are taking.
  - Clicking on a subject will show the list of all the lessons for that particular subject.
  - Clicking on a lesson will take the student to the lesson page, which shows an embedded YouTube video which is watchable on-site.

### Teachers
- **Updates page** :
  - Only teachers should be allowed to post new updates.
  
- **Resources page:**
  - Only teachers should be allowed to upload resources.
  - Once uploaded, the page should refresh showing the list of all uploaded resources.
  - Teachers can delete their resources **asynchronously**.
  - Before deleting resource, a confirmation is always required.
  
- **Assignments page:**
  - In every assignment page, teacher should be able to see the list of submissions from their students.
  - They should also see students that have not submitted that particular assignment
    - If the student registered after the submission deadline had closed, then the student will not appear in the student list.
    
- **Forum page:**
  - Teachers are allowed to comment on any questions posted by the students.
  - They should also be allowed to post their own posts.
  
- **Lessons page:**
  - Students are allowed to create lessons for the subjects they are teaching.

### Admin
- **User approval** :
  - Admin will be in charge of approving newly-registered user based on their delegated roles.
- **Creating subjects:**
  - Admin will be responsible for creating subjects based on a given list.
- **Deleting posts/updates** :
  - Only admin has the authority to delete forum posts and updates.
- **Editing data when necessary (e.g. Lessons, Assignments, etc.)**
- **The admin also has the privileges of a teacher.**

### **Notifications**

- Clicking on the username in the navigation bar should take the user to a page that displays the notifications for the particular user.
- Notifications will be sorted in reverse chronological order, and should include the time when the user was notified.
- **Standard notifications** are sent out when:
  - Teachers make an update post.
  - Teachers add a new lesson.
  - Teachers create a new assignment.
  - A user posts on the forum.
  - A user replies a forum post that has been previously made by the logged-in user.
- In addition, notifications are sent out to the corresponding teacher when a student submits an assignment.

## Relevant Files
This section will explain the files and its corresponding pages. For more details on the page features, refer to the section above.

### HTML Templates

 1. **layout.html**
	 - contains navbar, header and meta scripts
 2. **index.html**
	 - root path that contains the main 'Updates' page
 3. **assignments.html**
	 - 'Assignments' page, allows teachers to create assignments
 4. **submission.html**
	 - 'Assignments' sub-page, displays the homework and submission details.
 5. **forum.html**
	 - 'Forums' page with search bar, subject navigation, list of posts and option to create a post
 6. **forum_post.html**
	 - 'Forums' sub-page, displays selected forum post with replies and option to reply
 7. **lessons.html**
	 - 'Video Lessons' page that displays lessons for each subject and allows teachers to create lessons
 8. **lesson.html**
	 - 'Video Lessons' sub-page, displays selected video lesson
 9. **login.html**
	 - login page that displays error messages (e.g. 'not yet approved')
 10. **register.html**
	 - registration page where users can choose their subjects and roles
 11. **notification.html**
	 - 'Notification' page which lists all notifications pertaining to the logged-in user.
 12. **resources.html**
	 - 'Resources' page that shows all resources by subject

### models.py
Contains all Models:
1. **User:**
  - Additional 'role' field that marks the user as 'student' or 'teacher'
  - Once registered, account can only be approved by admin before signing in.
  - Otherwise, an error message should indicate that the account has not yet been approved.
2. **Update**
3. **Resource**
4. **Assignment**
5. **Submission**
6.  **Subject**
7. **Post**
8. **Comment**
9. **Lesson**
10. **Notification**

### forms.py
Contains all form classes that are built for creating the model objects.

### urls.py
Contains all traversable path patterns.

### views.py
List of views for the application.  Handles the logic for HTTP requests and form submissions and renders the appropriate HTML template accordingly.

### static files

 - **script.js**
	 - handles JavaScript for DOM manipulation. Also uses the fetch API() for server-side requests.
 - **styles.css**
	 - handles all CSS styles and elements

## Project Justification
This project has features inspired by the previous projects (i.e. search bar in &#39;wiki&#39;, post updates in &#39;network&#39;), but it carries its own distinction and a wider complexity. The distinguishing features include, but are not exclusive to:

1. Delegated user roles with specific permissions (teacher, student, admin)
2. Uploading of files (resources, submissions page)
3. Asynchronous deletion of files (resources page)
4. Notification system (notifications page)
5. Embedding external videos (lessons page)
6. Assignment-tracking (assignments page)
7. Mobile-responsiveness

It utilizes 10 Django models, with numerous Many-To-Many fields. It also employs datetime formatting, with a JavaScript datepicker to set the deadline of assignments. In terms of UI, it was designed for a simple look/feel, with seamless navigation between the different parts. Interrelating multiple components and user-types to create a functioning Learning Management System thus gives shape to the intricate complexity of this project.
