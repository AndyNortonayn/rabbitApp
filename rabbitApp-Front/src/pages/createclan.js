import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import './css/createclan.css';
import creclanav from './img/creclan/rabclub.svg';

axios.defaults.baseURL = 'https://rabbit-test.ru/'; // Базовый URL вашего API

function Main() {
  const [userData, setUserData] = useState(null);
  const [clanData, setClanData] = useState(null);
  const [clanName, setClanName] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [responseMessage, setResponseMessage] = useState('');
  const navigate = useNavigate();

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
        avatarUrl: user.photo_url,
        queryId: queryId
      });
    }

    // Функция для получения данных профиля и клана
    const fetchProfileAndClanData = async () => {
      try {
        const profileResponse = await axios.get(`/profile/1`, {
          headers: {
            'custom-header': queryId // Передаем query_id в заголовке
          }
        });

        const clanId = profileResponse.data.clan_id;
        if (clanId) {
          const clanResponse = await axios.get(`/clan/${clanId}`, {
            headers: {
              'custom-header': queryId
            }
          });
          setClanData(clanResponse.data);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProfileAndClanData();
  }, [navigate]);

  const triggerHapticFeedback = () => {
    const { WebApp } = window.Telegram;
    WebApp.HapticFeedback.impactOccurred('medium');
  };

  const handleCreateClan = async () => {
    if (clanData) {
      alert('You are already in a clan!');
      return;
    }

    setError(null); // Сброс ошибок перед новым запросом
    try {
      const response = await axios.post(`/clan/${clanName}`, null, {
        headers: {
          'custom-header': userData.queryId // Передаем query_id в заголовке
        }
      });
      setResponseMessage(`Clan "${response.data.name}" created successfully!`);
    } catch (err) {
      if (err.response && err.response.status === 422) {
        // Ошибка валидации
        setError('Validation error: ' + JSON.stringify(err.response.data.detail));
      } else {
        setError('Error creating clan: ' + err.message);
      }
    }
  };

  return (
    <div className="main-creclan">
      <header>
        <div>
          <div className='headone'>
            <p className='h1tasks'>CREATE YOUR CLAN</p>
          </div>
        </div>
      </header>

      <div className='create-clan'>
        <>
          <input
            type="text"
            value={clanName}
            onChange={(e) => setClanName(e.target.value)}
            placeholder="Clan name"
          />
          {responseMessage && <p>{responseMessage}</p>}
        </>
      </div>
      
      <footer>
        <img src={creclanav} width={150} alt="Clan Avatar"/>
        <Link to="/claninfo" style={{textDecoration:"none"}}>
          <button 
            className='creclanbtn' 
            onClick={() => {
              triggerHapticFeedback();
              handleCreateClan();
            }}
          >
            CREATE CLAN
          </button>
        </Link>
        <div className='fotbtns'>
          <Link to="/" style={{textDecoration:"none"}}>
            <button className='homeclan' onClick={triggerHapticFeedback}>HOME</button>
          </Link>
        </div>
      </footer>
    </div>
  );
}

export default Main;
