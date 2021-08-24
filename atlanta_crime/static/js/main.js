if (window.location.pathname === "/send"){
  // api requests
  // get ll todos/customers
  function getAllTodos(){
    $.ajax({
      url: "/api/customers",
      method: "GET",
      success: response => {
        const data = response.data.todos;
        const todo_list = document.querySelector("#todo-list");
        data.map(item=>{
          todo_list.innerHTML +=`
          <p><small>${item.name}</small></p>
          <p><small>${item.subject}</small></p>

          `
        })
      },
      error: err =>{
        console.log(err);
      }
    })
  }

  function postCreateTodo(){
    $.ajax({
      url:"/api/customers",
      method: "POST",
      data:{
        "name": $("#name").val(),
        "email": $("#email").val(),
        "subject": $("#subject").val(),
        "message": $("#message").val()
      },
      success: response => {
        console.log(response);
      },
      error: err => {
        console.log(err);
      }

    })

  } 
  getAllTodos();

  $("add-todo").on("submit", () => {
    postCreateTodo()
  })
}