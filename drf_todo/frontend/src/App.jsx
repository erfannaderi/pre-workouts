import React from "react";
import './App.css';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            todoList: [],
            activeItem: {
                id: null,
                title: '',
                completed: false
            },
            editing: false,
        };
        this.fetchTasks = this.fetchTasks.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        this.fetchTasks();
        const csrftoken = this.getCookie('csrftoken');
        this.setState({csrftoken: csrftoken});
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    fetchTasks() {
        fetch('http://127.0.0.1:8000/api/task-list/')
            .then(response => response.json())
            .then(data => this.setState({todoList: data}));
    }

    handleChange(e) {
        const {name, value} = e.target;
        this.setState({
            activeItem: {
                ...this.state.activeItem,
                title: value
            }
        });
    }

    handleSubmit(e) {
        e.preventDefault();
        var url = 'http://127.0.0.1:8000/api/task-create/';
        const {csrftoken} = this.state;
        var method = 'POST';
        if (this.state.editing == true) {
            url = `http://127.0.0.1:8000/api/task-update/${this.state.activeItem.id}/`
            method = 'PUT'

        }
        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(this.state.activeItem),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Task added:', data);
                this.setState({editing: false});
                this.fetchTasks();
            })
            .catch(error => console.log(error));
    }

    startEdit(task) {
        this.setState({activeItem: task, editing: true});
    }

    startDelete(task) {
        const {csrftoken} = this.state;
        fetch(`http://127.0.0.1:8000/api/task-delete/${task.id}`, {
            method: 'DELETE',
            'headers': {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            }
        }).then((response) => {
            this.fetchTasks()
        })
    }

    strikeUnstrik(task) {
        task.completed = !task.completed;
        const {csrftoken} = this.state;
        this.setState({activeItem: task, editing: true});

        // var url = `http://127.0.0.1:8000/api/task-update/${task.id}`
        // fetch(url, {
        //     method: 'PUT',
        //     'headers': {
        //         'Content-Type': 'application/json',
        //         'X-CSRFToken': csrftoken,
        //     },
        //     body: JSON.stringify({"completed": task.completed, 'title': task.title})
        // }).then((response) => {
        //     this.fetchTasks()
        // });  // var url = `http://127.0.0.1:8000/api/task-update/${task.id}`
        // fetch(url, {
        //     method: 'PUT',
        //     'headers': {
        //         'Content-Type': 'application/json',
        //         'X-CSRFToken': csrftoken,
        //     },
        //     body: JSON.stringify({"completed": task.completed, 'title': task.title})
        // }).then((response) => {
        //     this.fetchTasks()
        // });
    }

    render() {
        var tasks = this.state.todoList;
        var self = this
        return (
            <div className="container m-auto">
                <div id="task-container">
                    <div id="form-wrapper">
                        <form id='form' onSubmit={this.handleSubmit}>
                            <div className="flex-wrapper">
                                <div style={{flex: 6}}>
                                    {/*<p><strong>to mark as completed press edit then on the task then press butten to*/}
                                    {/*    sumbit queerry</strong></p>*/}
                                    <label htmlFor="title" className='text-success'>Add Task</label>
                                    <input onChange={this.handleChange} value={this.state.activeItem.title}
                                           className="form-control" id="title" type="text" name="title"/>
                                </div>
                                <div style={{flex: 1}}>
                                    <button className="btn btn-warning mt-2" type="submit">Add Task</button>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div id="list-wrapper">
                        {tasks.map((task, index) => (
                            <div onClick={() => self.strikeUnstrik(task)} key={index} className="task-wrapper card">
                                <div className="card-body d-flex justify-content-between align-items-center">
                                    {task.completed == false ? (
                                        <span>{task.title}</span>
                                    ) : (<strike>{task.title}</strike>)}
                                    <div>
                                        <button onClick={() => self.startEdit(task)}
                                                className="btn btn-sm btn-outline-info">Edit
                                        </button>
                                        <button onClick={() => self.startDelete(task)}
                                                className="btn btn-sm btn-outline-danger ms-2">Delete
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
