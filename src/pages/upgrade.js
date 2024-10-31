import './css/upgrade.css';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom'; // Добавлен импорт Link
import { useEffect, useState } from 'react';
import axios from 'axios';
import yellrab from './img/upg/yellrab.png';

// Компонент для отображения и покупки Boost
function BoostItem({ level, price, onBuy }) {
  return (
    <div className='boost'>
      <span>
        <p>Upgrade 1</p>
        <p>level {level}/3</p>
      </span>
      <button onClick={onBuy}>
        <p>BUY</p>
        <p>{price} $CRT</p>
      </button>
    </div>
  );
}

function Main() {
  const [userData, setUserData] = useState(null);
  const [boosts, setBoosts] = useState([]);
  const navigate = useNavigate();
  
  useEffect(() => {
    const { WebApp } = window.Telegram;
    
    WebApp.BackButton.show();
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

    axios.get('https://147.45.246.69:8001/boost/')
      .then(response => {
        setBoosts(response.data);
      })
      .catch(error => {
        console.error('Ошибка при получении списка Boost:', error);
      });
  }, [navigate]);

  const triggerHapticFeedback = () => {
    const { WebApp } = window.Telegram;
    WebApp.HapticFeedback.impactOccurred("medium");
  };

  const buyBoost = (id_boost) => {
    const { WebApp } = window.Telegram;
    const queryId = WebApp.initDataUnsafe?.query_id;

    axios.patch(`https://147.45.246.69:8001/boost/${id_boost}/`, {}, {
      headers: {
        'custom-header': `query_id=${queryId}`
      }
    })
    .then(response => {
      console.log('Boost purchased:', response.data);
    })
    .catch(error => {
      console.error('Ошибка при покупке Boost:', error);
    });
  };

  return (
    <div className="main-upg">
      <header>
        <div>
          <div className='headone'>
            <p className='h1upg'>UPGRADE YOUR FARM</p>
          </div>
          <p className='usebostp'>USE BOOSTS TO INCREASE YOUR $CRT FARMING RATES</p>
        </div>
      </header>

      <div className='boostcont'>
        {boosts.map((boost) => (
          <BoostItem
            key={boost.id}
            level={boost.auto_watering}
            price={500}
            onBuy={() => {
              triggerHapticFeedback();
              buyBoost(boost.id);
            }}
          />
        ))}
      </div>

      <button className='buyfarm' onClick={triggerHapticFeedback}>
        <p>BUY NEW FARM</p>
        <h1>100 000 000 $CRT + TWO BROTHERS NFT</h1>
      </button>

      <footer>
        <div className='rabclub'>
          <div className='rabclubcont'>
            <img src={yellrab} alt="Rabbit club" />
            <div className='rabclubinfo'>
              <p>Rabbit club socials give you latest alpha on the project</p>
              <button onClick={triggerHapticFeedback}>JOIN US NOW</button>
            </div>
          </div>
        </div>

        <Link to="/nft" style={{textDecoration: "none"}}>
          <button className='boostfarmnft' onClick={triggerHapticFeedback}>
            BOOST FARM WITH NFT
          </button>
        </Link>

        <div className='fotbtns'>
          <Link to="/" style={{textDecoration: "none"}}>
            <button 
              style={{ borderRight: '1px solid black', borderTopLeftRadius: '5px', borderBottomLeftRadius: '5px'}}
              onClick={triggerHapticFeedback}
            >
              HOME
            </button>
          </Link>
          <Link to="/upg" style={{textDecoration: "none"}}>
            <button className='selectfot' style={{ borderRight: '1px solid black'}} onClick={triggerHapticFeedback}>
              BOOST
            </button>
          </Link>
          <Link to="/tasks" style={{textDecoration: "none"}}>
            <button style={{ borderRight: '1px solid black'}} onClick={triggerHapticFeedback}>
              TASKS
            </button>
          </Link>
          <Link to="/friends" style={{textDecoration: "none"}}>
            <button style={{ borderTopRightRadius: '5px', borderBottomRightRadius: '5px'}} onClick={triggerHapticFeedback}>
              FRIENDS
            </button>
          </Link>
        </div>
      </footer>  
    </div>
  );
}

export default Main;
