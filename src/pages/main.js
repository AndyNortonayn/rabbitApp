import './css/main.css';
import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import tgsvg from './img/mainimg/tg.svg';
import copysvg from './img/mainimg/copy.svg';
import wtr from './img/mainimg/watering.svg';
import devav from './img/mainimg/derak.png';
import { TonConnectUIProvider, useTonConnectUI, useTonWallet, useTonAddress } from '@tonconnect/ui-react';
import { useAudio } from '../AudioProvider';

const API_URL = 'https://rabbit-test.ru/';

function Main() {
  const { toggleAudio, volume } = useAudio();
  const [userData, setUserData] = useState(null);
  const [profileData, setProfileData] = useState(null);
  const [wateringTime, setWateringTime] = useState(null); // Дата и время следующего полива
  const [tonConnectUI] = useTonConnectUI();
  const wallet = useTonWallet();
  const userFriendlyAddress = useTonAddress();
  const navigate = useNavigate();
  const [queryId, setQueryId] = useState(null);
  const [farmn, setFarmn] = useState(1);
  const [walletModalVisible, setWalletModalVisible] = useState(false);
  const [isClaimAvailable, setIsClaimAvailable] = useState(false);
  const pollingInterval = 1000;
  const [countdown, setCountdown] = useState(null);

  useEffect(() => {
    if (wateringTime) {
      const updateCountdown = () => {
        const now = new Date();
        const timeLeft = wateringTime - now;

        if (timeLeft > 0) {
          const hours = Math.floor(timeLeft / (1000 * 60 * 60));
          const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
          const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
          setCountdown(`${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
        } else {
          setCountdown(null); // Обнуляем `countdown`, когда время истекло
          clearInterval(countdownInterval);
        }
      };

      const countdownInterval = setInterval(updateCountdown, 1000);
      return () => clearInterval(countdownInterval);
    }
  }, [wateringTime]);
  useEffect(() => {
    const { WebApp } = window.Telegram;
    WebApp.BackButton.hide();
    WebApp.disableVerticalSwipes();
    WebApp.expand();

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
  }, [navigate]);

  useEffect(() => {
    if (!queryId) return;

    const fetchData = async () => {
      try {
        // Запрос профиля
        const profileResponse = await axios.get(`${API_URL}profile/${farmn}`, {
          headers: { 'custom-header': queryId },
        });
        setProfileData(profileResponse.data);

        // Записываем время следующего полива
        const lastWateringSeconds = profileResponse.data.last_watering;
        setWateringTime(new Date(lastWateringSeconds));

      } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, pollingInterval);

    return () => clearInterval(intervalId);
  }, [queryId, farmn]);

  const triggerHapticFeedback = () => {
    const { WebApp } = window.Telegram;
    WebApp.HapticFeedback.impactOccurred('medium');
  };

  const handleConnectWallet = async () => {
    try {
      await tonConnectUI.connectWallet();
      triggerHapticFeedback();
    } catch (error) {
      console.error('Ошибка подключения кошелька:', error);
    }
  };

  const handleDisconnectWallet = async () => {
    try {
      await tonConnectUI.disconnect();
      setWalletModalVisible(false);
      triggerHapticFeedback();
    } catch (error) {
      console.error('Ошибка отключения кошелька:', error);
    }
  };

  const maskWallet = (address) => {
    if (!address) return '';
    return `${address.slice(0, 5)}*****${address.slice(-7)}`;
  };

  const handleWatering = async () => {
    try {
      await axios.get(`${API_URL}profile/watering/${farmn}`, {
        headers: { 'custom-header': queryId },
      });
      alert('Полив успешно выполнен!');
    } catch (error) {
      console.error('Ошибка полива:', error);
    }
  };

  const handleClaim = async () => {
    try {
      const response = await fetch(`https://rabbit-test.ru/profile/claim/${farmn}/`, {
        method: 'GET',
        headers: {
          'custom-header': queryId,
        }
      });
  
      if (response.ok) {
        // Если ответ успешен, запускаем соответствующее действие, например, обновляем баланс
        console.log("Claim successful");
        // Обновить состояние или вызвать другие функции по необходимости
      } else {
        const data = await response.json();
        if (data.detail === "Time limit") {
          // Обновляем состояние для показа тайм-лимита
          setIsClaimAvailable(false);
          console.log("Claim unavailable due to time limit");
        } else {
          console.error("Unexpected error:", data);
        }
      }
    } catch (error) {
      console.error("Request failed", error);
    }
  };

  const handleWalletClick = () => {
    if (wallet) {
      handleDisconnectWallet();
    } else {
      handleConnectWallet();
    }
  };

  const closeWalletModal = () => {
    setWalletModalVisible(false);
  };

  const handleCopyWallet = () => {
    if (userFriendlyAddress) {
      navigator.clipboard.writeText(userFriendlyAddress);
      alert('Адрес кошелька скопирован в буфер обмена');
    } else {
      alert('Адрес кошелька недоступен');
    }
  };

  useEffect(() => {
    if (profileData?.claim_access) {
      const claimDate = new Date(profileData.claim_access);
      const now = new Date();
      setIsClaimAvailable(claimDate <= now);
    }
  }, [profileData]);

  const formatTime = (date) => {
    if (!date) return '';
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
  };
  return (
    <TonConnectUIProvider manifestUrl="https://jettocoinwebapp.vercel.app/tonconnect-manifest.json">
      <div className="main">
        <header>
          <div>
            <div className='headone'>
              <img src={profileData?.avatar || devav} alt="Avatar" className='avatar' />
              <button onClick={handleDisconnectWallet} className="wallet-button">
                <svg width="24" height="77" viewBox="0 0 77 77" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M16 60.8H20.56L51.84 29.52L47.28 24.96L16 56.24V60.8ZM9.59998 67.2V53.6L51.84 11.44C52.48 10.8533 53.1866 10.4 53.96 10.08C54.7333 9.75998 55.5466 9.59998 56.4 9.59998C57.2533 9.59998 58.08 9.75998 58.88 10.08C59.68 10.4 60.3733 10.88 60.96 11.52L65.36 16C66 16.5866 66.4666 17.28 66.76 18.08C67.0533 18.88 67.2 19.68 67.2 20.48C67.2 21.3333 67.0533 22.1466 66.76 22.92C66.4666 23.6933 66 24.4 65.36 25.04L23.2 67.2H9.59998ZM49.52 27.28L47.28 24.96L51.84 29.52L49.52 27.28Z" fill="white" />
                </svg>
              </button>
              <div className='wallet'>
                <p className='tag'>@{userData?.username}</p>
                {wallet ? (
                  <p className='wallet-button walletnum' onClick={handleWalletClick}>{maskWallet(userFriendlyAddress)}</p>
                ) : (
                  <button onClick={handleConnectWallet} className="wallet-button">Connect wallet</button>
                )}
              </div>
            </div>
            <div className='farmbtns'>
              {[1, 2, 3].map((farm, index) => (
                <button
                  key={index}
                  className={farmn === farm ? 'selectfarm' : ''}
                  onClick={() => setFarmn(farm)} // Необходимо добавить обработчик нажатия
                >
                  FARM {farm}
                </button>
              ))}
            </div>
          </div>
        </header>

        {profileData && (
          <div className='balance'>
            <div className='divbal'>
              <p>BALANCE: {profileData.amount_CRT} $CRT</p>
              <p className='nono'>STORAGE: {profileData.amount_storage} $CRT</p>
            </div>
            <button 
  className={`balance-claim ${isClaimAvailable ? 'inactive' : ''}`} 
  onClick={() => { 
    if (isClaimAvailable) {
      triggerHapticFeedback(); 
      handleClaim(); 
    }
  }}
>
  CLAIM
</button>
          </div>
        )}

        <div className='social'>
          <button onClick={triggerHapticFeedback}>
            <img src={tgsvg} width={32} alt="Telegram" />
            join our TG
          </button>
          <button className='soundbtn' onClick={toggleAudio}>
            <svg width="24" height="25" viewBox="0 0 24 25" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5.889 16.5H2C1.73478 16.5 1.48043 16.3947 1.29289 16.2071C1.10536 16.0196 1 15.7652 1 15.5V9.50002C1 9.23481 1.10536 8.98045 1.29289 8.79291C1.48043 8.60538 1.73478 8.50002 2 8.50002H5.889L11.183 4.16802C11.2563 4.10797 11.3451 4.06996 11.4391 4.05841C11.5331 4.04687 11.6284 4.06227 11.714 4.10282C11.7996 4.14337 11.872 4.2074 11.9226 4.28745C11.9732 4.36751 12.0001 4.4603 12 4.55502V20.445C12.0001 20.5397 11.9732 20.6325 11.9226 20.7126C11.872 20.7926 11.7996 20.8567 11.714 20.8972C11.6284 20.9378 11.5331 20.9532 11.4391 20.9416C11.3451 20.9301 11.2563 20.8921 11.183 20.832L5.89 16.5H5.889ZM19.406 20.634L17.99 19.218C18.938 18.3745 19.6964 17.3397 20.2152 16.1817C20.734 15.0237 21.0015 13.7689 21 12.5C21.0012 11.1661 20.7054 9.84867 20.1339 8.64339C19.5624 7.43811 18.7296 6.37526 17.696 5.53202L19.116 4.11202C20.3345 5.14357 21.3132 6.4285 21.9841 7.87722C22.6549 9.32593 23.0016 10.9035 23 12.5C23 15.723 21.614 18.622 19.406 20.634ZM15.863 17.091L14.441 15.669C14.9265 15.2957 15.3196 14.8158 15.5899 14.2663C15.8602 13.7167 16.0006 13.1124 16 12.5C16 11.07 15.25 9.81502 14.12 9.10802L15.559 7.66902C16.3165 8.22621 16.9321 8.95387 17.3562 9.79314C17.7802 10.6324 18.0008 11.5597 18 12.5C18 14.342 17.17 15.99 15.863 17.091Z" fill="white" />
            </svg>
            <p>{volume}%</p>
          </button>
        </div>

        <div className='footbar'>
          <div className='farmcont'>
            <p>FARM {farmn}</p>
            <p><img src={copysvg} width={25} alt="Copy" />NFT's CONNECTED: {profileData?.nft_connected.length || 0}</p>
          </div>
          <div className='progressbar-container'>
            <div className='numbers'>
              <p>{profileData?.watering_bar}%</p>
              <p>100%</p>
            </div>
            <div className='progressbar'>
              <div className='bar' style={{ width: `${profileData?.watering_bar}%` }}></div>
            </div>
          </div>
        </div>

        <button className='watering' onClick={handleWatering}>
          {countdown ? countdown : <><img src={wtr} width={25} alt="Watering" /> watering</>}
        </button>

        <footer>
          <div className='fotbtns'>
            <Link to="/" style={{ textDecoration: "none" }}>
              <button className='selectfot' style={{ borderRight: '1px solid black', borderTopLeftRadius: '5px', borderBottomLeftRadius: '5px' }} onClick={triggerHapticFeedback}>HOME</button>
            </Link>
            <Link to="/upg" style={{ textDecoration: "none" }}>
              <button style={{ borderRight: '1px solid black' }} onClick={triggerHapticFeedback}>BOOST</button>
            </Link>
            <Link to="/tasks" style={{ textDecoration: "none" }}>
              <button style={{ borderRight: '1px solid black' }} onClick={triggerHapticFeedback}>TASKS</button>
            </Link>
            <Link to="/friends" style={{ textDecoration: "none" }}>
              <button style={{ borderTopRightRadius: '5px', borderBottomRightRadius: '5px' }} onClick={triggerHapticFeedback}>FRIENDS</button>
            </Link>
          </div>
        </footer>
      </div>
    </TonConnectUIProvider>
  );

}

export default Main;
