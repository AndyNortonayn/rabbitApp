import './css/tasks.css';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import yellrab from './img/tasks/redrabbit.png';
import { Link } from 'react-router-dom';

function Main() {
  const [userData, setUserData] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [completedTasksCount, setCompletedTasksCount] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const { WebApp } = window.Telegram;
    WebApp.BackButton.show();
    const customhead = WebApp.initData;
    WebApp.BackButton.onClick(() => {
      navigate(-1);
    });

    const user = WebApp.initDataUnsafe?.user;
    if (user) {
      setUserData({
        username: user.username,
        avatarUrl: user.photo_url,
      });
    }

    fetchTasks(); // Инициализируем загрузку задач при монтировании компонента
  }, []);

  // Функция для запроса задач с бэкенда
  const fetchTasks = () => {
    const { WebApp } = window.Telegram;
    const customhead = WebApp.initData;

    fetch('https://rabbit-test.ru/task/', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'custom-header': customhead,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setTasks(data);
        const completedCount = data.filter(task => task.done).length;
        setCompletedTasksCount(completedCount);
      })
      .catch((error) => {
        console.error('Ошибка при получении задач:', error);
      });
  };

  const handleTaskCompletion = (taskId) => {
    const { WebApp } = window.Telegram;
    const customhead = WebApp.initData;

    fetch(`https://rabbit-test.ru/task/${taskId}`, {
      method: 'PATCH',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'custom-header': customhead,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Ошибка при выполнении задачи: ${response.status}`);
        }
        return response.json();
      })
      .then((updatedTask) => {
        console.log("Задача обновлена на сервере:", updatedTask);
        WebApp.HapticFeedback.impactOccurred("medium");

        // Перезапрос задач после обновления задачи
        fetchTasks();
      })
      .catch((error) => {
        console.error('Ошибка при выполнении задачи:', error);
      });
  };

  const handleTaskClick = (task) => {
    window.open(task.url, '_blank');
    handleTaskCompletion(task.id);
  };

  const isTaskCompleted = (task) => task.done;

  return (
    <div className="main-tsk">
      <header>
        <div>
          <div className='headone'>
            <p className='h1tasks'>COMPLETE TASKS AND EARN $CRT</p>
          </div>
          <p className='usebostp'>$CRT CAN BE USED TO UPGRADE YOUR FARM</p>
        </div>
      </header>
      
      <button className='tasksavailable'>
       available tasks: {completedTasksCount}/{tasks.length}
      </button>

      <div className='taskscont'>
        {tasks.map((task) => (
          <div className='tasks' key={task.id}>
            <span>
              <p>{task.name}</p>
            </span>
            <button 
              onClick={() => handleTaskClick(task)} 
              disabled={isTaskCompleted(task)}
              className={isTaskCompleted(task) ? 'disabled' : ''}
            >
              <p>{isTaskCompleted(task) ? "DONE" : "CHECK"}</p>
              <p>{task.amount} $CRT</p>
            </button>
          </div>
        ))}
      </div>

      <button className='daylycode'>
        DAILY CODE: 12312
      </button>

      <footer>
        <div className='rabclub'>
          <div className='rabclubcont'>
            <div className='rabclubinfo rabtasks'>
              <p>VOTE FOR US IN THE OPEN LEAGUE SEASON XI</p>
              <button>VOTE</button>
            </div>
            <img src={yellrab}/>
          </div>
        </div>
        <div className='fotbtns'>
          <Link to="/" style={{textDecoration: "none"}}>
            <button 
              style={{ borderRight: '1px solid black', borderTopLeftRadius: '5px', borderBottomLeftRadius: '5px'}} 
            >
              HOME
            </button>
          </Link>
          <Link to="/upg" style={{textDecoration: "none"}}>
            <button style={{ borderRight: '1px solid black'}}>
              BOOST
            </button>
          </Link>
          <Link to="/tasks" style={{textDecoration: "none"}}>
            <button className='selectfot' style={{ borderRight: '1px solid black'}}>
              TASKS
            </button>
          </Link>
          <Link to="/friends" style={{textDecoration: "none"}}>
            <button style={{ borderTopRightRadius: '5px', borderBottomRightRadius: '5px'}}>
              FRIENDS
            </button>
          </Link>
        </div>
      </footer>
    </div>
  );
}

export default Main;
