import './css/nft.css';
import './css/main.css';
import './css/upgrade.css';
import './css/createclan.css';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import creclanav from './img/creclan/image.png';
import whiterab from './img/nft/whiterab.png';
import tgsvg from './img/mainimg/tg.svg';

function Main() {
  const [userData, setUserData] = useState(null);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
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
  }, [navigate]);

  const triggerHapticFeedback = () => {
    const { WebApp } = window.Telegram;
    WebApp.HapticFeedback.impactOccurred('medium');
  };

  const handleClickInfo = () => {
    setIsPopupOpen(true);
    triggerHapticFeedback();
  };

  const closePopup = () => {
    setIsPopupOpen(false);
    triggerHapticFeedback();
  };

  return (
    <div className="main-creclan">
      <header>
        <div>
          <div className="headone">
            <p className="h1nft">USE YOUR RABBIT CLUB NFT’S TO BOOST UP YOUR FARM</p>
          </div>
        </div>
      </header>

      <p className="aboutour">ABOUT OUR NFT’S</p>
      <div className="rabbits">
        {[1, 2, 3].map((_, index) => (
          <div key={index} className="rabs">
            <img src={whiterab} className="rab" alt="White Rabbit"></img>
            <span>
              <span className="rabname">WHITE RABBIT</span>
              <span className="clickinfo" onClick={handleClickInfo}>
                CLICK TO LEARN MORE
              </span>
            </span>
          </div>
        ))}
      </div>

      {isPopupOpen && (
        <div className="popup">
          <div className="popup-content">
            <img src={whiterab} className="rab" alt="White Rabbit"></img>
            <h2>White Rabbit</h2>
            <p>1 NFT - 1 additional garden bed for 2X mining speed $CRT</p>
            <p>2 NFT’s - 2 additional garden bed for 3X mining speed $CRT</p>
            <p>3 NFT’s - 4 additional garden bed for 5X mining speed $CRT</p>
            <button className='popbuyon' onClick={triggerHapticFeedback}>BUY ON GETGEMS</button>
            <button className="close-popup" onClick={closePopup}>CLOSE</button>
          </div>
        </div>
      )}

      <footer>
        <div className="social soc">
          <button onClick={triggerHapticFeedback}>
            <img src={tgsvg} width={32} alt="Telegram"></img>join our official channel
          </button>
        </div>

        <img className="imgfot" src={creclanav} width={200} alt="Footer Image" />
        <button className="buynftnew" onClick={triggerHapticFeedback}>BUY NEW NFT</button>
        <div className="fotbtns">
          <Link to="/" style={{ textDecoration: 'none' }}>
            <button className="homeclan" onClick={triggerHapticFeedback}>HOME</button>
          </Link>
        </div>
      </footer>
    </div>
  );
}

export default Main;
