window.addEventListener("DOMContentLoaded", function () {
    // This code activates flatpickr on fields with the 'datetimefield' class when the document has loaded
    flatpickr(".datetimefield", {
        enableTime: true,
        enableSeconds: true,
        dateFormat: "Y-m-d H:i:S",
    });

    if (document.getElementById("create-assignment") != null) {
        document.getElementById("create-assignment").onclick = function() {
            let form = document.getElementById("assignment-form");
            if (form.style.display === "none") {
                form.style.display = "inline";
            } else {
                form.style.display = "none";
            }
        }
    }

    lessonSubjects = document.getElementsByClassName("btn btn-link subject-title");
    for (var i = 0; i < lessonSubjects.length; i++) {
        lessonSubjects[i].onclick = function () {
            if (this.nextElementSibling.style.display === "none") {
                this.nextElementSibling.style.display = "inline";
            } else {
                this.nextElementSibling.style.display = "none";
            }
        }
    }

    lessonsElement = document.getElementsByClassName("lesson-container");
    for (var i = 0; i < lessonsElement.length; i++) {
        lessonsElement[i].onclick = function () {
            
        }
    }

    // if editElement is not null, means the post is editable
    editElement = document.getElementById("edit");
    if (editElement != null) {
        editElement.onclick = function () {
            postContent = document.getElementById("post-content");
            edit_post(postContent, editElement);
        }
    }

    // if delete elements length > 0, means resources are deletable
    deleteElements = document.getElementsByClassName("delete-resource");
    for (var i = 0; i < deleteElements.length; i++) {
        
        deleteElements[i].onclick = function () {

            split_id = this.id.split("-");
            resource_id = split_id[0];
            resource_filename = split_id[1];

            var confirmation = confirm("Are you sure you want to delete " + resource_filename + "?");
            
            if (confirmation == true) {
                
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                // save the post
                fetch(window.location.pathname, {
                    method: 'PUT',
                    headers: {'X-CSRFToken': csrftoken},
                    body: JSON.stringify({
                        deleted: true,
                        deleted_id: resource_id,
                    })
                })
                .then(response => response.json())
                .then(result => {
                    // if result is OK, update the DOM
                    this.parentElement.parentElement.innerHTML = "";
                });

            } else {
                console.log("no delete");
            }
        }
    }

});

function edit_post(post, editEle) {
    // textarea currently being edited
    if(document.getElementById('editing') != null) {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        // save the post
        fetch(window.location.pathname, {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                content: document.getElementById('editing').value
            })
        })
        .then(response => response.json())
        .then(result => {
            // if result is OK, update the DOM
            post.innerHTML = result['content'];
            editEle.innerHTML = "Edit";
            //document.getElementById('post-timestamp').innerHTML = "Last modified: " + result['last_modified'] + " (edited)";
        });
        return;
    }

    original_content = post.innerHTML.trim();
    console.log(original_content);
    post.innerHTML = "<textarea id='editing" + "' rows='3' cols='60'>" + original_content + "</textarea>";
    editEle.innerHTML = "Save";
  
  }