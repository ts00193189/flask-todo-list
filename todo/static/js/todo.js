document.addEventListener('DOMContentLoaded', function() {
    get_todos(user_name);
    const task_submit_btn = document.getElementById('task_submit');
    const task_form = document.getElementById('task_form');
    task_submit_btn.addEventListener('click', function() {
        let form_data = new FormData(task_form);
        add_todo(user_name, form_data);
        location.reload();
    });
});

function add_todo(user_name, form_data) {
    axios.post("/todo/" + user_name, form_data)
    .then(function(res) {
        console.log("add task success");
    })
    .catch(function(err) {
        console.log("add task error");
    });
}

function get_todos(user_name) {
    axios.get("/todo/" + user_name)
    .then(function(res) {
        let todos = res.data.todos
        const todo_table = document.getElementById("todo_table");
        let todo_body = todo_table.querySelector("tbody");
        add_todos_rows(todos, todo_body);
    })
    .catch(function(err) {
        console.log("get todos error");
    });
}

function add_todos_rows(todos, todo_body) {
    for (let idx = 0; idx < todos.length; idx++) {
        let row = document.createElement("tr");
        let head = document.createElement("th");
        head.setAttribute("scope", "row");
        head.innerHTML = todos[idx]["task_id"];
        row.append(head);

        for (let key of ["task_name", "task_content", "task_date", "task_time"]) {
            let data = document.createElement("td");
            data.innerHTML = todos[idx][key];
            row.append(data);
        }

        for (let btn_name of ["edit", "delete"]) {
            let col = document.createElement("td");
            let btn = document.createElement("button");
            btn.setAttribute("type", "button");
            btn.classList = "btn btn-outline-secondary btn-sm";
            btn.innerHTML = btn_name;
            col.append(btn);
            row.append(col);
        }

        todo_body.append(row);
    }
}