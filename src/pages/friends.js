import './css/friends.css';
import './css/main.css';
import './css/tasks.css'
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';
import yellrab from './img/fri/rabs.png';
import devav from "./img/fri/defav.png";

function Main() {
  const [userData, setUserData] = useState(null);
  const [referrals, setReferrals] = useState([]);
  const navigate = useNavigate();
  const [queryId, setQueryId] = useState(null);

  useEffect(() => {
    const { WebApp } = window.Telegram;
    WebApp.BackButton.show();
    WebApp.BackButton.onClick(() => {
      navigate(-1);
    });

    const user = WebApp.initDataUnsafe?.user;
    const queryId = WebApp.initData;

    if (user) {
      setUserData({
        username: user.username,
        id: user.id,
      });
    }

    if (queryId) {
      setQueryId(queryId);
    }

    // Fetch referral data from the API
    const fetchReferrals = async () => {
      try {
        const response = await axios.get('https://rabbit-test.ru/ref/', {
          headers: {
            'custom-header': queryId
          }
        });
        setReferrals(response.data);
      } catch (error) {
        console.error("Error fetching referral data", error);
      }
    };

    fetchReferrals();
  }, [navigate]);

  // Подсчитываем общую сумму поинтов
  const totalPoints = referrals.reduce((total, referral) => total + referral.point, 0);

  // Функция для копирования ссылки в буфер
  const handleInviteClick = () => {
    if (userData) {
      const referralLink = `https://t.me/Grani_trening_bot?start=${userData.id}`;
  
      if (navigator.share) {
        // Если API Web Share поддерживается, используем его
        navigator.share({
          title: 'Приглашение',
          text: 'Присоединяйся ко мне в Rabbits!',
          url: referralLink,
        })
        .then(() => {
          console.log('Ссылка успешно поделена');
        })
        .catch((error) => {
          console.error('Ошибка при попытке поделиться:', error);
        });
      } else {
        // Если API Web Share не поддерживается, используем Telegram WebApp
        const { WebApp } = window.Telegram;
        WebApp.showPopup({
          message: "Реферальная ссылка скопирована",
          buttons: [{ text: "Ок", id: "ok" }]
        });
  
        // Копируем ссылку в буфер обмена на случай, если пользователь хочет вставить её вручную
        navigator.clipboard.writeText(referralLink).catch(err => {
          console.error("Ошибка при копировании ссылки:", err);
        });
      }
    }
  };
  

  const triggerHapticFeedback = () => {
    const { WebApp } = window.Telegram;
    WebApp.HapticFeedback.impactOccurred('medium');
  };

  return (
    <div className="main-fri">
      <header>
        <div>
          <div className='headone'>
            <p className='h1tasks'>COMPLETE TASKS AND EARN $CRT</p>
          </div>
          <p className='usebostp'>$CRT CAN BE USED TO UPGRADE YOUR FARM</p>
        </div>
      </header>
      <img src={yellrab} width={350} alt="Rabbit"/>
      <button className='tasksavailable tskrab' onClick={triggerHapticFeedback}>RABBIT FAMILY TO DO LIST:</button>

      <div className='tododiv'>
        <Link to="/chooseclan" style={{textDecoration:"none"}}>
          <button className='daylycode todo' onClick={triggerHapticFeedback}>CHOOSE YOUR CLAN</button>
        </Link>
        <Link to="/clancreate" style={{textDecoration:"none"}}>
          <button className='daylycode todo' onClick={triggerHapticFeedback}>CREATE YOUR CLAN</button>
        </Link>
        <Link to="/claninfo" style={{textDecoration:"none"}}>
        <button className='daylycode todo' onClick={triggerHapticFeedback}>LEADERBOARD</button>
        </Link>
      </div>

      <div className='Frlisth1'>
        <span>
          <h1>Friend list</h1>
        </span>
        <span>
          <p>You have {referrals.length} fren's - earned 6.5M $CRT</p>
          <p>Referal’s total points: {totalPoints} $CRT</p>
        </span>
      </div>

      <div className='FriendList'>
        {referrals.length > 0 ? (
          referrals.map((referral, index) => (
            <div className='Frtask' key={index}>
              <span>
                <img src={devav} width={30} alt="Friend avatar"/>
                <p className="refname">@{referral.nick_name}</p>
              </span>
              <span className='spannnn'>{referral.point} points</span>
            </div>
          ))
        ) : (
          <p>No referrals found</p>
        )}
      </div>

      <footer>
        <button className='invfr' onClick={handleInviteClick}>INVITE FRIEND</button> {/* Обновлённый обработчик */}
        <div className='infofr'>5000 $CRT + 10% from your fren + 2% from their referrals</div>
        <div className='fotbtns'>
          <Link to="/" style={{textDecoration:"none"}}>
            <button style={{ borderRight:'1px solid black', borderTopLeftRadius:'5px', borderBottomLeftRadius:'5px' }} onClick={triggerHapticFeedback}>HOME</button>
          </Link>
          <Link to="/upg" style={{textDecoration:"none"}}>
            <button style={{ borderRight:'1px solid black' }} onClick={triggerHapticFeedback}>BOOST</button>
          </Link>
          <Link to="/tasks" style={{textDecoration:"none"}}>
            <button style={{ borderRight:'1px solid black' }} onClick={triggerHapticFeedback}>TASKS</button>
          </Link>
          <Link to="/friends" style={{textDecoration:"none"}}>
            <button className='selectfot' style={{ borderTopRightRadius:'5px', borderBottomRightRadius:'5px' }} onClick={triggerHapticFeedback}>FRIENDS</button>
          </Link>
        </div>
      </footer>
    </div>
  );
}

export default Main;
